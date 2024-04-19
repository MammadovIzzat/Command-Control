from pynput import keyboard
import sys
import threading
import time
line_buffer = ""
stop = True



def hello():
    while stop:
        global line_buffer
        sys.stdout.write("\r\u001b[1000D[hello]                                                                                   \n")
        print(line_buffer,end="",flush=True)
        time.sleep(1)
    
def keylogs():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
        

def on_press(key):
    global line_buffer
    try:
        if  key == keyboard.Key.space :
            line_buffer += " "
        elif key == keyboard.Key.backspace:
            line_buffer = line_buffer [:-1]
        else:
            key_char = key.char
            line_buffer += key_char
    except AttributeError as e:
        pass
    
def on_release(key):
    global line_buffer
    if key == keyboard.Key.enter:
        line_buffer = ""  
    if not stop :
        return False  
    
    
helloo = threading.Thread(target=hello)
helloo.start()
keylog = threading.Thread(target=keylogs)
keylog.start()

sa = input()
print(f'your input is :{sa}')
stop = False