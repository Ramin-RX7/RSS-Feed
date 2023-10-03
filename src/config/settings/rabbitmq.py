import sys
import time

import pika

__all__ = ("RABBIT_CHANNEL", "RABBIT_CONNECTION")


params = pika.URLParameters('amqp://rabbit:5672')

for _ in range(6):
    try:
        RABBIT_CONNECTION = pika.BlockingConnection(params)
    except pika.exceptions.AMQPConnectionError as e:
        print("RabbitMQ is not up yet. sleeping for 2.5 second")
        time.sleep(2.5)
    else:
        print("Connected to RabbitMQ service succesfully")
        break
else:
    sys.stderr.write("Could not connect to rabbitmq server")
    sys.exit(1)

RABBIT_CHANNEL = RABBIT_CONNECTION.channel()
