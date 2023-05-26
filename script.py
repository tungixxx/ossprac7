import nmap
import ftplib
import subprocess
from ftplib import FTP
from termcolor import colored
import sys

ip_target = input("IP: ")
scanner = nmap.PortScanner()
opened_ports = []

for i in [21, 80]:
    try:
        response = scanner.scan(ip_target, str(i))
        if response['scan'][ip_target]['tcp'][i]['state'] == "open":
            print(f"Port {i} is {response['scan'][ip_target]['tcp'][i]['state']}.")
            opened_ports.append(i)
    except:
        print("WRONG IP")
        sys.exit(0)

if 21 in opened_ports:
    try:
        print("[TRYING TO CONNECT FTP SERVER THROUGH ANONYMOUS USER]")
        ftp = ftplib.FTP(ip_target, "anonymous", "")
        if ftp.getwelcome()[0:3] == "220":
            print("[ANONYMOUS FTP LOGIN ALLOWED]")
    except:
        print("[ANONYMOUS FTP LOGIN NOT ALLOWED]")
    try:
        conn=FTP(ip_target)
        ftp=conn.getwelcome()
        if ftp[4:11] == "ProFTPD":
            print(colored("[THIS FTP USES PROFTPD SERVER]", 'red'))
            print(colored(f"[YOU CAN FIND EXPLOIT IN https://www.exploit-db.com/search?q=ProFTPd+{ftp[12:17]}]", 'red'))
    except:
        print("")

if 80 in opened_ports:
    try:
        print("[TRYING TO CHECK DIRS IN THE WEBSITE]")
        p = subprocess.run(["gobuster", "dir", "-u", f"{ip_target}", "-w", "/usr/share/wordlists/dirb/common.txt"])
        print(p)
    except:
        print(["SOMETHING WENT WRONG"])
