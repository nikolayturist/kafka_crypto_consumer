To run consumer for crypto data do following:

1. Clone git repository :
```
	git clone https://github.com/nikolayturist/kafka_crypto_consumer.git
```

2. Deploy lab3_kafka_publisher.xml NIFI template to NIFI.

3. Launch NIFI flow.

2. Change directory to repository

3. Add execution permissions to environment_create.sh

```
	chmod +x environment_create.sh
```

4. Execute environment_create.sh. It will create 'crypto_topic' kafka topic, venv, install needed packages and launch 'kafka_consumer.py'
```
	./environment_create.sh
```