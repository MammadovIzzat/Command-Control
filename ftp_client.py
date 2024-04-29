import socket

HOST = "127.0.0.1"
PORT = 6767

def write(file,data):
    with open(file,'wb') as f:
        f.write(data)

file = "b.jpg"


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST,PORT))

size = int(client.recv(4096).decode('utf-8'))
data = []
client.send(b"ready")
for i in range(size):
    chunk = client.recv(409600)
    data.append(chunk)
binary_data = b''.join(data)  
write(file,binary_data)

