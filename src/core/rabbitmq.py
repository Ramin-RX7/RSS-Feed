import json

import pika

from config.settings import RABBIT_URL




def publish_podcast_update(data):
    return RabbitMQ.publish_s("podcast_update", data)




class RabbitMQ:
    """
    Context manager to use rabbitmq message broker.

    self.ch -> rabbit channel
    self.con -> rabbit connection
    self.properties -> publish properties
    context manager return -> self
    """
    def __init__(self, *args, **kwargs):
        self.con = pika.BlockingConnection(RABBIT_URL)
        self.ch = self.con.channel()
        self.properties = pika.BasicProperties("...")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.ch.close()
        self.con.close()
        return True

    def publish(self, queue, data):
        self.ch.basic_publish(exchange="", routing_key=queue, body=json.dumps(data), properties=self.properties)


    @staticmethod
    def publish_s(queue, data):
        con = pika.BlockingConnection(RABBIT_URL)
        properties = pika.BasicProperties("...")
        ch = con.channel()
        ch.basic_publish(exchange='', routing_key=queue, body=json.dumps(data), properties=properties)
        ch.close()
        con.close()
