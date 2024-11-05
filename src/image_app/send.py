import base64
import json
import os

import pika
from dotenv import load_dotenv

load_dotenv()


def send_message(body: dict) -> None:
    credentials = pika.PlainCredentials(
        os.environ.get("RABBITMQ_DEFAULT_USER"),
        os.environ.get("RABBITMQ_DEFAULT_PASS"),
    )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("rabbitmq", 5672, "/", credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue="add_images")

    body["src_file"] = (base64.b64encode(body["src_file"]).decode("utf-8"),)
    message = json.dumps(body)

    channel.basic_publish(exchange="", routing_key="add_images", body=message)
    connection.close()
