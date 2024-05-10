import rsa
import socket

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes

host = "192.168.30.52"
port = 8888

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen(3)
client, address = server.accept()




rsa_pub = rsa.PublicKey.load_pkcs1(client.recv(4096),"PEM")
aes_key = get_random_bytes(AES.block_size)
print(aes_key)
print(rsa_pub)
print(rsa.encrypt(aes_key,rsa_pub))
client.send(rsa.encrypt(aes_key,rsa_pub))
