# -*-coding:UTF-8 -*
# !/usr/bin/env python

""" Project tool-box
NB: Some of those algorithms are Pythonic implementation of pseudo-codes available on Wikipedia

~~~ SUMMARY ~~~

# FILE UTILS
# wipe_file
# write_file
# check_file_exist
# get_file_hex
# get_filename

# MATHS UTILS
# gcd
# gcd_recursive
# lcm
# exp_by_squaring_recursive
# exp_by_squaring_iterative
# ceil_div
# xgcd
# mod_inv

# SIEVES :
# sieve_of_eratosthenes
# sieve_of_hoare
# sieve_of_sundaram
# sieve_of_atkin

# PRIMALITY TESTS
# fermat_primality_test
# Solovay-Strassen
# Rabin-Miller  # https://fr.wikipedia.org/wiki/Test_de_primalit%C3%A9_de_Miller-Rabin
# (Ulam spiral)

# PRIME GENERATOR
# prime_gen
"""

import secrets
import random
from time import process_time
from tkinter import filedialog, Tk


#########################
#                       #
#       FILE UTILS      #
#                       #
#########################

def wipe_file(file):
    """ Erase file content if it already exists

    :param file: <str>
    :return: file: <str> - wiped file
    """
    with open(file, encoding='utf-8', mode='w') as file_to_wipe:
        file_to_wipe.write("")
    return file


def write_file(file_name, text):
    with open(file_name, mode='wb') as file:
        file.write(text)
    return 0


def check_file_exist(filename):
    """ Check if a file exists

    :param filename: <str>
    :return: <boolean>
    """
    try:
        with open(filename):
            return True
    except:
        return False


def get_filename():
    """ Open a Tkinter filedialog

    :return: <str> - file path
    """
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    return filedialog.askopenfilename(title = "Select file to Encrypt", filetypes = (("Text Files","*.txt"),("all files","*.*")))

def save_file():
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    return filedialog.asksaveasfilename(title = "Select file", filetypes = (("Encrypted Files","*.cypher"), ("all files","*.*")))

def get_file_hex(file_name="tests/idea_test.txt"):
    """ Getting the content of a file

    :param: file_name: <str> - file name
    :return: content_as_bytes : <str> - content in hex
    """
    with open(file_name, 'rb') as file_alias:
        content_as_bytes = file_alias.read()

    hex_content = bytes.hex(content_as_bytes)
    return hex_content


#########################
#                       #
#      MATHS UTILS      #
#                       #
#########################

def gcd(a, b):
    """ Calculate the Greatest Common Divisor of a and b

    Unless b==0, the result will have the same sign as b (so that when
    b is divided by it, the result comes out positive).
    :param a : <int>
    :param b : <int>
    :return a : <int> - the gcd of a and b
    """
    while b != 0:
        a, b = b, (a % b)
    return a


def gcd_recursive(a, b):
    if b == 0:
        return a
    else:
        return gcd_recursive(b, a % b)


def lcm(a, b):
    """ Search the lowest positive integer than can be devide by a and b

    :param a : <int>
    :param b: <int>
    :return: <int> - the lcm of a and b
    """
    return (a * b) // gcd(a, b)


def exp_by_squaring_recursive(n, exp):
    """ Fast way to do exponentiation, recursively (Not tail-recursive)

    :param n: <int>
    :param exp: <int> - exponent
    :return: n**exp
    """
    x = n
    n = exp
    if n < 0:
        return exp_by_squaring_recursive(1 / x, -1)
    elif n == 0:
        return 1
    elif n == 1:
        return x
    elif n % 2 == 0:
        return exp_by_squaring_recursive(x * x, n / 2)
    elif n % 2 != 0:
        return x * exp_by_squaring_recursive(x * x, (n - 1) / 2)


def exp_by_squaring_iterative(n, exp):
    """  Fast way to do exponentiation, iteratively

    :param n: <int>
    :param exp: <int> - exponent
    :return: n**exp
    """
    if exp < 0:
        n = 1 / n
        exp = -exp

    if exp == 0:
        return 1

    y = 1
    while exp > 1:
        if exp % 2 == 0:
            n = n * n
            exp = exp / 2
        else:
            y = n * y
            n = n * n
            exp = (exp - 1) / 2

    return n * y


