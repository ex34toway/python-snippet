# -*- coding:utf-8 -*-
#!/bin/env python3

from kafka import KafkaProducer
import json

def idGenerator(maxSize=10):
    import random
    return random.choice(range(0,10 ** maxSize))

def senderMessageSync(producer, topic, message, encoding = 'utf-8', times = 1):
    round = 0
    while round < times:
        producer.send(topic, bytes(json.dumps(message), encoding)).get(timeout = 60)
        round = round + 1

def senderMessageAsync(producer, topic, message, encoding = 'utf-8', times = 1):
    round = 0
    while round < times:
        producer.send(topic, bytes(json.dumps(message), encoding))
        round = round + 1

if __name__ == '__main__':
    topic = 'test'
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    encoding = 'utf-8'
    content = 'i am message'
    senderMessageAsync(producer, topic, content, encoding)
    senderMessageSync(producer, topic, content, encoding)
    producer.close()
