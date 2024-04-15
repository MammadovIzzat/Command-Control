import subprocess

command = ""
try:
    if command.split()[0] == "cd":
        print("sa")
except:
    True
stdout = subprocess.check_output(["powershell", "-Command",command])
if stdout :
    print(stdout.decode("utf-8"))
else :
    print("as")