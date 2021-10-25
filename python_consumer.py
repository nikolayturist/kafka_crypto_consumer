from kafka import KafkaConsumer, OffsetAndMetadata
from json import loads
import sys
from optparse import OptionParser


class CryptoConsumer:

    def __init__(self, config):
        self.commit_size = config["commit_size"]
        self.max_price_count = 10

        self.consumer = KafkaConsumer(
            config["topic"],
            bootstrap_servers=config["servers"],
            group_id=config["group"],
            enable_auto_commit=False,
            value_deserializer=lambda x: loads(x.decode('utf-8')),
        )

    def _calc_max_prices(self, existing_top10, new_data):
        existing_top10.extend(sorted(new_data, reverse=True)[0:self.max_price_count])
        return sorted(existing_top10, reverse=True)[0:self.max_price_count]

    def consume_messages(self):

        raw_prices = {}
        top_prices = []
        msg_cnt = 0

        while True:
            message_batch = self.consumer.poll(self.commit_size)

            for topic_partition, partition_batch in message_batch.items():
                for message in partition_batch:
                    # do processing of message
                    msg_data = message[6]["data"]
                    raw_prices[msg_data["id"]] = msg_data["price"]

                    msg_cnt += 1
                    if message.offset % self.commit_size == 0:
                        # pass the topic, partition and offset as a dict of TopicPartition: OffsetAndMetadata
                        self.consumer.commit({topic_partition: OffsetAndMetadata(message.offset, "no metadata")})

                    if msg_cnt == self.commit_size:
                        top_prices = self._calc_max_prices(top_prices, raw_prices.values())
                        print(top_prices)
                        raw_prices.clear()
                        msg_cnt = 0


if __name__ == "__main__":

    config = {}

    if len(sys.argv) <= 4:
        print("Not enough arguments. Usage: python_consumer.py -t <topic_name> -s <server_list>, -c <commit_size> ")
        exit(0)

    parser = OptionParser()
    parser.add_option("-t", "--topic", dest="topic", help="Specifies KAFKA topic for message")
    parser.add_option("-s", "--servers", dest="servers", help="Specifies KAFKA server")
    parser.add_option("-c", "--commit_size", dest="commit_size", help="Specifies KAFKA commit size")
    parser.add_option("-g", "--group_name", dest="group_name", help="Specifies KAFKA commit size")

    (options, args) = parser.parse_args(sys.argv)
    topic = ""
    if options.topic:
        config["topic"] = options.topic

    if options.servers:
        config["servers"] = options.servers.split(",")

    if options.commit_size:
        config["commit_size"] = int(options.commit_size)

    if options.group_name:
        config["group"] = options.group_name
    else:
        config["group"] = "group1"

    print(config)

    message_consumer = CryptoConsumer(config)
    message_consumer.consume_messages()
