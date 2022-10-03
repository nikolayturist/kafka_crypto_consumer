#!/bin/bash

echo "-----------------------------------------------------------"
echo "Create topic crypto_order"
echo "-----------------------------------------------------------"
/usr/lib/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 2 --partitions 3 --topic crypto_topic

echo "-----------------------------------------------------------"
echo "Configure consumer"
echo "-----------------------------------------------------------"

sudo apt install virtualenv

virtualenv -p /usr/bin/python3 venv
source venv/bin/activate

pip install kafka-python
pip install gcloud
pip install google-cloud-storage
pip install google-api-python-client

python kafka_consumer.py