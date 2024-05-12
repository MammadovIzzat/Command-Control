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

## Troubleshooting tips
Try to not rush for using commands, it can be drop connection, sometime ftp can give error or you can breake connection with keyboard interuption, then try to stop client, wait for max timer time then again start, it recover client connections. You can decrease timer but it can increase detection rate on network.