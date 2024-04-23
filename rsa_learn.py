import socket
import ssl
import random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def generate_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def generate_symmetric_key():
    # Generating a random 16-byte symmetric key (128 bits)
    return bytes([random.randint(0, 255) for _ in range(16)])

def server():
    private_key, server_public_key = generate_key_pair()
    sym_key = None
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 7878))
        s.listen(1)
        print("Server listening on port 7878...")
        
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            
            # Send server's public key
            conn.sendall(server_public_key)
            
            # Receive encrypted symmetric key
            encrypted_sym_key = conn.recv(2048)
            rsa_private_key = RSA.import_key(private_key)
            cipher_rsa = PKCS1_OAEP.new(rsa_private_key)
            sym_key = cipher_rsa.decrypt(encrypted_sym_key)
            
            print("Symmetric key received and decrypted by server:", sym_key)
            
            # Send encrypted secret data
            secret_data = b"Hello, client! This is a secret message."
            cipher_sym = AES.new(sym_key, AES.MODE_CBC)
            padded_data = pad(secret_data, AES.block_size)
            ciphertext = cipher_sym.encrypt(padded_data)
            conn.sendall(ciphertext)
            print("Secret data sent to client.")

if __name__ == "__main__":
    server()
