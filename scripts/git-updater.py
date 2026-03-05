#!/usr/bin/env python3
import subprocess
import sys
import os
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
    # Сообщение для коммита (однострочное)
    msg = f'MFDBA Update {ts}'
    if m:
        msg += f' | Mod: {",".join(m[:3])}'
    if n:
        msg += f' | New: {",".join(n[:2])}'
    
    # Красивый вывод с переносами
    print('\nCommit message:')
    print(msg.replace(' | ', '\n'))
    
    if input('\nPush y/n? ').lower() != 'y':
        return
    
    # Используем subprocess вместо os.system
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', msg], check=True)
    subprocess.run(['git', 'push'], check=True)
    print('Done!')

if __name__ == '__main__':
    main()
