import socket


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



file = 'a.jpg'
file_data = read(file)
parse_file = parse_chunks(file_data)



HOST = "127.0.0.1"
PORT = 6767


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen(5)


client, address = server.accept()
print(str(len(parse_file)),parse_file)
client.send(str(len(parse_file)).encode('utf-8'))
client.recv(4096)
for chunk in parse_file:
    client.send(chunk)
