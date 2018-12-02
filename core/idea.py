# -*-coding:UTF-8 -*
# !/usr/bin/env python

""" This module implements the IDEA algorithm
@see: https://en.wikipedia.org/wiki/International_Data_Encryption_Algorithm
@see: https://en.wikipedia.org/wiki/Threefish

# Interesting point
    > IDEA algorithm entirely avoids the use of any lookup tables or S-boxes.

# Supported key sizes:
    > 96-bit
    > 128-bit
    > 160-bit
    > 256-bit

# Supported modes of operation:
    > ECB - Electronic Codebook
    > CBC - Cipher-Block Chaining
    > PCBC - Propagating Cipher Block Chaining
    @see: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation
    @see: https://csrc.nist.gov/publications/detail/sp/800-38a/final
"""

def addition(a, b):
    """ Addition modulo 2^16

    :param a: <int>
    :param b: <int>
    :return: result: <int>
    """

    result = (a + b) % 0x10000
    assert 0 <= result <= 0xFFFF

    return result


def multiplication(a, b):
    """ Multiplication modulo 2^16 + 1 ,
    where tha all-zero word (0x0000) in inputs is interpreted as 2^16,
    and 2^16 in output is interpreted as the all-zero word (0x0000)

    :param a: <int>
    :param b: <int>
    :return: result: <int>
    """

    # Assert statements are a convenient way to insert debugging
    # 'assert expression' is equivalent to :
    # if __debug__:
    #   if not expression: raise Assertion Error
    assert 0 <= a <= 0xFFFF  # FFFF = 65535
    assert 0 <= b <= 0xFFFF

    # Preventing entropy destruction and insure reversibility
    if a == 0:
        a = 0x10000  # 65536 = 2^16
    if b == 0:
        b = 0x10000

    result = (a * b) % 0x10001

    if result == 0x10000:
        result = 0

    assert 0 <= result <= 0xFFFF
    return result


def mul_inv(a):
    if a == 0:
         a = 0x10000

    result = a**(0x10001-2) % 0x10001
    return result


