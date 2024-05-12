# ASLANAT

Aslanat is Command and Control server.

## Installation

Use the package manager pip to install requested libraries.

```bash
pip install pycryptodome
pip install rsa
pip install tabulate
```

## Usage
Change Host as your IP address (if you want to work on each device in internet, use public IP address) on srv.py and cli.py, then client connect server each time you set clients status True ( use start and stop commands). If you run client first time it auto connect server and add itself to list and for protect from network detections, you can increase timer on client code ( default 20-200 second randomly). It effect client connection time. Such commands need Nickname for using, that's why try to give special Nickname for each clients. You can use ftp command for upload (-u) and download (-d) files from server to client in connection, and also list (-l) for check ftp file for unloadable files. HF.
