import socket
import base64

ip = "127.0.0.1"
port = 20001
bufferSize  = 1024 * 64
serverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
serverSocket.bind((ip, port))
while(True):
    bytesAddressPair = serverSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    print(f"address: {address},message: {base64.b64encode(message)}")
