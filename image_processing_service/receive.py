import os
import sys
import time

import pika
from dotenv import load_dotenv

from core import add_new_file_data

load_dotenv()


def main():
    credentials = pika.PlainCredentials(
        os.environ.get("RABBITMQ_DEFAULT_USER"),
        os.environ.get("RABBITMQ_DEFAULT_PASS"),
    )

    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters("rabbitmq", 5672, "/", credentials)
            )
            break
        except pika.exceptions.AMQPConnectionError:
            time.sleep(5)

    channel = connection.channel()
    channel.queue_declare(queue="add_images")

    channel.basic_consume(
        queue="add_images", on_message_callback=add_new_file_data, auto_ack=True
    )

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
