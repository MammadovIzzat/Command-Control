import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Provided AES key
aes_key = b'o\x802\x0ez\xe0\x8f\x8b\xc7>\xbf\x9fce\x85\xd3'

# Encrypt data using AES
def encrypt_data(data):
    cipher = AES.new(aes_key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv + ciphertext

# Decrypt data using AES
def decrypt_data(encrypted_data):
    iv = encrypted_data[:AES.block_size]
    ciphertext = encrypted_data[AES.block_size:]
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_data

# Server code
def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)

    print("Server listening...")
    conn, addr = server_socket.accept()
    print("Connected to", addr)

    # Encrypt and send data
    data_to_encrypt = b"Hello, client! This is a secret message."
    encrypted_data = encrypt_data(data_to_encrypt)
    conn.sendall(encrypted_data)

    conn.close()
    server_socket.close()

# Client code
def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    # Receive encrypted data
    encrypted_data = client_socket.recv(1024)

    # Decrypt data
    decrypted_data = decrypt_data(encrypted_data)
    print("Received message from server:", decrypted_data.decode())

    client_socket.close()

if __name__ == "__main__":
    server()
