from time import sleep
from json import dumps
from kafka import KafkaProducer
import json


CRYPTO_TOPIC_NAME = "crypto_order_created"


def main():
    producer = KafkaProducer(bootstrap_servers=['localhost:9093'],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))

    with open("data/data.json", "r") as jfile:
        json_data = json.load(jfile)

    for data_item in json_data["payload"]:
        item = data_item["data"]
        msg = {"id": item["id"], "order_type": item["order_type"], "amount": item["amount"], "price": item["price"]}
        producer.send(CRYPTO_TOPIC_NAME, value=msg)
        print("Send message {msg}".format(msg=str(msg)))
        sleep(5)


if __name__ == "__main__":
    main()
