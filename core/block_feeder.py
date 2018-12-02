# -*-coding:UTF-8 -*
# !/usr/bin/env python

""" This module do things

"""

import binascii

from GS15.IDEA.idea import IDEA


def generate_test_file():
    pass

#########################
#                       #
#        OTHERS         #
#                       #
#########################


def get_file_hex(file_name='test.txt'):
    """ ...
    :return: fileHex: <bytes>
    """
    with open(file_name, 'rb') as file_alias:
        content = file_alias.read()
    # file_hex = binascii.hexlify(content)  # bytes
    file_hex = content.hex()

    return file_hex


def ceil_div(a, b):
    return -(-a // b)


def generate_block():
    file_hex = get_file_hex()
    len_hex = len(file_hex)

    # Padding PKCS#7
    # k - (input_len mod k) octets all having value k - (input_len mod k)
    for i in range(16 - (len_hex % 16)):
        file_hex += format(16 - (len_hex % 16), 'x')

    # Dividing file hex
    hex_blocks = []
    num_blocks = ceil_div(len_hex, 16)
    for i in range(num_blocks):
        to_int = int(file_hex[i*16:16+i*16], 16) # THIS CAN GENERATE ERROR
        hex_blocks.append(to_int)
        # print(hex(hex_blocks[i])[2:])
    assert num_blocks == len(hex_blocks)

    return hex_blocks


def encryption_feed(key, blocks, output_file='Output.txt'):
    # erase file content if it already exists
    with open(output_file, encoding='utf-8', mode='w') as file:
            file.write("")

    my_IDEA = IDEA(key, 128)

    for i in range(len(blocks)):
        encrypted = my_IDEA.encrypt(blocks[i])
        encrypted = hex(encrypted)[2:].zfill(16) # formatage
        with open('Output.txt', mode='a') as file:
            file.write(encrypted)

# Test
if __name__ == '__main__':
    key = 0x5a14fb3e021c79e0608146a0117bff03

    # encryption
    blocks = generate_block()  # extraction + padding + spliting in multiple blocks
    encryption_feed(key, blocks)
    with open('Output.txt', 'r') as file_alias:
        enc_file_hex = file_alias.read()

    # decryption
    # Dividing file into multiple 16octet parts
    len_hex = len(enc_file_hex)
    crypt_hex_blocks = []
    num_blocks = ceil_div(len_hex, 16)
    for i in range(num_blocks):
        to_int = int(enc_file_hex[i*16:16+i*16], 16)  # THIS CAN GENERATE ERROR
        crypt_hex_blocks.append(to_int)
    assert num_blocks == len(crypt_hex_blocks)

    # pure decryption
    decrypted_blocks = []
    my_IDEA = IDEA(key, 128)
    for i in range(len(crypt_hex_blocks)):
        decrypted = my_IDEA.decrypt(crypt_hex_blocks[i])
        decrypted = hex(decrypted)[2:].zfill(16) # formatage
        decrypted_blocks.append(decrypted)

    print(blocks)
    print(decrypted_blocks)

    # unpadding

    # encoding it to UTF-8 and write into file

    pass

# int.from_bytes( bytes, byteorder, *, signed=False )
# fileString = fileHex.decode("UTF-8")
# int.from_bytes(b'\x00\x10', byteorder='little')

#############################################################################################################################################
## Naming convention  : Pythono PEP 8 ####
#
# module_name, package_name
# ClassName,
# method_name, ExceptionName, function_name,
# GLOBAL_CONSTANT_NAME, CLASS_CONSTANT_NAME, global_var_name, instance_var_name, function_parameter_name, local_var_name
