#!/bin/python

import sys
import getopt
import subprocess


class Args:
    def __init__(self, dir, sha):
        self.dir = dir
        self.sha = sha
def updatePKGBUILD(args: Args):
    lines = []
    with open("{}/PKGBUILD".format(args.dir), 'r') as f:
        for line in f:
            lines.append(line)
    lines = lines[:5] + ['sha={}\n'.format(args.sha)] + lines[5:]
    with open("{}/PKGBUILD".format(args.dir), 'w') as f:
        for line in lines:
            f.write(line)

def build(args: Args):
    commands = [['deepincn-x86_64-build']]
    for command in commands:
        subprocess.run(command, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8", workingdir=args.dir)

def main(argv):
    dir = ''
    sha = ''
    try:
        opts, args = getopt.getopt(argv, "hd:s:", ["dir=", "sha="])
    except getopt.GetoptError:
        print('jenkins.py -d <PKGBUILD dir> -s <sha of commit>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('jenkins.py -d <PKGBUILD dir> -s <sha of commit>')
            sys.exit()
        elif opt in ("-d", "--dir"):
            dir = arg
        elif opt in ("-s", "--sha"):
            sha = arg
    return Args(dir, sha)


if __name__ == "__main__":
    args = main(sys.argv[1:])
    updatePKGBUILD(args)
    build(args)
