Simple Kafka message consumer for Crypto data.
To run it:
1. Login to master node and create topics:

    `cd /usr/lib/kafka/bin/
    ./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 2 --partitions 3 --topic crypto_order_created
    ./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 2 --partitions 3 --topic crypto_order_deleted`
    
    check if topics created:
    
    `./kafka-topics.sh --list --zookeeper localhost:2181`
    
2. Deploy NIFI flow from big_data_lab3_kafka.xml template
3. Run NIFI flow
4. Install kafka for python with following command:
    
    `sudo pip install kafka`
    
5. Run message consumer with following command:

    `sudo python python_consumer.py -t crypto_order_created -s localhost:9092 -c 100 -g group1`
    
Script writes in STDOUT top 10 prices: see sample of output:

`[62884.9, 62816.36, 62816.36, 62815.86, 62815.46, 62814.56, 62811.75, 62808.35, 62807.82, 62807.08]
[62886.29, 62884.9, 62829.35, 62824.99, 62816.36, 62816.36, 62816.36, 62816.36, 62816.36, 62816.16]
[62886.29, 62884.9, 62829.35, 62824.99, 62816.36, 62816.36, 62816.36, 62816.36, 62816.36, 62816.16]
[62892.4, 62886.29, 62884.9, 62829.35, 62824.99, 62816.36, 62816.36, 62816.36, 62816.36, 62816.36]
[62892.4, 62886.29, 62884.9, 62829.35, 62824.99, 62816.36, 62816.36, 62816.36, 62816.36, 62816.36]  ` 