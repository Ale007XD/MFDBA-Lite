#!/usr/bin/env python3
import subprocess
import sys
from datetime import datetime

def git(cmd):
    r = subprocess.run(['git'] + cmd.split(), capture_output=True, text=True)
    if r.returncode:
        print(f"Git error: {r.stderr}")
        sys.exit(1)
    return r.stdout.strip()

def main():
    s = git('status --porcelain')
    if not s:
        print('No changes')
        return
    
    modified = []
    new = []
    for line in s.splitlines():
        if line:
            status = line[0]
            filename = line[2:]
            if status in 'MA':
                modified.append(filename)
            if status == '?':
                new.append(filename)
    
    ts = datetime.now().strftime('%H:%M %d.%m')
    msg = 'MFDBA Update ' + ts
    if modified:
        msg += '\nMod: ' + ','.join(modified[:3])
    if new:
        msg += '\nNew: ' + ','.join(new[:2])
    
    print('Commit:\n' + msg)
    if input('Push y/n? ').lower() != 'y':
        return
    
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', msg], check=True)
    subprocess.run(['git', 'push'], check=True)
    print('Done!')

if __name__ == '__main__':
    main()
