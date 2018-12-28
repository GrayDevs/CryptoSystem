#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" The CryptoSystem main part. """

# import
import argparse
import sys
from core import idea, SHA3, diffie_hellman, X509

# Output should be colored
colors = True
# Detecting the OS of current system
machine = sys.platform
if machine.lower().startswith(('os', 'win', 'darwin', 'ios')):
    # Colors shouldn't be displayed on macOS and Windows
    colors = False
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
parser.add_argument('-v', '--verbose', help='verbose output', dest='verbose', action='store_true')
# ...
args = parser.parse_args()

# Menu
menu = {}
menu['[1]'] = "Generate keys"
menu['[2]'] = "Authenticate a public key / certificate"
menu['[3]'] = "Sharing a secrete key"
menu['[4]'] = "Encrypt a message / file (and sign it)"
menu['[5]'] = "Decrypt a message and verify its signature"
menu['[6]'] = "FULL"
menu['[7]'] = "Exit"
while True:
    options = menu.keys()
    for entry in options:
        print(entry, menu[entry])

    selection = input("> ")
    if selection == '1':
        diffie_hellman.dh_main()
    elif selection == '2':
        print("Authenticate a certificate")
    elif selection == '3':
        print("Sharing a secret key")
    elif selection == '4':
        print("Encrypt a message / file")
    elif selection == '5':
        print("Decrypt a message and verify its signature")
    elif selection == '6':
        print("FULL")
    elif selection == '7':
        break
    else:
        print("Unknown Option Selected!\n")

print('\n# Exit...')
