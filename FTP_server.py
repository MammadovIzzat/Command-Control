# import socket



# HOST = "192.168.30.52"
# PORT = 6565


# server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# server.bind((HOST,PORT))
# server.listen(5)
# print(f"[*] Listening on {HOST}:{PORT}")

# client,address = server.accept()
# print(f"[*] Connected from {address[0]}:{address[1]}")

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import threading
import time
def create_ftp_server():
    authorizer = DummyAuthorizer()

    authorizer.add_user("izzat", "salam123", ".", perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer
    global server
    server = FTPServer(("0.0.0.0", 21), handler)
    thred = threading.Thread(target=server.serve_forever)
    thred.start
    time.sleep(3)
    server.close_when_done()

if __name__ == "__main__":
    create_ftp_server()
