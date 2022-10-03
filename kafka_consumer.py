from kafka import KafkaConsumer
from json import loads
from google.cloud import storage
import time

MAX_PRICE_COUNT = 10
BUCKET_NAME = "crypto_storage_bucket"

consumer = KafkaConsumer(
    'crypto_topic',
    bootstrap_servers=['localhost:9092'],
    group_id='group-1',
    enable_auto_commit=False,
    value_deserializer=lambda x: loads(x.decode('utf-8')),
)

def calc_max_prices(existed_data, new_data):
    existed_data.extend(sorted(new_data, reverse=True)[0:MAX_PRICE_COUNT])
    return sorted(existed_data, reverse=True)[0:MAX_PRICE_COUNT]

def load_prices(bucket):
    blobs = storage_client.list_blobs(BUCKET_NAME)

    if blobs:
        tss = [int(bn.name.replace(".txt", "")) for bn in blobs]
        if tss:
            latest_ts = str(max(tss))
            blob = bucket.blob(latest_ts + ".txt")
            content = list(map(int, blob.download_as_string().decode("utf-8").strip().split(",")))

            print("-------------------------------------------------")
            print("Max prices loaded from bucket")
            print(str(content))

            return content
    return [0] * MAX_PRICE_COUNT

def save_prices(bucket, data):
    ts = str(round(time.time()*1000))
    blob_name = f"{ts}.txt".format(ts=ts)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(",".join([str(e) for e in data]))

def consume_messages(bucket):
    top_prices = load_prices(bucket)
    polled_prices = []
    while True:
        message_batch = consumer.poll()
        for partition_batch in message_batch.values():
            for message in partition_batch:
                price = message[6]["data"]["price"]
                event_type = message[6]["event"]
                # add price only if it bigger than the smallest saved price
                # I do not know what does price = 99999999 mean. Probably it is some trash
                if price < 100000 and event_type in ["order_created", "order_deleted"] and price > top_prices[MAX_PRICE_COUNT-1]:
                    polled_prices.append(price)

        # if something was added to polled_list, then calc max 10 values in prices
        if len(polled_prices) > 0:
            top_prices = calc_max_prices(top_prices, set(polled_prices))

            # save calculated values to GCP bucket
            save_prices(bucket, top_prices)

            print(top_prices)
            polled_prices *= 0

        # commits the latest offsets returned by poll
        consumer.commit()


if __name__ == '__main__':
    storage_client = storage.Client()

    bkt = storage.Bucket(storage_client, BUCKET_NAME)
    if not bkt.exists():
        crypto_bucket = storage_client.bucket(BUCKET_NAME)
        crypto_bucket.location = "us-east1"
        crypto_bucket.type = "Region" # create_bucket(BUCKET_NAME)
        crypto_bucket.create()
    else:
        crypto_bucket = storage_client.get_bucket(BUCKET_NAME)

    consume_messages(crypto_bucket)

