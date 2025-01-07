from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException
import json

def create_producer():
    conf = {
        'bootstrap.servers': 'localhost:9092'
    }
    return Producer(conf)

def produce_message(producer, topic, message):
    try:
        message_bytes = json.dumps(message).encode('utf-8')
        producer.produce(topic=topic, value=message_bytes)
        producer.flush()
        print(f"Message sent successfully: {message}")
    except Exception as e:
        print(f"Error sending message: {e}")

def create_topic_confluent(topic_name, num_partitions=1, replication_factor=1):
    """
        CREATE TOPIC NAME
    """

    conf = {
        'bootstrap.servers': 'localhost:9092'
    }

    try:
        admin =   AdminClient(conf)  # created admin client
        # admin topice activate
        topic = NewTopic(  
            topic_name,
            num_partitions=num_partitions,
            replication_factor=replication_factor
        )
        futures =  admin.create_topics([topic])
        for topic, future in futures.items():
            try:
                future.result()
                print(f"Topic {topic} created successfully")
            except KafkaException as e:
                print(f"Error creating topic {topic}: {e}")
    except Exception as e:
        print(f"Error creating topic: {e}")
    