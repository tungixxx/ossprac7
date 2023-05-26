# What about this script
This script is used to find vulnerabilities in ports 21 and 80

`scanner = nmap.PortScanner()` create an object of nmap port scanner

Iterates through two ports to detect their openness and adds them to the array
```Python
for i in [21, 80]:
    try:
        response = scanner.scan(ip_target, str(i))
        if response['scan'][ip_target]['tcp'][i]['state'] == "open":
            print(f"Port {i} is {response['scan'][ip_target]['tcp'][i]['state']}.")
            opened_ports.append(i)
    except:
        print("WRONG IP")
        sys.exit(0)
```


Starts find vulnerabilities on FTP. First trying to login through anonymous user if it didn't work out then starts to get more information 
about server and search exploit
```Python
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
```


Starts find directories on HTTP. 
```Python
if 80 in opened_ports:
    try:
        print("[TRYING TO CHECK DIRS IN THE WEBSITE]")
        p = subprocess.run(["gobuster", "dir", "-u", f"{ip_target}", "-w", "/usr/share/wordlists/dirb/common.txt"])
        print(p)
    except:
        print(["SOMETHING WENT WRONG"])
```
