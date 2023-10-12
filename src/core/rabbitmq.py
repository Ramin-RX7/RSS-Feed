import json

import pika

from config.settings import RABBIT_CHANNEL,RABBIT_CONNECTION



def publish(queue, method, body):
    properties = pika.BasicProperties(method)
    ch = RABBIT_CONNECTION.channel()
    ch.basic_publish(exchange='', routing_key=queue, body=json.dumps(body), properties=properties)
    ch.close()

def publish_podcast_update(data):
    return publish("podcast_update", "...", data)
