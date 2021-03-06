# -*-coding:UTF-8 -*
# !/usr/bin/env python

import sys
from time import sleep
import numpy as np
from math import *

from tqdm import tqdm

""" SHA3 Hash Implementation

Works for different hash length:
> 256 bits
> 384 bits
> 512 bits
"""


#########################
#                       #
#       UTILITIES       #
#                       #
#########################

def bloc(lgHash):
    """ bloc =r+c bits
    :param lgHash:
    :return: (r, c, tailleBloc):
    """

    c = 2 * int(lgHash)
    tailleBloc = 1600
    r = tailleBloc - c

    # print("r :" + str(r))
    # print("c " + str(c))

    return r, c, tailleBloc



def choixlgHash():
    """ choix longueur Hash utlisateur
    :return: lgHash
    """
    taillehash = 0
    i = 1
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
    assert taillehash != 0
    return taillehash


def ofichier():
    """ Ouvre le fichier et vérifie s'il existe
    :return: fichier
    """
    fichier = input("Entrez un fichier :")
    i = 0
    while i == 0:
        try:
            with open(fichier):
                i = 1
        except IOError:
            fichier = input("Erreur, entrez un vrai fichier :")

    return fichier


def convBin(fichier):
    """ Convertis le fichier au format binaire
    :param fichier:
    :return: fichierbinaire
    """
    fic = open(fichier, "r", encoding="ISO-8859-1").read()
    fichierbinaire = ''.join(format(ord(x), 'b') for x in fic)
    return fichierbinaire


def padding(fichierBinaire, r):
    """ Padding multiple de r
    :param fichierBinaire:
    :param r:
    :return: messagePadding
    """

    if len(fichierBinaire) != r:
        messagePadding = ("0" * (r - (len(fichierBinaire)) % r)) + fichierBinaire
    else:
        messagePadding = fichierBinaire
    return str(messagePadding)


def padding2(taille, xor):
    """ Padding binaire clé (clé à la taille souhaité)
    :param taille:
    :param xor:
    :return: resu
    """
    if len(xor) != taille:
        resu = ("0" * (taille - (len(xor)) % taille)) + xor
    else:
        resu = xor

    return resu


def hash(messagePadding, r):
    """ Fonction hash = creation bloc + application fonction

    :param messagePadding:
    :param r:
    :return:
    """

    "Création du Bloc B0"
    B0 = [[["0" for k in range(0, 64)] for j in range(0, 5)] for i in range(0, 5)]
    "print(B0)"
    B0_tab = np.asarray(B0)
    "print(B0_tab)"
    B0_string = array_to_string(B0_tab)
    "print(B0_string)"

    "Calcul nombre de bloc à construire"
    Nb_iteration = int(len(messagePadding) / r)
    BlocString = ''
    for n in range(0, Nb_iteration):
        "Construction des différents blocs"
        stn_p = messagePadding[n * r:(n + 1) * r]  # Decoupe le message en plusieurs parties de taille r
        if n == 0:  # Construction B0 et XOR B0(r) avec P1
            # print("------------------------------------------------------Construction B" + str(n)
            # + "-----------------------------------------------------")
            rhashB0 = B0_string[:r]
            RXOR = xor_binaire(rhashB0, stn_p)
            Bloc = RXOR + B0_string[r:]
        else:  # Construction des autres blocs et XOR Bn(r) avec Pn+1
            # print("------------------------------------------------------Construction B" + str(n)
            # + "-----------------------------------------------------")
            rhashB = BlocString[:r]
            RXOR = xor_binaire(rhashB, stn_p)
            Bloc = RXOR + BlocString[r:]

        BlocTab = string_to_array(Bloc)
        # print("Avant application de la fonction " + array_to_string(BlocTab))

        for i in range(0, 24):
            "Application fonction f"
            # print("Fonction de hashage :" + str(i+1) + "ème iteration")
            BlocTab, BlocString = fonctionHASH(BlocTab)

    # print("hash-"+lgHash+"bits ->" + BlocString)
    # print("-------------TEST--------------")
    # print("pad " + str(messagePadding))
    # print(len(messagePadding))
    # print("P1 " + str(stn_p))
    # print(len(stn_p))
    # print("rb0 " + str(rhashB0))
    # print(len(rhashB0))
    # print("resu " )
    # print("test " + RXOR)
    # print(len(RXOR))
    # print("--------------------------------")

    return BlocTab, BlocString


