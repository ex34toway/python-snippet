from socket import *
import json


host = '127.0.0.1'
port = 5148

times = 1

def syslog():
    ip_port = (host, port)
    client_socket = socket(AF_INET, SOCK_DGRAM)
    # client_socket.sendto(bytes('<178>DBAppWAF: 发生时间/2011-09-29 16:40:39,威胁/高,事件/木马,URL地址/192.168.25.116/scripts/root.exe?/c+dir,POST数据/,服务器IP/192.168.25.116,主机名/192.168.25.116,服务器端口/80,客户端IP/192.168.10.211,客户端端口/3048,客户端环境/Mozilla/4.0 (compatible; MSIE 6.0; Win32),标签/木马,动作/告警,HTTP/S响应码/404,攻击特征串/root.exe,触发规则/15010003,访问唯一编号/ToQvB38AAAEAAFOG550AAA3Q', encoding = 'utf-8'), ip_port)
    with open(file=r'c:\\Users\\liliang\\Desktop\\datadd', mode='r', encoding='utf-8') as f:
        msg = f.read()
    msb_bytes = bytes(msg, 'utf-8')
    print(msg)
    for i in range(0, times):
        client_socket.sendto(msb_bytes, ip_port)
        if i % 10000 == 0:
            print(i)
    

if __name__ == '__main__':
    syslog()
