# -*- coding:utf-8 -*-
#!/bin/env python3

from kafka import KafkaProducer
import json
import time

time_diff = 0.02

def idGenerator(maxSize=10):
    import random
    return random.choice(range(0,10 ** maxSize))

def senderMessageSync(producer, topic, message, times = 1):
    round = 0
    while round < times:
        message['eventId'] = idGenerator()
        d = producer.send(topic, bytes(json.dumps(message), 'utf-8')).get(timeout = 60)
        time.sleep(time_diff)
        round = round + 1

def senderMessageAsync(producer, topic, message, times = 1):
    round = 0
    while round < times:
        message['eventId'] = idGenerator()
        producer.send(topic, bytes(json.dumps(message), 'utf-8'))
        round = round + 1

if __name__ == '__main__':
    # topic = 'infrastructure.event'
    topic = 'dragonfly.event.mapped'
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    e1 = {
'__eventPattern': 'E1',
'srcAddress': '192.168.30.11',
'srcPort': 54564,
'destAddress': '192.168.30.80',
'destPort': 8080,
'destUserName': 'test',
'catTechnique': '',
'catBehavior': '/Authentication/Verify',
'catOutcome': 'FAIL',
'deviceCat': '/IDS/Host'
}
    e2 = {
'__eventPattern': 'E2',
'srcAddress': '192.168.30.11',
'srcPort': 54564,
'destAddress': '192.168.30.80',
'destPort': 8080,
'destUserName': 'test',
'catTechnique': '',
'catBehavior': '/Authentication/Verify',
'catOutcome': 'Ok',
'deviceCat': '/IDS/Host'
}
    e3 = {
'__eventPattern': 'E3',
'srcAddress': '192.168.30.11',
'srcPort': 54564,
'destAddress': '192.168.30.80',
'destPort': 8080,
'destUserName': 'test',
'catTechnique': '/Exploit/PrivilegeEscalation',
'catBehavior': '',
'catOutcome': 'Ok',
'deviceCat': '/IDS/Host'
}

    te = {
  "srcUserName": "admin",
  "destAddress": "192.168.30.80",
  "catTechnique": "/Exploit/PrivilegeEscalation",
  "appProtocol": "/IDS/Host",
  "catBehavior": "/Authentication/Verify",
  "srcAddress": "192.168.30.11",
  "srcPort": 54564,
  "destUserName": "test",
  "deviceName": "暴力破解测试",
  "catOutcome": "FAIL",
  "deviceId": "1234"
}

    ut = {
  "deviceProtocol": "fileUpload",
  "assetId": "1",
  "srcAddress": "127.0.0.1",
  "receiverName": "agent",
  "rawEvent": "<178>DBAppWAF: 发生时间/2011-09-29 16:40:39,威胁/高,事件/木马,URL地址/192.168.25.116/scripts/root.exe?/c+dir,POST数据/,服务器IP/192.168.25.116,主机名/192.168.25.116,服务器端口/80,客户端IP/192.168.10.211,客户端端口/3048,客户端环境/Mozilla/4.0 (compatible; MSIE 6.0; Win32),标签/木马,动作/告警,HTTP/S响应码/404,攻击特征串/root.exe,触发规则/15010003,访问唯一编号/ToQvB38AAAEAAFOG550AAA3Q",
  "collectorReceiptTime": int(time.time() * 1000+0.5)
}
    us = {"deviceProtocol":"fileUpload","eventId":0,"mapperId":"da564fd1-5800-41a9-9f5c-ffe31055e343","elapsedNS":151396,"metricTime":1643115288136,"dataMap":{"802269aa-cea5-49da-b028-7af51c6b874e":{"elapsedMS":2257,"order":1},"f27e16f6-308e-4fd7-a8cb-777428bcab15":{"elapsedMS":788,"order":28},"c42ee713-de12-4677-ac34-154a823527a8":{"elapsedMS":800,"order":20},"e07f7b1a-3b9d-4292-a410-ef374b421aa0":{"elapsedMS":232,"order":8},"cd927d27-0094-4a95-8035-ce7d97346bdf":{"elapsedMS":3312,"order":27},"336579da-f7c8-4ae6-8323-2dacedb5cb8e":{"elapsedMS":165,"order":10},"7f6f7205-4568-4143-9c75-b29bd37d3afb":{"elapsedMS":4838,"order":17},"17510134-e70f-4361-b5a0-313e1b8490a1":{"elapsedMS":282,"order":30},"ce67451b-c56f-4780-938b-1fcb757253ee":{"elapsedMS":865,"order":11},"765d6b42-085b-46fc-9314-e6a9c5da7947":{"elapsedMS":19072,"order":23},"085dbb97-b153-4df9-acf0-56a592492b3d":{"elapsedMS":648,"order":19},"1df506df-e438-4ac1-b65e-dd25e5155db0":{"elapsedMS":1428,"order":12},"9d0eee70-a4e0-4f7d-b1a4-e81b7cd36220":{"elapsedMS":790,"order":14},"da7cbf96-5daf-4c64-8b45-e1085ed9ca26":{"elapsedMS":3669,"order":25},"c14cc631-41cd-4078-8281-1bc7fb350a6c":{"elapsedMS":503,"order":29},"38b530fc-c546-4e31-a9a4-a140b8b5cde4":{"elapsedMS":35935,"order":13},"88e6496c-6710-49ad-91e1-2e0f5c93d18b":{"elapsedMS":1612,"order":22},"97938f8b-54fc-4a92-be63-0865477f4790":{"elapsedMS":4122,"order":21},"adca2710-ce87-4fc6-b332-15f423e689fc":{"elapsedMS":3109,"order":6},"653bd894-7058-498f-9984-e21b2865cd39":{"elapsedMS":1049,"order":3},"29e85e1c-3529-4b73-916c-b5188b4c61a6":{"elapsedMS":4006,"order":26},"ac1e7dcb-8ad0-4ef9-8a36-f2e196a7a0af":{"elapsedMS":2705,"order":31},"90b816f2-eacc-4e95-ad23-11b4cce174ba":{"elapsedMS":873,"order":18},"039b9a22-6f45-4a1a-a6e0-46e3b61d5513":{"elapsedMS":4673,"order":24}}}

    times = 100_000_000
    round = 0
    ut["rawEvent"] = "<22>Sep  9 07:31:01 erd postfix/cleanup[15789]: 8BE535FA28E: message-id=<20130908160023.8BE535FA28E@erd.ydc.sgcc.com.cn>"
    senderMessageAsync(producer, topic, ut, 1)

    nt = {
        "messageId": "1",
        "dataType": "mapper",
        "messageType": "messageTypeDataUpdate",
        "messages": '[{"dataId":"-1","dataMap":null}]'
    }
    # senderMessageAsync(producer, "infrastructure.message", nt, 1)
    producer.close()
