import json

import pika

from config.settings import RABBIT_CHANNEL



def publish(queue, method, body):
    properties = pika.BasicProperties(method)
    RABBIT_CHANNEL.basic_publish(exchange='', routing_key=queue, body=json.dumps(body), properties=properties)


def publish_podcast_update(data):
    return publish("podcast_update", "...", data)
