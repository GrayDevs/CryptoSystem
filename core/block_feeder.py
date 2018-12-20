# -*-coding:UTF-8 -*
# !/usr/bin/env python

""" This module do things """

from core import utils


#########################
#                       #
#       PADDING         #
#                       #
#########################

def PKCS7_padding(hex_message):
    """ Padding PKCS#7
    k - (input_len mod k) octets all having value k - (input_len mod k)

    :param: hex_message: <str> - hexadecimal message
    :return: hex_message: <str> - padded hexadecimal message
    """
    len_message = len(hex_message)

    for i in range(16 - (len_message % 16)):
        hex_message += format(16 - (len_message % 16), 'x')

    assert len(hex_message) % 16 == 0  # Checking if padding is successful
    return hex_message


def PKCS7_unpadding(hex_message):
    """ Unpadding PKCS#7
    k - (input_len mod k) octets all having value k - (input_len mod k)

    :param hex_message: <str> - padded hexadecimal message
    :return: <str> -  unpadded hexadecimal message
    """
    # Getting last character of the chain
    k = hex_message[-1]

    # Converting it to int
    try:
        k = int(k ,16)
    except:
        print("Conversion Error during the un-padding operation")

    # Removing the pad
    return hex_message[:len(hex_message) - k]


#########################
#                       #
#    BLOCK GENERATOR    #
#                       #
#########################

def generate_blocks(hex_message):
    """ Dividing a hex message into multiple blocks and convert those into integer

    :param hex_message: <str> - string of hexadecimal data (needs to be padded)
    :return: blocks: <list> - usable values for idea, ...
    """
    assert len(hex_message) % 16 == 0
    blocks = []
    for i in range(len(hex_message) // 16):
        to_int = int(hex_message[i * 16:16 + i * 16], 16)  # Risky move here
        blocks.append(to_int)

    return blocks


# Test
if __name__ == '__main__':
    hex_message = utils.get_file_hex('tests/idea_test.txt')   # Getting the Hex
    pad = PKCS7_padding(hex_message)                          # Padding
    blocks = generate_blocks(pad)                             # Generating Blocks

    pass

#content_as_int = int.from_bytes(content_as_bytes, 'little')  # to little endians
#bin_content = bin(content_as_int)[2:]

# print(content.decode('utf-8'))

# int.from_bytes( bytes, byteorder, *, signed=False )
# fileString = fileHex.decode("UTF-8")
# int.from_bytes(b'\x00\x10', byteorder='little')
