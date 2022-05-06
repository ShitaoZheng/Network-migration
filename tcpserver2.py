import socket
def recdata(ip,port):
    serverSock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSock.bind((ip,port))
    serverSock.listen()
    client, addr=serverSock.accept()
    while True:
        data=client.recv(1024)
        print("message:",data)

if __name__=="__main__":
    ip="192.168.1.103"
    port=30001
    recdata(ip,port)