def bit_parite(bloc):
    """
    :param bloc:
    :return: valeurBitParité
    """
    bit = str(bloc)
    # print(str(bloc))
    var = bit.count('1')
    # print("nombre de 1 " + str(var))

    if var % 2 == 0:  # pair
        return "00000"
    else:  # impair
        return "11111"


def padding3(Bloc):
    """Padding pour un bloc
    :param Bloc:
    :return: BlocN
    """
    if len(Bloc) != 5:
        BlocN = ("0" * (5 - len(Bloc))) + Bloc
    else:
        BlocN = Bloc

    return BlocN


def fonctionHASH(BlocTab):
    """ Creation de la fonction f utilisé dans hash
    :param BlocTab:
    :return: BlocEtape, BlocString
    """

    "Etape 1"
    BlocEtape1 = BlocTab
    for j in range(0, 5):
        for k in range(1, 64):
            # print("DEBUT----------")
            # print(''.join(BlocTab[:,j,k]),)
            # print("------Parité------")
            # print(bit_parite(''.join(BlocTab[:,j,k-1])))
            # print("FIN -------------")
            Bloc = xor_binaire(''.join(BlocTab[:, j, k]),
                               bit_parite(''.join(BlocTab[:, j, k - 1])))  # XOr avec le bit de parité
            # print("1 -> " +str(Bloc))
            # BlocN1 = str(padding3(Bloc1))
            BlocEtape1[:, j, k] = list(str(Bloc))
        "on le fait aussi pour le premier bit du bloc de 64 bits"
        Bloc = xor_binaire(''.join(BlocTab[:, j, 0]), bit_parite(''.join(BlocTab[:, j, 63])))
        # print("2 -> " + str(Bloc))
        # BlocN2 = str(padding3(Bloc2))
        BlocEtape1[:, j, 0] = list(Bloc)

    # BlocString1 = array_to_string(BlocEtape1)
    # print("Etape 1 : " + BlocString1)

    "Etape 2"
    BlocEtape2 = BlocEtape1
    for i in range(0, 5):
        for j in range(0, 5):
            tj, ti = T(j, i)
            # On permute les blocs de 64bits en fonction de T
            BlocEtape2[i, j, :] = BlocEtape1[(ti + i) % 5, (tj + j) % 5, :]

    # BlocString2 = array_to_string(BlocEtape2)
    # print("Etape 2 : " + BlocString2)

    "Etape 3"
    BlocEtape3 = BlocEtape2
    for i in range(0, 5):
        for j in range(0, 5):
            # On permute les blocs de 64bits en fonction de j > (2i+3j)%5
            BlocEtape3[i, j, :] = BlocEtape2[j, (2 * i + 3 * j) % 5, :]

    # BlocString3 = array_to_string(BlocEtape3)
    # print("Etape 3 : " + BlocString3)

    "Etape 4"
    BlocEtape4 = BlocEtape3
    for j in range(0, 4):
        for i in range(0, 5):
            # print("---------")
            # print(''.join(BlocEtape3[i, j, :]))
            # print(And(''.join(BlocEtape3[i, j + 1, :]),''.join(BlocEtape3[i, j - 1, :])))
            # print("---------")
            bloc = xor_binaire(''.join(BlocEtape3[i, j, :]), And(''.join(BlocEtape3[i, (j + 1) % 5, :]), ''.join(
                BlocEtape3[i, (j - 1) % 5, :])))  # XOR entre lignes
            # print("(-------)")
            # print(bloc)
            # print("(-------)")
            BlocEtape4[i, j, :] = list(bloc)

    # BlocString4 = array_to_string(BlocEtape4)
    # print("Etape 4 : " + BlocString4)

    "Etape 5"
    BlocEtape5 = BlocEtape4
    for m in range(0, 6):
        for j in range(1, 5):
            BlocEtape5[j, j, :] = xor_binaire(BlocEtape4[j, j, (2 ^ m - 1) % 64],
                                              BlocEtape4[j, j, m + 7 * lfsr(m)])  # XOR entre certains bits

    BlocString5 = array_to_string(BlocEtape5)
    # print("Etape 5 : " + BlocString5)

    return BlocEtape5, BlocString5


