import rsa
import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes

host = "192.168.30.52"
port = 8888

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))






(publickey, privatekey) = rsa.newkeys(1024)
print(publickey.save_pkcs1("PEM"))
client.send(publickey.save_pkcs1("PEM"))
print("key sended")
aes_key = rsa.decrypt(client.recv(4096),privatekey)
print(aes_key)