from socket import *


host = '192.168.30.227'
port = 514
times = 100_000_000

def main():
    ip_port = (host, port)
    client_socket = socket(AF_INET, SOCK_DGRAM)
    with open(file=r'/root/syslog/all.txt', mode='r', encoding='utf-8') as file:
        for line in file:
            line = line.lstrip()
            if len(line) > 0:
                client_socket.sendto(line.encode(), ip_port)

if __name__ == '__main__':
    main()
