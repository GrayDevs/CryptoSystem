#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" The CryptoSystem main part.

# standard_key = 0x4781248c843906b0ce31ab07d62e968a6b7e8c17ecdfdd4b6b78aafbc13030cde610e0aea6ce35e1d39fbf8cc6fd98caee79f83f8fc1a04d7ef2db74e02ecaabd668385c9c8b4f62d9c1ad761601e040716494cad09cde8885bea8307a82032f037440cdc2976593d142eb70e83475839a3d089cbb0ed274b994e9c7d6b5c323
"""

# import
import argparse
import sys
import textwrap

from core import idea, SHA3, diffie_hellman, X509

# Output should be colored
colors = True
# Detecting the OS of current system
machine = sys.platform
if machine.lower().startswith(('os', 'darwin', 'ios')):
    # Colors shouldn't be displayed on macOS and Windows
    colors = False
if not colors:
    end = red = white = green = yellow = run = bad = good = info = que = ''
else:
    end = '\x1b[0m'  # '\033[1;m'
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

# Some Checking parameters
cert_created, cert_authenticated = False, False

# Menu
menu = {}
menu['[1]'] = "Generate a Diffie-hellman Public Key"
menu['[2]'] = "Create and sign a certificate"
menu['[3]'] = "Authenticate a certificate"
menu['[4]'] = "Sharing a secret key"
menu['[5]'] = "Encrypt a file (and sign it)"
menu['[6]'] = "Decrypt a file and verify its signature"
menu['[7]'] = "Exit"
while True:
    print("\n--- GS15 Main Menu")
    options = menu.keys()
    for entry in options:
        print(entry, menu[entry])

    selection = input("/> ")
    if selection == '1':
        A, g, p = diffie_hellman.dh_public_keygen()
        print(run, "Public Key: [A, g, p]\x1b[0m (copy the following line):\n{0}\n{1}\n{2}".format(A, g, p))
    elif selection == '2':
        print(run, "\x1b[0mStep 1) Creating a certificate")
        A = int(input("Type in A:"))
        g = int(input("Type in g:"))
        p = int(input("Type in p:"))
        public_key = [A, g, p]
        cert = X509.Certificate(public_key)
        print(run, "\x1b[0mStep 2) Make it signed by a trusted third party")
        X509.UTT_Signature(cert)
        cert_created = True
    elif selection == '3':
        if cert_created:
            print("\033[1;97m[~]\x1b[0m Getting Third Party Public Key ...")
            utt_n, utt_e = X509.UTT_Keys()[:2]
            wrap_n = textwrap.fill(hex(utt_n), 94, initial_indent="\t", subsequent_indent="\t\t")
            print("\033[1;97m[~]\x1b[0m UTT Public Keys:\n\tn:{0}\n\te:\t{1}".format(wrap_n, hex(utt_e)))
            cert.pk_signature_check(utt_n, utt_e)
            cert_authenticated = True
        else:
            print(info, "You must Create a certificate before trying to authentify one", end)
    elif selection == '4':
        print(que, "\x1b[0mDirect Sharing (y) / Sharing through certificate")
        choice = input("KeyGen/> ")
        if choice == "y" or choice == "Y":
            diffie_hellman.dh_main()
        elif cert_authenticated:
            print(diffie_hellman.dh_keygen(cert.subject_public_key[:-1]))
        else:
            print(info, "You must Create and Authenticate a certificate before sharing key through it", end)
    elif selection == '5':
        print(run, "Encrypt a file (and sign it)", end)
        idea.idea_main_encryption()
    elif selection == '6':
        print(run, "Decrypt a message (and verify its signature)", end)
        idea.idea_main_decryption()
    elif selection == '7':
        break
    else:
        print(info, "Unknown Option Selected!", end)

print('\n# Exit...')
