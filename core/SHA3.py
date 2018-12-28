import sys
import numpy as np
from math import *


def bloc(lgHash):
    """ bloc =r+c bits

    :param lgHash:
    :return: (r, c, tailleBloc):
    """

    c = 2 * int(lgHash)
    tailleBloc = 1600
    r = tailleBloc - c

    print("r :" + str(r))
    print("c " + str(c))

    return r, c, tailleBloc


def choixlgHash():
    """ choix longueur Hash utlisateur

    :return: lgHash
    """
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

    if (len(fichierBinaire) != r):
        messagePadding = ("0" * ((r - (len(fichierBinaire)) % r))) + fichierBinaire
    else:
        messagePadding = fichierBinaire
    # print(len(messagePadding))
    return str(messagePadding)


def padding2(taille, xor):
    """ Padding binaire clé (clé à la taille souhaité)

    :param taille:
    :param xor:
    :return: resu
    """
    if (len(xor) != taille):
        resu = ("0" * (taille - (len(xor)) % taille)) + xor
    else:
        resu = xor

    return resu


def hash(messagePadding, r, c, taillebloc, lgHash):
    """ Fonction hash = creation bloc + application fonction
    

    :param messagePadding:
    :param r:
    :param c:
    :param taillebloc:
    :param lgHash:
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

    for n in range(0, Nb_iteration):
        "Construction des différents blocs"
        stn_p = messagePadding[n * r:(n + 1) * r] # Decoupe le message en plusieurs parties de taille r
        if n == 0:# Construction B0 et XOR B0(r) avec P1
            print("------------------------------------------------------Construction B" + str(
                n) + "-----------------------------------------------------")
            rhashB0 = B0_string[:r]
            RXOR = xor_binaire(rhashB0, stn_p)
            Bloc = RXOR + B0_string[r:]
        else: #Construction des autres blocs et XOR Bn(r) avec Pn+1
            print("------------------------------------------------------Construction B" + str(
                n) + "-----------------------------------------------------")
            rhashB = BlocString[:r]
            RXOR = xor_binaire(rhashB, stn_p)
            Bloc = RXOR + BlocString[r:]

        BlocTab = string_to_array(Bloc)
        # print("Avant application de la fonction " + array_to_string(BlocTab))

        for i in range(0, 24):
            "Application fonction f"
            # print("Fonction de hashage :" + str(i+1) + "ème iteration")
            BlocTab, BlocString = fonctionHASH(BlocTab)

            pass

    pass

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

    if var % 2 == 0:#pair
        return "00000"
    else:#impair
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
            Bloc = xor_binaire(''.join(BlocTab[:, j, k]), bit_parite(''.join(BlocTab[:, j, k - 1])))#XOr avec le bit de parité
            # print("1 -> " +str(Bloc))
            # BlocN1 = str(padding3(Bloc1))
            BlocEtape1[:, j, k] = list(str(Bloc))
        "on le fait aussi pour le premier bit du bloc de 64 bits"
        Bloc = xor_binaire(''.join(BlocTab[:, j, 0]), bit_parite(''.join(BlocTab[:, j, 63])))
        # print("2 -> " + str(Bloc))
        # BlocN2 = str(padding3(Bloc2))
        BlocEtape1[:, j, 0] = list(Bloc)
        pass
    pass

    BlocString1 = array_to_string(BlocEtape1)
    # print("Etape 1 : " + BlocString1)

    "Etape 2"
    BlocEtape2 = BlocEtape1
    for i in range(0, 5):
        for j in range(0, 5):
            tj, ti = T(j, i)
            BlocEtape2[i, j, :] = BlocEtape1[(ti + i) % 5, (tj + j) % 5, :]#On permute les blocs de 64bits en fonction de T
        pass
    pass

    BlocString2 = array_to_string(BlocEtape2)
    # print("Etape 2 : " + BlocString2)

    "Etape 3"
    BlocEtape3 = BlocEtape2
    for i in range(0, 5):
        for j in range(0, 5):
            BlocEtape3[i, j, :] = BlocEtape2[j, (2 * i + 3 * j) % 5, :]#On permute les blocs de 64bits en fonction de j > (2i+3j)%5
        pass
    pass

    BlocString3 = array_to_string(BlocEtape3)
    # print("Etape 3 : " + BlocString3)

    "Etape 4"
    BlocEtape4 = BlocEtape3
    for j in range(0, 4):
        for i in range(0, 5):
            # print("---------")
            # print(''.join(BlocEtape3[i, j, :]))
            # print(And(''.join(BlocEtape3[i, j + 1, :]),''.join(BlocEtape3[i, j - 1, :])))
            # print("---------")
            bloc = xor_binaire(''.join(BlocEtape3[i, j, :]), And(''.join(BlocEtape3[i, (j + 1)%5, :]), ''.join(BlocEtape3[i, (j - 1)%5, :])))#XOR entre lignes
            # print("(-------)")
            # print(bloc)
            # print("(-------)")
            BlocEtape4[i, j, :] = list(bloc)
        pass
    pass

    BlocString4 = array_to_string(BlocEtape4)
    # print("Etape 4 : " + BlocString4)

    "Etape 5"
    BlocEtape5 = BlocEtape4
    for m in range(0, 6):
        for j in range(1, 5):
            BlocEtape5[j, j, :] = xor_binaire(BlocEtape4[j, j, (2 ^ m - 1) % 64], BlocEtape4[j, j, m + 7 * lfsr(m)])#XOR entre certains bits

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


def fonctionRecuperation(HashBloc, HashString, p, r):
    """ Phase de recuperation

    :param HashBloc:
    :param HashString:
    :param p:
    :param r:
    :return: Hash: <str> -
    """

    m = ceil(int(r) / int(p))
    c = int(r) + int(p)
    # print("m : " + str(m))

    for i in range(0, m - 1):
        "application fonction récupération"
        # print("Fonction de hashage :" + str(i+1) + "ème iteration")
        HashBloc, HashString = fonctionHASH(HashBloc)
        if i == 0:
            Hash = str(HashString[:r])
        else:
            Hash = str(HashString[:r]) + str(Hash)#Concaténation morceaux de hash

    # print("taille hash : " + str(len(Hash)))
    # print("Sha3-"+p+"bits ->"+HashString)
    Hash = Hash[:int(p)]#hash tronqué pour obtenir p bits

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
    # print(len(string_hash))
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


def sha3_auto_main(fichier, lgHash=256):
    """

    :param fichier:
    :param lgHash:
    :return:
    """
    r, c, taillebloc = bloc(lgHash)
    fichierBinaire = convBin(fichier)
    messagePadding = padding(fichierBinaire, r)
    HashBloc, HashString = hash(messagePadding, r, c, taillebloc, lgHash)
    RecupHash = fonctionRecuperation(HashBloc, HashString, lgHash, r)
    print(RecupHash)

    return 0


def sha3_main():
    """

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
    HashBloc, HashString = hash(messagePadding, r, c, taillebloc, lgHash)
    print(
        "---------------------------------------------------Phase de récupération--------------------------------------------------")
    RecupHash = fonctionRecuperation(HashBloc, HashString, lgHash, r)
    print("Hash-" + lgHash + "bits =>" + RecupHash)
    print("Taille de Hash = " + str(len(RecupHash)))

    return 0

if __name__ == '__main__':
    sha3_main()
