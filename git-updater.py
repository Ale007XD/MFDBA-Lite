#!/usr/bin/env python3
import subprocess
import sys
import os
from datetime import datetime

def git(cmd):
    r = subprocess.run(['git'] + cmd.split(), capture_output=True, text=True)
    if r.returncode:
        sys.exit(1)
    return r.stdout.strip()

def main():
    s = git('status --porcelain')
    if not s:
        print('No changes')
        return
    
    m = []
    n = []
    for l in s.splitlines():
        if l:
            st = l[0]
            f = l[2:]
            if st in 'MA':
                m.append(f)
            if st == '?':
                n.append(f)
    
    ts = datetime.now().strftime('%H:%M %d.%m')
    msg = 'MFDBA Update ' + ts
    if m:
        msg += '\nMod: ' + ','.join(m[:3])
    if n:
        msg += '\nNew: ' + ','.join(n[:2])
    
    print('Commit:\n' + msg)
    if input('Push y/n? ').lower() != 'y':
        return
    
    os.system('git add .')
    os.system('git commit -m "' + msg + '"')
    os.system('git push')
    print('Done!')

if __name__ == '__main__':
    main()
