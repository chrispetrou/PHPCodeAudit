#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__      = 'Christophoros Petrou (game0ver)'
__description__ = 'PHPCodeAudit.py: A Multi threaded PHP Code Auditor!'
__version__     = '1.0'

import os
import sys
import Queue
import threading
from colorama import Fore,Back,Style
from argparse import ArgumentParser, RawTextHelpFormatter, ArgumentTypeError

# console colors
FG, BT, FR, FY, S = Fore.GREEN, Style.BRIGHT, Fore.RED, Fore.YELLOW, Style.RESET_ALL


def banner():
    print BT+" _____ _____ _____ _____       _     _____       _ _ _   "
    print    "|  _  |  |  |  _  |     |___ _| |___|  _  |_ _ _| |_| |_ "
    print    "|   __|     |   __|   --| . | . | -_|     | | | . | |  _|"
    print    "|__|  |__|__|__|  |_____|___|___|___|__|__|___|___|_|_| ...ver. {}".format(S+FR+__version__+S)
    print "{0}Author:{1} Christoforos Petrou (game0ver) !\n".format(BT, S)


def console():
    """argument parser"""
    parser = ArgumentParser(description="{}PHPCodeAudit.py:{} A Multi threaded PHP Code Auditor!".format(BT, S),formatter_class=RawTextHelpFormatter)
    parser._optionals.title = "{}arguments{}".format(BT, S)
    parser.add_argument('-t', "--threads", help="Specify how many threads to use [{0}Default:{2} {1}None{2}]".format(BT, FR, S), 
                    default=None, type=int, metavar='')
    parser.add_argument('-d', "--dir", help="Specify a PHP application directory",
                    type=checkDir, required=True, metavar='')
    return parser.parse_args()

## the above PHP functions are taken by this stackoverflow thread:
## https://stackoverflow.com/questions/3115559/exploitable-php-functions
badPHPFunctions=[
"$_GET[", "$_POST[", "$_REQUEST[", 
"exec(", "passthru(", "system(", 
"shell_exec(", "popen(", "proc_open(", 
"pcntl_exec(","eval(", "assert(", 
"preg_replace(", "create_function(", 
"include(", "include_once(", "require(", 
"require_once(","phpinfo(","posix_mkfifo(",
"posix_getlogin(","posix_ttyname(","getenv(",
"get_current_user(","proc_get_status(","get_cfg_var(",
"disk_free_space(", "disk_total_space(","diskfreespace(",
"getcwd(","getlastmo(","getmygid(","getmyinode(","getmypid(","getmyuid("]

PHPfiles = Queue.Queue()

def checkDir(dirctry):
    if not os.path.isdir(dirctry):
        raise ArgumentTypeError('{}[-] Directory does not exist'.format(FR,S))

    if os.access(dirctry, os.R_OK):
        return dirctry
    else:
        raise ArgumentTypeError('{}[-] Directory is not writable'.format(FR,S))


def process(file):
    with open(file, 'r') as f:
        data = f.read().splitlines()
    for ind, line in enumerate(data):
        for func in badPHPFunctions:
            if func in line:
                print "{2}{3}{1}:{0}{2}{4} => {2}{1} {5}".format(BT, S, FG, file, ind, line.strip().replace(func[:-1],FR+func[:-1]+S))


def examine():
    while not PHPfiles.empty():
        process(PHPfiles.get())


if __name__ == '__main__':
    banner()
    args = console()
    os.chdir(args.dir)
    for r,d,f in os.walk("."):
        for file in f:
            if file.endswith('.php'):
                PHPfiles.put("{}/{}".format(r[1:],file)[1:])
    if args.threads:
        for i in range(args.threads):
            t = threading.Thread(target=examine)
            t.start()
    else:
        examine()
#_EOF