# -*-coding:UTF-8 -*
# !/usr/bin/env python

""" This module implements the IDEA algorithm
@see: https://en.wikipedia.org/wiki/International_Data_Encryption_Algorithm

# Interesting point
    > IDEA algorithm entirely avoids the use of any lookup tables or S-boxes.

# Supported key sizes:
    > 128-bit   X
    > 256-bit   X

# Supported modes of operation:
    > ECB - Electronic Codebook
    > CBC - Cipher-Block Chaining
    > PCBC - Propagating Cipher Block Chaining
    @see: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation
    @see: https://csrc.nist.gov/publications/detail/sp/800-38a/final
"""

from secrets import randbits
import hashlib
import textwrap

from core import block_feeder, utils


#########################
#                       #
#       FUNCTIONS       #
#                       #
#########################

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
    """
    :type a: int
    """
    if a == 0:
        a = 0x10000

    result = pow(a, 0x10001 - 2, 0x10001)
    return result


#########################
#                       #
#     IDEA CLASSES      #
#                       #
#########################

class IDEA(object):
    """
    This class is responsible for managing the encryption.
    It will generate subkeys and encrypt/decrypt the data.
    """

    def __init__(self, key=0x2BD6459F82C5B300952C49104881FF48, keylength=128):
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
            sub_keys.append((key >> ((self.keylength - 16) - 16 * (i % (self.keylength // 16)))) % 0x10000)  # slicing the key into X 16bits long parts
            if i % int(self.keylength // 16) == (self.keylength // 16) - 1:  # keylength = 128, i = {7, 15, 23, 31, 39, 47}
                # x << y basically returns x with the bits shifted to the left by y places, BUT new bits on the right-hand-side are replaced by zeros.
                # To obtain a clean permutation, we simply do (x << y) OR (x >> (len(x)-y))
                key = ((key << 25) | (key >> (self.keylength - 25))) % modulo

        # Each round uses 6 16-bit sub-keys, while the half-round uses 4,
        # Putting subkeys into tuples should ease the encryption.
        keys = []
        for i in range(9):  # 8.5 round => 9 tuples
            round_keys = sub_keys[6 * i: 6 * (i + 1)]
            keys.append(tuple(round_keys))
        self.subkeys = tuple(keys)

    def encrypt(self, plaintext):
        """ IDEA Encryption

        :param plaintext:
        :return: cipher: <int> encrypted text
        """
        B1 = (plaintext >> 48) & 0xFFFF  # 0xFFFF masc
        B2 = (plaintext >> 32) & 0xFFFF
        B3 = (plaintext >> 16) & 0xFFFF
        B4 = plaintext & 0xFFFF

        for i in range(8):
            K = self.subkeys[i]  # gathering necessary subkeys
            B1 = multiplication(B1, K[0])  # 1
            B2 = addition(B2, K[1])  # 2
            B3 = addition(B3, K[2])  # 3
            B4 = multiplication(B4, K[3])  # 4

            T1 = B1 ^ B3  # 5
            T2 = B2 ^ B4  # 6

            T1 = multiplication(T1, K[4])  # 7
            T2 = addition(T2, T1)  # 8
            T2 = multiplication(T2, K[5])  # 9
            T1 = addition(T1, T2)  # 10

            B1 = B1 ^ T2  # 11
            B3 = B3 ^ T2  # 12
            B2 = B2 ^ T1  # 13
            B4 = B4 ^ T1  # 14

            B2, B3 = B3, B2  # 15

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
        """ Generate decrypting subkeys

        :return: tuple(d_keys): <tuple(int)>
        """
        d_sub_keys = []
        K = self.subkeys[8]
        d_sub_keys.append(mul_inv(K[0]))
        d_sub_keys.append(-K[1] % 0x10000)
        d_sub_keys.append(-K[2] % 0x10000)
        d_sub_keys.append(mul_inv(K[3]))

        for i in reversed(range(8)):
            K = self.subkeys[i]
            d_sub_keys.append(K[4])  # KD(5) = K(47)
            d_sub_keys.append(K[5])  # KD(6) = K(48)
            # noinspection PyTypeChecker
            d_sub_keys.append(mul_inv(K[0]))  # KD(7) = 1/K(43)
            d_sub_keys.append(-K[2] % 0x10000)  # KD(8) = -K(45)
            d_sub_keys.append(-K[1] % 0x10000)  # KD(9) = -K(44)
            # noinspection PyTypeChecker
            d_sub_keys.append(mul_inv(K[3]))  # KD(10) = 1/K(46)

        d_keys = []
        for i in range(9):  # 8.5 round => 9 tuples
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
            B1 = multiplication(B1, KD[0])  # 1
            B2 = addition(B2, KD[1])  # 2
            B3 = addition(B3, KD[2])  # 3
            B4 = multiplication(B4, KD[3])  # 4

            T1 = B1 ^ B3  # 5
            T2 = B2 ^ B4  # 6

            T1 = multiplication(T1, KD[4])  # 7
            T2 = addition(T2, T1)  # 8
            T2 = multiplication(T2, KD[5])  # 9
            T1 = addition(T1, T2)  # 10

            B1 = B1 ^ T2  # 11
            B3 = B3 ^ T2  # 12
            B2 = B2 ^ T1  # 13
            B4 = B4 ^ T1  # 14

            B2, B3 = B3, B2  # 15

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


class IDEABlockModeOfOperation(object):
    """Mother class for IDEA modes of operation."""

    def __init__(self, key=0x5a14fb3e021c79e0608146a0117bff03, keylen=128):
        self._idea = IDEA(key, keylen)

    def encrypt(self, plaintext):
        pass

    def decrypt(self, ciphertext):
        pass


class IDEAModeOfOperationECB(IDEABlockModeOfOperation):
    """IDEA Electronic CodeBook Mode of Operation.

        > Block-cipher, data must be padded to 16 bytes boundaries
        > Warning: This mode can expose data patterns and tho is deprecated.
    """

    name = "Electronic Codebook (ECB)"

    def encrypt(self, plaintext):
        return self._idea.encrypt(plaintext)

    def decrypt(self, ciphertext):
        return self._idea.decrypt(ciphertext)


class IDEAModeOfOperationCBC(IDEABlockModeOfOperation):
    """IDEA Cipher-Block Chaining Mode of Operation.

         > Needs an Initialization Vector (IV)
         > Block-cipher, data must be padded to 16 bytes boundaries
         > Warning : Bad IV can cause block corruption.
    """

    name = "Cipher-Block Chaining (CBC)"

    def __init__(self, key, keylen, iv=15217303795843126513):
        if len(hex(iv)[2:]) != 16:
            raise ValueError("IV must be 16 Bytes long")
        else:
            self.last_cipherblock = iv

        IDEABlockModeOfOperation.__init__(self, key, keylen)

    def encrypt(self, plaintext):
        pre_cipherblock = (plaintext ^ self.last_cipherblock) % pow(2, 64)  # XOR IV
        self.last_cipherblock = self._idea.encrypt(pre_cipherblock)  # Encryption
        return self.last_cipherblock

    def decrypt(self, ciphertext):
        plaintext = (self._idea.decrypt(ciphertext) ^ self.last_cipherblock) % pow(2, 64)  # Decryption, then XOR IV
        self.last_cipherblock = ciphertext
        return plaintext


class IDEAModeOfOperationPCBC(IDEABlockModeOfOperation):
    """IDEA Cipher-Block Propagating Cipher Block Chaining.

        > IT'S DIFFERENT OK !
        > Block-cipher, data must be padded to 16 bytes boundaries
    """

    name = "Propagating Cipher-Block Chaining (PCBC)"

    def __init__(self, key, keylen, iv=15217303795843126513):
        if len(hex(iv)[2:]) != 16:
            raise ValueError("IV must be 16 Bytes long")
        else:
            self.last_cipherblock = iv
        IDEABlockModeOfOperation.__init__(self, key, keylen)

    def encrypt(self, plaintext):
        pre_cipherblock = (plaintext ^ self.last_cipherblock) % pow(2, 64)  # XOR IV
        ciphertext = self.last_cipherblock = self._idea.encrypt(pre_cipherblock)  # Encryption
        self.last_cipherblock = plaintext ^ self.last_cipherblock
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = (self._idea.decrypt(ciphertext) ^ self.last_cipherblock) % pow(2, 64)  # Decryption, then XOR IV
        self.last_cipherblock = ciphertext ^ plaintext
        return plaintext


#########################
#                       #
#     MAIN FUNCTIONS    #
#                       #
#########################

def idea_menu():
    """ Print menu and get user inputs

    :return: key_len: <int>, mod_of_encryption: <str>
    """
    key_len, mod_of_operation = 128, 'CBC'  # Setting default values

    # Menu 1 - keylen
    idea_menu_keylen = {
        '1-': "128 bits (DH/MD5)",
        '2-': "256 bits (DH/SHA3)"
    }
    # Menu 2 - ModeofOperation
    idea_menu_modOfOperation = {
        '1-': "ECB",
        '2-': "CBC",
        '3-': "PCBC"
    }

    # Choices
    loop_continue = True
    while loop_continue:
        options = idea_menu_keylen.keys()
        print("Choose Keylen (bits)")
        for entry in options:
            print(entry, idea_menu_keylen[entry])

        selection = input("> ")
        if selection == '1':
            key_len, loop_continue = 128, False
        elif selection == '2':
            key_len, loop_continue = 256, False
        else:
            print("Invalid Option, please retry\n")

    loop_continue = True
    while loop_continue:
        options = idea_menu_modOfOperation.keys()
        print("Choose Mode of Operation")
        for entry in options:
            print(entry, idea_menu_modOfOperation[entry])

        selection = input("> ")
        if selection == '1':
            mod_of_operation, loop_continue = 'ECB', False
        elif selection == '2':
            mod_of_operation, loop_continue = 'CBC', False
        elif selection == '3':
            mod_of_operation, loop_continue = 'PCBC', False
        else:
            print("Invalid Option, please retry\n")

    return key_len, mod_of_operation


def idea_main_encryption():
    """ Launch IDEA Encryption process """

    print("========================================IDEA ENCRYPTION========================================")
    key_len, mod_of_operation = idea_menu()

    print("-------------------------------------------PASSWORD-------------------------------------------")
    # key = diffie_hellman(1024, True)  # Launch Diffie Hellman with default values
    print("\033[1;34m[?]\033[1;m", "PASSWORD", "\x1b[0m", "(diffie-hellman shared key)")
    key = input("IDEA/> ")  # convert <srt> to <int>
    bytes_key = bytes.fromhex(key[2:])
    if key_len == 128:
        key = int.from_bytes(hashlib.md5(bytes_key).digest(), 'little')
    elif key_len == 256:
        key = int.from_bytes(hashlib.sha3_256(bytes_key).digest(), 'little')
    else:
        raise ValueError("Wrong key length value")
    # print('\033[91mKEY:', hex(key), '\x1b[0m')
    # input("Please Consider Saving this Key... (Press any Key)")

    print("---------------------------------------SELECTING A FILE---------------------------------------")
    filename = utils.get_filename()

    # filename = "C:/Users/antoine/Desktop/CryptoSystem/core/tests/idea_test.txt"
    print("File to encrypt:", filename)
    cypher_file = filename.split(".", 1)[0] + '.cypher'

    print("------------------------------------GATHERING FILE CONTENT------------------------------------")
    hex_message = utils.get_file_hex(filename)  # Getting the Hex
    pad = block_feeder.PKCS7_padding(hex_message)  # Padding
    file_blocks = block_feeder.generate_blocks(pad)  # Generating Blocks
    print("File Blocks: {0}\n{1}\n{2}\n...".format(file_blocks[:3], file_blocks[3:7], file_blocks[7:11]))

    print("------------------------------------------ENCRYPTION------------------------------------------")
    # Managing mode of operation
    if mod_of_operation is "ECB":
        idea = IDEAModeOfOperationECB(key, key_len)
    elif mod_of_operation is "CBC":
        # iv = secrets.randbits(64)    # 16 hex long = 64 bits  # works with static iv
        idea = IDEAModeOfOperationCBC(key, key_len)
    elif mod_of_operation is "PCBC":
        # iv = secrets.randbits(64)    # 16 hex long = 64 bits  # works with static iv
        idea = IDEAModeOfOperationPCBC(key, key_len)
    else:
        raise ValueError("Wrong Mode of Operation.")

    # Encryption (It's about time)
    output = ''
    for i in range(len(file_blocks)):
        encrypted = idea.encrypt(file_blocks[i])
        output += hex(encrypted)[2:].zfill(16)

    wrap = textwrap.fill(output, 94)
    print(wrap)

    print("----------------------------------CREATE ENCRYPTED FILE-----------------------------------")
    utils.wipe_file(cypher_file)  # Clean cypher file if it already exist
    with open(cypher_file, mode='a') as file:
        file.write(output)
    print("\x1b[6;30;42mCypher successfully created\x1b[0m")

    return 0


def idea_main_decryption():
    """ Launch IDEA Decryption process """

    print("========================================IDEA DECRYPTION========================================")
    key_len, mod_of_operation = idea_menu()

    print("---------------------------------------SELECTING A FILE---------------------------------------")
    filename = utils.get_filename()
    print("File to Decrypt:", filename)

    print("------------------------------------GATHERING FILE CONTENT------------------------------------")
    hex_message = utils.get_file_hex(filename)
    true_hex_message = bytes.decode(
        bytes.fromhex(hex_message))  # one more decoding step due to how the file is open ('rb')
    file_blocks = block_feeder.generate_blocks(true_hex_message)
    print("File Blocks: {0}\n{1}\n{2}\n...".format(file_blocks[:3], file_blocks[3:7], file_blocks[7:11]))

    print("-------------------------------------------PASSWORD-------------------------------------------")
    print("Please type-in the Hexadecimal password given during the encryption process")
    # key = int(input("> "), 16)
    key = input("IDEA/> ")
    bytes_key = bytes.fromhex(key[2:])
    if key_len == 128:
        key = int.from_bytes(hashlib.md5(bytes_key).digest(), 'little')
    elif key_len == 256:
        key = int.from_bytes(hashlib.sha3_256(bytes_key).digest(), 'little')
    else:
        raise ValueError("Wrong key length value")

    print("------------------------------------------DECRYPTION------------------------------------------")
    # Managing mode of operation
    if mod_of_operation is "ECB":
        idea = IDEAModeOfOperationECB(key, key_len)
    elif mod_of_operation is "CBC":
        # iv = secrets.randbits(64)    # 16 hex long = 64 bits  # works with static iv
        idea = IDEAModeOfOperationCBC(key, key_len)
    elif mod_of_operation is "PCBC":
        # iv = secrets.randbits(64)    # 16 hex long = 64 bits  # works with static iv
        idea = IDEAModeOfOperationPCBC(key, key_len)
    else:
        raise ValueError("Wrong Mode of Operation.")

    # Decryption
    output = ''
    for i in range(len(file_blocks)):
        decrypted = idea.decrypt(file_blocks[i])
        decrypted = hex(decrypted)[2:].zfill(16)  # keeping the right format
        output += decrypted

    unpadded = block_feeder.PKCS7_unpadding(output)
    try:
        unpadded_to_bytes = bytes.fromhex(unpadded)

        wrap = textwrap.fill(str(unpadded_to_bytes)[2:], 94)
        print(wrap)

        print("----------------------------------SAVING DECRYPTED TEXT-----------------------------------")
        new_file = input("Enter a file name: ")
        utils.write_file(new_file + ".txt", unpadded_to_bytes)
    except:
        print("It seems like you entered the wrong Password")

    return 0


# TEST ZONE
if __name__ == "__main__":
    # idea_main_encryption()
    idea_main_decryption()

    # During password (/key generation step) :
    # bytes_key = key.to_bytes((key.bit_length() + 7) // 8, 'little')  # key from <int> to <bytes> (compatibility with hashlib functions)

    # LA KLAIENT = 0x5863a453b9fd82254950770b9b7ac6b7
    # Prime = 0x4781248c843906b0ce31ab07d62e968a6b7e8c17ecdfdd4b6b78aafbc13030cde610e0aea6ce35e1d39fbf8cc6fd98caee79f83f8fc1a04d7ef2db74e02ecaabd668385c9c8b4f62d9c1ad761601e040716494cad09cde8885bea8307a82032f037440cdc2976593d142eb70e83475839a3d089cbb0ed274b994e9c7d6b5c323
    pass
