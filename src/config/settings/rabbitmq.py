import sys
import time

import pika

from .base import BASE_ENV


__all__ = ("RABBIT_CHANNEL", "RABBIT_CONNECTION", "RABBIT_URL")



RABBIT_URL = pika.URLParameters(BASE_ENV("RABBIT_URL"))

for _ in range(6):
    try:
        RABBIT_CONNECTION = pika.BlockingConnection(RABBIT_URL)
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
