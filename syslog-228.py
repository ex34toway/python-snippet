from socket import *


host = '192.168.30.228'
port = 514
times = 100

def main():
    ip_port = (host, port)
    client_socket = socket(AF_INET, SOCK_DGRAM)
    with open(file=r'/root/syslog/log.txt', mode='r', encoding='utf-8') as f:
        log_lines = f.readlines()
    f.close()
    for i in range(0, times):
        for log_line in log_lines:
            client_socket.sendto(log_line.encode(), ip_port)
        if i % 10000 == 0:
            print(i)

if __name__ == '__main__':
    main()
