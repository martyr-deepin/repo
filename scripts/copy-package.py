#!/bin/python

import os
import sys
import getopt
import subprocess
import shutil

class Struct:
    def __init__(self, name, db, dir):
        self.name = name
        self.db = db
        self.dir = dir
        self.cwd = ''
        for file in os.listdir(dir):
            with open(os.path.join(dir, "{}/{}".format(file, 'PKGBUILD')), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if not line.startswith('url') and not line.startswith('URL'):
                        continue
                    if 'github.com/linuxdeepin/{}'.format(name) in line:
                        self.cwd = os.path.join(dir, file)
                        break
            if len(self.cwd) != 0:
                break

def main(argv):
    name = ''
    db = ''
    dir = ''
    try:
        opts, args = getopt.getopt(argv, "hn:b:d:", ["name=", "db=", "dir="])
    except getopt.GetoptError:
        print('copy-package.py -n <repo name> -b <db path> -d <repo dir>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('copy-package.py -n <repo name> -b <db path> -d <repo dir>')
            sys.exit()
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-b", "--db"):
            db = arg
        elif opt in ("-d", "--dir"):
            dir = os.path.abspath(arg)
    return Struct(name, db, dir)

def copy(struct: Struct):
    for file in os.listdir(struct.cwd):
        if not file.endswith('.zst'):
            continue
        file_path = os.path.join(struct.cwd, file)
        cmd = subprocess.run(['gpg', '--detach-sign', file_path], cwd=struct.cwd)
        if cmd.returncode != 0:
            os.exit(-1)
        shutil.copyfile(file_path, os.path.join(struct.db, file))
        cmd = subprocess.run(['repo-add', '-R', 'deepincn.db.tar.xz', file], cwd=struct.db)
        if cmd.returncode != 0:
            os.remove("{}/{}".format(struct.db, file))
        else:
            shutil.copyfile("{}.sig".format(file_path), os.path.join(struct.db, '{}.sig'.format(file)))

if __name__ == "__main__":
    struct = main(sys.argv[1:])
    if not os.path.exists(struct.db):
        os.mkdir(struct.db)
    copy(struct)