class IDEA:
    """
    This class is responsible for managing the encryption.
    It will generate subkeys and encrypt/decrypt the data.
    """
    def __init__(self, key=0x2BD6459F82C5B300952C49104881FF48, keylength = 128):
        self.keylength = keylength
        self.subkeys = [None]
        self.generate_subkeys(key)

    def generate_subkeys(self, key):
        """ IDEA operates with 52 subkeys.
        The first 8 sub-keys are extracted directly from the key, with K1 from the first round being the lower 16 bits.
        Further groups of 8 keys are created by rotating the main key left 25 bits between each group of 8.

        :param key: <int> key in hexadecimals
        """
        # assert 0 <= key < (1 << self.keylength) # debug
        modulo = 1 << self.keylength  # 0x100000000000000000000000000000000 (129 bits)

        sub_keys = []
        for i in range(52):
            sub_keys.append((key >> (112 - 16 * (i % int(self.keylength/16)))) % 0x10000)  # slicing the key into X 16bits long parts
            if i % int(self.keylength/16) == int(self.keylength/16)-1:  # keylength = 128, i = {7, 15, 23, 31, 39, 47}
                # x << y basically returns x with the bits shifted to the left by y places, BUT new bits on the right-hand-side are replaced by zeros.
                # To obtain a clean permutation, we simply do (x << y) OR (x >> (len(x)-y))
                key = ((key << 25) | (key >> (self.keylength - 25))) % modulo

        # Each round uses 6 16-bit sub-keys, while the half-round uses 4,
        # Putting subkeys into tuples should ease the encryption.
        keys = []
        for i in range(9): # 8.5 round => 9 tuples
            round_keys = sub_keys[6 * i: 6 * (i + 1)]
            keys.append(tuple(round_keys))
        self.subkeys = tuple(keys)

    def encrypt(self, plaintext):
        """
        :param plaintext:
        :return: cipher: <int> encrypted text
        """
        B1 = (plaintext >> 48) & 0xFFFF  # 0xFFFF masc
        B2 = (plaintext >> 32) & 0xFFFF
        B3 = (plaintext >> 16) & 0xFFFF
        B4 = plaintext & 0xFFFF

        for i in range(8):
            K = self.subkeys[i]  # gathering necessary subkeys
            B1 = multiplication(B1, K[0])     # 1
            B2 = addition(B2, K[1])           # 2
            B3 = addition(B3, K[2])           # 3
            B4 = multiplication(B4, K[3])     # 4

            T1 = B1 ^ B3                      # 5
            T2 = B2 ^ B4                      # 6

            T1 = multiplication(T1, K[4])     # 7
            T2 = addition(T2, T1)             # 8
            T2 = multiplication(T2, K[5])     # 9
            T1 = addition(T1, T2)             # 10

            B1 = B1 ^ T2                      # 11
            B3 = B3 ^ T2                      # 12
            B2 = B2 ^ T1                      # 13
            B4 = B4 ^ T1                      # 14

            B2, B3 = B3, B2                   # 15

        # NB : B2 and B3 are not permuted in the last round !!!
        # That is why we re-invert them
        B2, B3 = B3, B2

        # Half Round
        K = self.subkeys[8]
        B1 = multiplication(B1, K[0])
        B2 = addition(B2, K[1])
        B3 = addition(B3, K[2])
        B4 = multiplication(B4, K[3])

        cipher = (B1 << 48) | (B2 << 32) | (B3 << 16) | B4
        return cipher

    def generate_d_subkeys(self):
        """
        Generate decrypting subkeys
        :param key:
        :return:
        """
        d_sub_keys = []
        K = self.subkeys[8]
        d_sub_keys.append(mul_inv(K[0]))
        d_sub_keys.append(-K[1] % 0x10000)
        d_sub_keys.append(-K[2] % 0x10000)
        d_sub_keys.append(mul_inv(K[3]))

        for i in reversed(range(8)):
            K = self.subkeys[i]
            d_sub_keys.append(K[4])              # KD(5) = K(47)
            d_sub_keys.append(K[5])              # KD(6) = K(48)

            d_sub_keys.append(mul_inv(K[0]))     # KD(7) = 1/K(43)
            d_sub_keys.append(-K[2] % 0x10000)   # KD(8) = -K(45)
            d_sub_keys.append(-K[1] % 0x10000)   # KD(9) = -K(44)
            d_sub_keys.append(mul_inv(K[3]))     # KD(10) = 1/K(46)

        d_keys = []
        for i in range(9): # 8.5 round => 9 tuples
            round_keys = d_sub_keys[6 * i: 6 * (i + 1)]
            d_keys.append(tuple(round_keys))

        return tuple(d_keys)

    def decrypt(self, ciphertext):
        """
        Decryption works like encryption, but the order of the round keys is inverted, and the subkeys for the odd rounds are inversed.
        For instance, the values of subkeys K1–K4 are replaced by the inverse of K49–K52 for the respective group operation,
        K5 and K6 of each group should be replaced by K47 and K48 for decryption.
        :param ciphertext: <int>
        :return: plaintext: <int>
        """
        d_subkeys = self.generate_d_subkeys()

        B1 = (ciphertext >> 48) & 0xFFFF  # 0xFFFF masc
        B2 = (ciphertext >> 32) & 0xFFFF
        B3 = (ciphertext >> 16) & 0xFFFF
        B4 = ciphertext & 0xFFFF

        for i in range(8):
            KD = d_subkeys[i]  # gathering necessary subkeys
            B1 = multiplication(B1, KD[0])     # 1
            B2 = addition(B2, KD[1])           # 2
            B3 = addition(B3, KD[2])           # 3
            B4 = multiplication(B4, KD[3])     # 4

            T1 = B1 ^ B3                      # 5
            T2 = B2 ^ B4                      # 6

            T1 = multiplication(T1, KD[4])     # 7
            T2 = addition(T2, T1)             # 8
            T2 = multiplication(T2, KD[5])     # 9
            T1 = addition(T1, T2)             # 10

            B1 = B1 ^ T2                      # 11
            B3 = B3 ^ T2                      # 12
            B2 = B2 ^ T1                      # 13
            B4 = B4 ^ T1                      # 14

            B2, B3 = B3, B2                   # 15

        # Half Round
        KD = d_subkeys[8]
        B1 = multiplication(B1, KD[0])
        B2 = addition(B2, KD[1])
        B3 = addition(B3, KD[2])
        B4 = multiplication(B4, KD[3])

        # Permuting after
        B2, B3 = B3, B2

        plaintext = (B1 << 48) | (B2 << 32) | (B3 << 16) | B4
        return plaintext


def main():
    #key = 0x2BD6459F82C5B300952C49104881FF48
    #keylen = 128
    #plain = 0xF129A6601EF62A47
    #cipher = 0xEA024714AD5C4D84

    key = 0x5a14fb3e021c79e0608146a0117bff03
    keylen = 128
    plain = 0xF129A6601EF62A47
    cipher = 0xaa31cc614e0faa30

    print('key\t\t', hex(key))
    print('plaintext\t', hex(plain))

    my_IDEA = IDEA(key, keylen)  # creation de l'objet my_IDEA de type IDEA
    encrypted = my_IDEA.encrypt(plain)

    assert encrypted == cipher  # debug
    print('encrypted\t', hex(encrypted))

    decrypted = my_IDEA.decrypt(cipher)
    assert decrypted == plain  # debug
    print('decrypted\t', hex(decrypted))


if __name__ == "__main__":
    main()
