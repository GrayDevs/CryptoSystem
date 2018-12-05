import sys
import numpy as np

def bloc(lgHash):
    "bloc =r+c bits"
    c = 2 * int(lgHash)
    tailleBloc = 1600
    r = tailleBloc - c

    print("r :"  + str(r))
    print("c " +  str(c))

    return r,c,tailleBloc

def choixlgHash():

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
            i= 3
        elif ctaille == '3':
            taillehash = '512'
            i= 3
        elif ctaille == '0':
            sys.exit()
        else:
            print("Choisir un nombre entre 1 et 3 !!!")
            i = 1

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
        messagePadding = ("0" * ((r - (len(fichierBinaire)) % r ))) + fichierBinaire
    else :
        messagePadding = fichierBinaire
    # print(len(messagePadding))
    return str(messagePadding)

def padding2(taille, xor):

    if (len(xor) != taille):
        resu = ("0" * (taille - (len(xor)) % taille)) + xor
    else :
        resu = xor

    return resu



def hash(messagePadding,r,c,taillebloc):


    " Fonction hash = creation bloc + application fonction"


    "-> 7 pour 384bits"

    B0 = [[["0" for k in range(0,64)] for j in range(0,5)] for i in range(0,5)]
    "print(B0)"
    B0_tab = np.asarray(B0)
    "print(B0_tab)"
    B0_string = array_to_string(B0_tab)
    "print(B0_string)"

    "Creation P"


    Nb_iteration = int(len(messagePadding) / r)

    for n in range(0,Nb_iteration):
        "Construction des blocs"

        rhashB0 = B0_string[:r]
        stn_p = messagePadding[n * r:(n+1) * r]
        resuXOR = format(int(rhashB0,2) ^ int(stn_p,2),'b')
        RXOR=padding2(len(stn_p),resuXOR)
        Bloc = RXOR + B0_string[r:]
        BlocTab = string_to_array(Bloc)

        for i in range(0,23):
            "application fonction"
            R_Fct_Hash = fonctionHASH(RXOR, BlocTab)

            pass

    pass


        #print("-------------TEST--------------")
        #print("pad " + str(messagePadding))
        #print(len(messagePadding))
        #print("P1 " + str(stn_p))
        #print(len(stn_p))
        #print("rb0 " + str(rhashB0))
        #print(len(rhashB0))
        #print("resu " )
        #print("test " + RXOR)
        #print(len(RXOR))
        #print("--------------------------------")







def fonctionHASH(RXOR, BlocTab ):

    "Creation de la fonction hash utilisé dans hash"

    """on remplace chaque bit de chaque sous-blocs de 64 bits par un XOR avec le bit de parité d’une colone
adjacente : B[:, j, k] ← B[:, j, k] ⊕ parite(B[:, j, k − 1]) ;"""



    for j in range(0, 5):
        for k in range(1, 64):
            BlocTab[:, j, k] =  BlocTab[:,j ,k] ^ BlocTab[:,j ,k-1]
    print(array_to_string(BlocTab))

    pass





def array_to_string(bloc):

    string_hash = '0'
    for i in range(0, 5):
        for j in range(0, 5):
            string_hash = string_hash + ''.join(bloc[i, j, :])

    string_hash = string_hash[1:]
    print(len(string_hash))
    return string_hash

def string_to_array(string_hash):

    block_hash_tab = [[["0" for y in range(64)] for x in range(5)] for z in range(5)]
    block_hash = np.asarray(block_hash_tab)
    n = 0
    for i in range(0, 5):
        for j in range(0, 5):
            for k in range(0, 64):
                block_hash[i, j, k] = string_hash[n]
                n = n + 1

    return block_hash

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
































