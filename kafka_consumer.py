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
                         auto_offset_reset='latest', enable_auto_commit=False)

    total_count = 0
    partition_count = len(consumer.partitions_for_topic(topic));
    print(f'topic: {topic}, partitions: {partition_count}')
    try:
        while True:
            for m in consumer:
                msg = json.loads(m.value)
                print(msg)
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
