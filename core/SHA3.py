""" This module implements SHA3 algorithm """

import sys


def bloc(lgHash):
    "bloc =r+c bits"
    c = 2 * int(lgHash)
    tailleBloc = 1600
    r = tailleBloc - c

    return r, c, tailleBloc


def choixlgHash():
    i = 1
    taillehash = -1
    while i < 2:
        print("""Veuillez choisir une taille pour le hash ?\n
                0- Stopper le programme 
                1- 256 bits
                2- 384 bits
                3- 512 bits""")
        ctaille = input("Votre choix :")

        if ctaille == '1':
            taillehash = '256'
            i = 3
        elif ctaille == '2':
            taillehash = '384'
            i = 3
        elif ctaille == '3':
            taillehash = '512'
            i = 3
        elif ctaille == '0':
            sys.exit()
        else:
            print("Choisir un nombre entre 1 et 3 !!!")
            i = 1

    assert taillehash != -1
    return taillehash


def ofichier():

    fichier = input ("Entrez un fichier :")
    i = 0
    while i == 0:
        try:
            with open(fichier):
                i = 1
        except IOError:
            fichier = input("Erreur, entrez un vrai fichier :")

    return fichier


def convBin(fichier):

    fic = open(fichier, "r", encoding="ISO-8859-1").read()
    fichierbinaire = ''.join(format(ord(x), 'b') for x in fic)

    return fichierbinaire

def padding(fichierBinaire,r):

    "padding multiple de r"

    if (len(fichierBinaire) != r):
        messagePadding = ("0" * (r - (len(fichierBinaire)) % r )) + fichierBinaire
    else : messagePadding = fichierBinaire

    return messagePadding

def hash(messagePadding,r,c,taillebloc):
    "EN COURS "
    B0 = "0" * taillebloc
    NombreIter = 24

def main():

    print("------Hashage sha-3----------")
    fichier = ofichier()
    lgHash=choixlgHash()
    print("Vous avez choisis " + lgHash +" bits.")
    r,c,taillebloc=bloc(lgHash)
    fichierBinaire=convBin(fichier)
    messagePadding=padding(fichierBinaire,r)
    print ("---------PADDING-----------")
    print("---------Initialisation-----------")
    hashage=hash(messagePadding,r,c,taillebloc)



if __name__ == '__main__':
     main()

