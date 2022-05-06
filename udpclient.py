import socket

client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
ip="192.168.1.104"
port=30000
Message=b"hello"
while True:
    try:
        client.sendto(Message,(ip,port))
    except(ConnectionError):
        print("fail")