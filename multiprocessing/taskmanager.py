# -*- coding:utf-8 -*-

from multiprocessing.managers import BaseManager
import queue
import random


# 发送任务的队列
task_queue = queue.Queue()
# 接收结果的队列
result_queue = queue.Queue()


def get_task_queue():
    return task_queue


def get_result_queue():
    return result_queue


class QueueManager(BaseManager):
    pass


def distributed_task():
    # 把两个queue注册到网络上
    QueueManager.register('get_task_queue', callable=get_task_queue)
    QueueManager.register('get_result_queue', callable=get_result_queue)
    # 绑定端口5000，设置验证码abc
    manager = QueueManager(address=('127.0.0.1', 5000), authkey=bytes("abc".encode('utf-8')))
    manager.start()
    # 通过网络访问Queue对象
    task = manager.get_task_queue()
    result = manager.get_result_queue()

    # 添加待处理任务
    for i in range(10):
        n = random.randint(0, 10000)
        print('Put task %d ...' % n)
        task.put(n)

    # 从result队列读取结果
    print('Try get results...')
    for i in range(10):
        r = result.get(timeout=10)
        print('Result: %s ' % r)

    # 关闭
    manager.shutdown()


if __name__ == '__main__':
    distributed_task()
