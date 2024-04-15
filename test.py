import os
import subprocess

while 1:
    command = input().split(" ")
    if command[0] == "cd":
        try:
            os.chdir(command[1])
        except FileNotFoundError as er:
            print(er)
    else :
        command.insert(0,"powershell.exe")
        output = subprocess.getoutput(command)
        output = f"{output}\n{os.getcwd()}->"
        print(output)