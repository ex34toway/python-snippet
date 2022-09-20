# -*- coding:utf-8 -*-
#!/bin/env python3

from kafka import KafkaConsumer
import json

if __name__ == '__main__':
    topic = 'test'
    groupId = 'consumer.test'
    consumer = KafkaConsumer(topic,
                         group_id=groupId,
                         bootstrap_servers=['localhost:9092'],
                         auto_offset_reset='earliest', enable_auto_commit=False)

    total_count = 0
    print(consumer.partitions_for_topic(topic))
    try:
        while True:
            msg = consumer.poll(timeout_ms = 1000)
            print(msg)
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