def lfsr(m):
    """ LFSR
    :param m:
    :return: ValeurLFSR
    """
    lfsr_tab = [0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(0, 7):
        lfsr_tab[i + 8] = lfsr_tab[i + 3] ^ lfsr_tab[i + 5]
        # print( lfsr_tab)
    return lfsr_tab[m + 8]


def fonctionRecuperation(HashBloc, p, r):
    """ Phase de recuperation
    :param HashBloc:
    :param p: <int>
    :param r: <int>
    :return: Hash: <str> -
    """

    m = ceil(int(r) / int(p))
    # c = int(r) + int(p)
    # print("m : " + str(m))

    for i in range(0, m - 1):
        "application fonction récupération"
        # print("Fonction de hashage :" + str(i+1) + "ème iteration")
        HashBloc, HashString = fonctionHASH(HashBloc)
        if i == 0:
            Hash = str(HashString[:r])
        else:
            Hash = str(HashString[:r]) + str(Hash)  # Concaténation morceaux de hash

    # print("taille hash : " + str(len(Hash)))
    # print("Sha3-"+p+"bits ->"+HashString)
    Hash = Hash[:int(p)]  # hash tronqué obtenir p bits

    return str(Hash)


def T(j, i):
    """ Calcul de valeur ti et tj pour etape 2 fonction f
    :param j:
    :param i:
    :return:
    """
    tj = (5 - i + j) % 5
    ti = (5 + i - j) % 5
    return tj, ti


def And(a, c):
    """fonction and binaire
    :param a:
    :param c:
    :return: rvar
    """
    var = '{0:b}'.format(int(a, 2) & int(c, 2))
    rvar = padding2((len(c)), var)
    return rvar


def xor_binaire(r, p):
    """ fonction xor binaire
    :param r:
    :param p:
    :return: RXOR
    """
    resuXOR = format(int(r, 2) ^ int(p, 2), 'b')
    RXOR = padding2(len(p), resuXOR)
    return RXOR


def array_to_string(bloc):
    """fonction array_to_string
    :param bloc:
    :return: string_hash
    """
    string_hash = '0'
    for i in range(0, 5):
        for j in range(0, 5):
            string_hash = string_hash + ''.join(bloc[i, j, :])

    string_hash = string_hash[1:]
    return string_hash


def string_to_array(string_hash):
    """ fonction string_to_array
    :param string_hash:
    :return: bloc_hash
    """
    block_hash_tab = [[["0" for y in range(64)] for x in range(5)] for z in range(5)]
    block_hash = np.asarray(block_hash_tab)
    n = 0
    for i in range(0, 5):
        for j in range(0, 5):
            for k in range(0, 64):
                block_hash[i, j, k] = string_hash[n]
                n = n + 1

    return block_hash


#########################
#                       #
#     MAIN FUNCTIONS    #
#                       #
#########################

def sha3_txt(txt, lgHash=256):
    """ NOT WORKIN' (or at least not everytime)

    :param txt: <str>(preferably) - some text
    :param lgHash: <int> - hash length
    :return: hexdigest: <str>
    """
    r, c, block_len = bloc(lgHash)
    binary_txt = bin(int.from_bytes(str(txt).encode('utf-8'), 'little'))[2:]
    messagePadding = padding(binary_txt, r)
    HashBloc, HashString = hash(messagePadding, r)
    RecupHash = fonctionRecuperation(HashBloc, lgHash, r)
    hexdigest = hex(int(str(RecupHash), 2)).zfill(lgHash // 4)

    return hexdigest


def sha3_int(integer, lgHash=256):
    """ From int to sha3_XXX hexdigest

    :param integer: <int>
    :param lgHash: <int> - hash length
    :return: hexdigest: <str>
    """
    r, c, block_len = bloc(lgHash)
    binary_txt = bin(integer)[2:]
    messagePadding = padding(binary_txt, r)
    HashBloc, HashString = hash(messagePadding, r)
    RecupHash = fonctionRecuperation(HashBloc, lgHash, r)
    hexdigest = hex(int(str(RecupHash), 2)).zfill(lgHash // 4)
    # print("\033[1;32m[+]\x1b[0m", "Hash successfully generated")

    return hexdigest


def sha3_file(filename, lgHash=256):
    """ Give the Sha3_XXX hexdigest of a file

    :param filename: <str> - a filepath (or filename)
    :param lgHash: <int> - hash length
    :return: hexdigest: <str>
    """
    sys.stdout.flush()

    for i in tqdm(range(100), desc="Generating SHA3 Hash"):
        if i == 0:
            r, c, block_len = bloc(lgHash)
        elif i == 5:
            binary_file = convBin(filename)
        elif i == 10:
            messagePadding = padding(binary_file, r)
        elif i == 30:
            HashBloc, HashString = hash(messagePadding, r)
        elif i == 60:
            RecupHash = fonctionRecuperation(HashBloc, lgHash, r)
        elif i == 80:
            hexdigest = hex(int(str(RecupHash), 2)).zfill(lgHash // 4)
        sleep(0.01)

    sys.stdout.flush()

    return hexdigest


def sha3_main():
    """ Give the Sha3_XXX hexdigest of a file
    :return:
    """
    print("------Hashage sha-3----------")
    fichier = ofichier()
    lgHash = choixlgHash()
    print("Vous avez choisis " + lgHash + " bits.")
    r, c, taillebloc = bloc(lgHash)
    fichierBinaire = convBin(fichier)
    messagePadding = padding(fichierBinaire, r)
    print(
        "----------------------------------------------------------PADDING---------------------------------------------------------")
    print(
        "-------------------------------------------------------Initialisation-----------------------------------------------------")
    HashBloc, HashString = hash(messagePadding, r)
    print(
        "---------------------------------------------------Phase de récupération--------------------------------------------------")
    RecupHash = fonctionRecuperation(HashBloc, lgHash, r)
    print("Hash-" + lgHash + "bits =>" + RecupHash)
    print("Taille de Hash = " + str(len(RecupHash)))

# TEST ZONE
if __name__ == '__main__':
    # sha3_main()

    """    
    # ----------------
    # sha3_txt() TEST
    txt = "bonjour"
    plaintext_hash = sha3_txt(txt)
    print(plaintext_hash)
    """

    # ----------------
    # sha3_int() TEST
    integer = 0x4781248c843906b0ce31ab07d62e968a6b7e8c17ecdfdd4b6b78aafbc13030cde610e0aea6ce35e1d39fbf8cc6fd98caee79f83f8fc1a04d7ef2db74e02ecaabd668385c9c8b4f62d9c1ad761601e040716494cad09cde8885bea8307a82032f037440cdc2976593d142eb70e83475839a3d089cbb0ed274b994e9c7d6b5c323
    plaintext_hash = sha3_int(integer)
    print(plaintext_hash)


    # ----------------
    # sha3_file() TEST
    file = "tests/idea_test.txt"
    plaintext_hash = sha3_file(file)
    # Check
    expected_result = '0x2d852e36053c8f30d3635a53c286001e97643bd8397d0bfda82fbd946375f8bc'
    assert expected_result == plaintext_hash
    print("Hash:\033[1;32m", plaintext_hash, "\x1b[0m")


    pass
