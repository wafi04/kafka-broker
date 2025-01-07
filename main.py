from consumer import *
from database.database  import create_table
import time
from producer import *

def main():
    producer = create_producer()
    topic_name="kafka"
    message = {
            "message": "hello kafka",
            "timestamp": str(time.time())
    }
    produce_message(producer, topic_name, message)
    consume_messages(topic_name)

main()