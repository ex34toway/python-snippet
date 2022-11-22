# -*- coding:utf-8 -*-
#!/bin/env python3

from pysnmp.hlapi import *
from pyasn1.type import univ

iterator = sendNotification(
    SnmpEngine(),
    UsmUserData('testuser', authKey='authenticationkey'),
    UdpTransportTarget(('127.0.0.1', 162)),
    ContextData(),
    'inform',
    NotificationType(
        ObjectIdentity('1.3.6.1.6.3.1.1.5.2')
    ).addVarBinds(
         ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0'), 'system name')
    ).loadMibs(
        'SNMPv2-MIB'
    )
)

errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

if errorIndication:
    print(errorIndication)

elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))
