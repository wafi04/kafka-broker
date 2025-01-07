from producer import create_producer, produce_message
import time

if __name__ == "__main__":
    topic_name = "kafka"
    producer = create_producer()
    message =  input("Masukkan Message ke Kafka : ")
    
    message = {
        "message": message,
        "timestamp": str(time.time())
    }
    
    produce_message(producer, topic_name, message)