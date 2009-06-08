#!/usr/bin/python
import sys
import os
import shutil

WEAVER_DIR = os.path.dirname(os.path.abspath(__file__))

def init(args):
    target_dir = args[0]
    try:
        os.mkdir(target_dir)
    except OSError:
        print 'Cannot start project. A project with that name (%s) appears to already exist.' % target_dir
        sys.exit(1)
    else:
        shutil.copy(
            os.path.join(WEAVER_DIR, 'settings.py.tmpl'), 
            os.path.join(target_dir, 'settings.py')
        )

if __name__ == '__main__':
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    commands[cmd](args)