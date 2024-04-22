from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
import threading
import logging
import time

def create_ftp_server():
    authorizer = DummyAuthorizer()
    authorizer.add_user("izzat", "salam123", "./Data/ftp", perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer
    
    # Set the logging level to suppress logging to the console
    logger = logging.getLogger("pyftpdlib")
    logger.setLevel(logging.WARNING)

    server = ThreadedFTPServer(("0.0.0.0", 21), handler)
    server.serve_forever()

if __name__ == "__main__":
    # Configure the root logger to suppress all messages
    logging.basicConfig(level=logging.CRITICAL)
    
    thred = threading.Thread(target=create_ftp_server, daemon=True, name="FTP")
    thred.start()
    time.sleep(1)
    sa = input("in >")
    print(sa)
