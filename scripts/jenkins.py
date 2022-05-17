#!/bin/python

import os
import sys
import getopt
import subprocess

class Args:
    def __init__(self, name, sha, dir):
        self.name = name
        self.sha = sha
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
                return
        exit(1)

def updatePKGBUILD(args: Args):
    lines = []
    with open("{}/PKGBUILD".format(args.cwd), 'r') as f:
        for line in f:
            lines.append(line)
    lines = lines[:5] + ['sha={}\n'.format(args.sha)] + lines[5:]
    with open("{}/PKGBUILD".format(args.cwd), 'w') as f:
        for line in lines:
            f.write(line)

def build(args: Args):
    commands = [['deepincn-x86_64-build', '--', '--', '-c', '-C']]
    for command in commands:
        result = subprocess.run(command, cwd=args.cwd)
        if result.returncode != 0:
            exit(result.returncode)

def main(argv):
    name = ''
    sha = ''
    dir = ''
    try:
        opts, args = getopt.getopt(argv, "hn:s:d:", ["name=", "sha=", "dir="])
    except getopt.GetoptError:
        print('jenkins.py -n <repo name> -s <sha of commit> -d <repo dir>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('jenkins.py -n <repo name> -s <sha of commit> -d <repo dir>')
            sys.exit()
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-s", "--sha"):
            sha = arg
        elif opt in ("-d", "--dir"):
            dir = os.path.abspath(arg)
    return Args(name, sha, dir)

if __name__ == "__main__":
    args = main(sys.argv[1:])
    updatePKGBUILD(args)
    build(args)
