#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" The CryptoSystem main part. """

# import
import argparse
import sys

# Output should be colored
colors = True
# Detecting the OS of current system
machine = sys.platform
if not colors:
    end = red = white = green = yellow = run = bad = good = info = que = ''
else:
    end = '\033[1;m'
    red = '\033[91m'
    white = '\033[1;97m'
    green = '\033[1;32m'
    yellow = '\033[1;33m'
    run = '\033[1;97m[~]\033[1;m'
    bad = '\033[1;31m[-]\033[1;m'
    good = '\033[1;32m[+]\033[1;m'
    info = '\033[1;33m[!]\033[1;m'
que = '\033[1;34m[?]\033[1;m'

# Banner
print('''
 .d8888b.   .d8888b.   d888  888888888       
d88P  Y88b d88P  Y88b d8888  888             
888    888 Y88b.        888  888             
888         "Y888b.     888  8888888b.       
888  88888     "Y88b.   888       "Y88b      
888    888       "888   888         888      
Y88b  d88P Y88b  d88P   888  Y88b  d88P      
 "Y8888P88  "Y8888P"  8888888 "Y8888P"
''')

# Processing command line arguments
parser = argparse.ArgumentParser()
# Options
# ...
parser.add_argument('-v', '--verbose', help='verbose output', dest='verbose', action='store_true')
args = parser.parse_args()

