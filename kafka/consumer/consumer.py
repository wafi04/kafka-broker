from confluent_kafka import Consumer
import json

def create_consumer(group_id='my-group'):
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    }
    return Consumer(conf)

def consume_messages(topic):
    consumer = create_consumer()
    consumer.subscribe([topic])
    
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            try:
                message = json.loads(msg.value().decode('utf-8'))
                print(f'Received message: {message}')
            except Exception as e:
                print(f"Error processing message: {e}")
                
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        consumer.close()
