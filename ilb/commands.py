import json
import time


def data_read():
    try:
        with open('.././Data/client_list.json') as f:
            global data 
            data = json.load(f)
        time.sleep(1)
    except:
        print("[*] There is a problem in JSON data.")

