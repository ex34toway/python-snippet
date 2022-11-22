# -*- coding:utf-8 -*-
#!/bin/env python3

from pysnmp.hlapi import *

iterator = sendNotification(
    SnmpEngine(),
    CommunityData('public'),
    UdpTransportTarget(('127.0.0.1', 162)),
    ContextData(),
    'trap',
    NotificationType(
        ObjectIdentity('IF-MIB', 'linkUp'),
        instanceIndex=(123,),
        objects={
            ('IF-MIB', 'ifIndex'): 123,
            ('IF-MIB', 'ifAdminStatus'): 'up',
            ('IF-MIB', 'ifOperStatus'): 'up'
        }
    )
)

errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

if errorIndication:
    print(errorIndication)
