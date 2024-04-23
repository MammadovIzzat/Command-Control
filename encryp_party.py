import socket
import ssl
import random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def generate_symmetric_key():
    # Generating a random 16-byte symmetric key (128 bits)
    return bytes([random.randint(0, 255) for _ in range(16)])

def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 7878))
        
        # Receive server's public key
        server_public_key = s.recv(2048)
        
        # Generate symmetric key
        sym_key = generate_symmetric_key()
        
        # Encrypt symmetric key with server's public key
        rsa_public_key = RSA.import_key(server_public_key)
        cipher_rsa = PKCS1_OAEP.new(rsa_public_key)
        encrypted_sym_key = cipher_rsa.encrypt(sym_key)
        
        # Send encrypted symmetric key to server
        s.sendall(encrypted_sym_key)
        
        print("Symmetric key generated and sent by client:", sym_key)
        
        # Receive encrypted secret data
        ciphertext = s.recv(2048)
        cipher_sym = AES.new(sym_key, AES.MODE_CBC)
        decrypted_data = unpad(cipher_sym.decrypt(ciphertext), AES.block_size)
        print("Decrypted secret data received from server:", decrypted_data.decode('utf-8', 'ignore'))



if __name__ == "__main__":
    client()