def ceil_div(a, b):
    return -(-a // b)


def xgcd(a, b):
    """ Extended Euclidean Algorithm
    :param a: <int>
    :param b: <int>
    :return: k: <int>, a: <int>,  prev_x: <int>, prev_x: <int>
    """
    k, q = 0, 0
    prev_x, x = 1, 0
    prev_y, y = 0, 1
    while b:
        q = a // b
        x, prev_x = (q * x + prev_x), x
        y, prev_y = (q * y + prev_y), y
        a, b = b, a % b
        k += 1
        # print("k={0}\t a={1}\t  b={2}\t  q={3}\t x={4}\t  y={5}".format(k+1, a, b, q, x, y))

    return k, a, prev_x, prev_y


def mod_inv(a, b):
    """ Calculate the modular inverse
    :param a: <int>
    :param b: <int>
    :return: <int> - a^(-1) [b]
    """
    k, a, x, y = xgcd(a, b)
    return (pow(-1, k) * x) % b


#########################
#                       #
#        SIEVES         #
#                       #
#########################

def sieve_of_eratosthenes(limit):
    """ Search and return the primes lower or equals to 'limit'

    :param limit: <int>
    :return: primes: <list>
    """
    primes = []
    numbers = range(2, limit + 1)

    while len(numbers):
        primes.append(numbers[0])  # 2 is a prime

        # remove all the multiple of the first number
        next_numbers = []
        for i in range(1, len(numbers)):
            if numbers[i] % numbers[0] > 0:
                next_numbers.append(numbers[i])
        numbers = next_numbers

    return primes


def sieve_of_hoare():
    """ pipe-line version (1978) """
    pass


def sieve_of_sundaram():
    pass


def sieve_of_atkin():
    pass


#########################
#                       #
#    PRIMALITY TESTS    #
#                       #
#########################

def fermat_primality_test(n, k=2):
    """ Probabilistic way to determine if a number n is prime or not

    :param n: <int> - the number to test for primality
    :param k: <int> - number of tests
    :return: <boolean>:
        False if not prime,
        True if it seems to be prime
    """
    if n < 2:
        return False

    if n > 3:
        # https://stackoverflow.com/questions/39188827/trying-to-understand-python-loop-using-underscore-and-input#39188897
        for _ in range(k):
            rand_num = random.randint(2, n - 2)
            if exp_by_squaring_recursive(rand_num, n - 1) % n != 1:
                return False

    return True


# https://fr.wikipedia.org/wiki/Test_de_primalit%C3%A9_de_Miller-Rabin
# Nota : Use pow(x, y, z) instead of x**y % z
def temoin_miller(a, n):
    """  Recherche d'un témoin de Miller

    :param a: <int> - un entier > 1
    :param n: <int> - un entier impair ≥ 3
    :return: <boolean>:
        True si a est un témoin de Miller que n est composé,
        False si n est fortement pseudo-premier en base a
    """
    # Calculer s et d tels que n - 1 = 2^(s)×d avec d impair  s > 0 car n impair
    s = 0
    d = n - 1
    while s % 2 == 0:
        s += 1
        d //= 2  # floor

    x = pow(a, d, n)  # x entier reste de la division de a^d par n
    # print("a:", a, "s:", s, "d:", d, "x:", x, "n-1:", n-1)  # debug
    if (x == 1) or (x == n - 1):
        return False  # sortie : a n'est pas un témoin de Miller

    while s > 0:
        x = pow(x, 2, n)  # reste de la division de x^2 par n
        if x == n - 1:
            return False  # sortie : a n'est pas un témoin de Miller
        s = s - 1

    return True  # a est un témoin de Miller, n est composé


def rabin_miller(n, k=14):
    """ Test de Rabin-Miller

    :param n: <int> - un entier impair ≥ 3
    :param k: <int> - un entier ≥ 1 (nombre de test)
    :return: <boolean>
        True si n est fortement pseudo-premier en base a pour k entiers a,
        False s'il est composé.
    """
    if (n == 2) or (n == 3):
        return True
    elif (n < 2) or (n % 2 == 0):
        return False

    # if n < 2^16 = 18,446,744,073,709,551,616, it is enough to test a=2,3,5,7,11,13,17,19,23,29,31 and 37;
    # ... @see wikipedia
    test_list = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 61, 73, 1662803]  # optimization
    for i in range(k):
        # 'a' est choisi aléatoirement dans l'intervalle [2, n-2]
        # a = randrange(2, n - 2)
        a = test_list[i]
        if a == n:
            return a == n
        if temoin_miller(a, n):  # temoin_miller(a, n) == True
            return False  # sortie, n est composé

    return True


# mathworld.wolfram.com/Rabin-MillerStrongPseudoprimeTest.html
def miller_rabin_primality_test(n, k=2):
    """ Probabilistic test to determine if n is prime
        Args:
            n -- int -- the number to test for primality
            k -- int -- the number of tests
        return False if not prime, or True if it seems to be prime
    """
    if (n == 2) or (n == 3):
        return True
    if (n < 2) or (n % 2 == 0):
        return False

    # factor n - 1 as 2^(r)*s
    r = 0
    s = n - 1
    while s & 1 == 0:
        r += 1
        s //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


#########################
#                       #
#    PRIME GENERATOR    #
#                       #
#########################

def prime_gen(bit_len=1024):
    t = process_time()
    probably_prime = 0
    while not rabin_miller(probably_prime):
        probably_prime = secrets.randbits(bit_len)

    print("Prime successfully generated in", process_time() - t)
    return probably_prime


# TEST ZONE
if __name__ == "__main__":
    # sieve_of_eratosthenes(1000000)
    # print(fermat_primality_test(7))
    # print(rabin_miller(44600782844059322679787115580475394454610249729145792871260295110063546808692305971895255281608176659435668688076634717303552368620463427957722398118490589527180422187442349959283617691974410079937916405314415599450518488171311795228586635640346382637523377502311060484277241482917191477205629836101135468161))
    # print(mod_inv(13, 7))
    # print(mod_inv(23, 120))



    filename = get_filename() + '.cypher'
    print(filename)
    file_extension = filename.split('.cypher', 1)[0]
    if len(file_extension.split('.', 1)) != 1:
        file_extension = '.' + file_extension.split('.', 1)[1]
    else:
        file_extension = ''
    print(file_extension)

    # print(save_file())
    pass
