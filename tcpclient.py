from socket import *
client=socket(AF_INET,SOCK_STREAM)
client.connect(("192.168.1.104",30000))
while True:
    try:
        data=b"hello"
        client.send(data)
    except(ConnectionError):
        print("fail")