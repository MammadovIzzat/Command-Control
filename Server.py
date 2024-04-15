import socket
import threading
import csv

Host = "127.0.0.1"
Port = 6565
csv_data = "./Data/client_list.csv"
client_list=[]
with open(csv_data, 'r') as data:
  for line in csv.DictReader(data):
      client_list.append(line)



# def status():
   

# def start():


# def stop():


# def ftp():


# def log():


# def connect():


# def help():








if __name__ == "__main__":
    
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((Host,Port))
    server.listen(10)
    
