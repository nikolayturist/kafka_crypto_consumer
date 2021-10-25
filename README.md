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