#!/bin/python

import sys
import getopt
import subprocess


class Args:
    dir = ''
    sha = ''

def updatePKGBUILD(args: Args):
    lines = []
    with open("{}/PKGBUILD".format(args.dir), 'r') as f:
        for line in f:
            lines.append(line)
    lines.insert(5, 'sha={}'.format(args.sha))
    with open("{}/PKGBUILD".format(args.dir), 'w') as f:
        f.write(lines)

def build(args: Args):
    commands = [['deepincn-x86_64-build']]
    for command in commands:
        subprocess.run(command, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8", workingdir=args.dir)

def main(argv):
    args: Args = Args()
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
            args.dir = arg
        elif opt in ("-s", "--sha"):
            args.sha = arg
    return args


if __name__ == "__main__":
    args = main(sys.argv[1:])
    updatePKGBUILD(args)
    build(args)
