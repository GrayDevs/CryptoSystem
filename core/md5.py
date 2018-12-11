# -*- coding: utf-8 -*-

""" Message Digest version 5 (MD5) Hash algorithm
@ see https://tools.ietf.org/html/rfc1321
@ see https://en.wikipedia.org/wiki/MD5

Warning :
> md5 has known hash collision weaknesses
"""

import hashlib
from math import ceil  # , floor, sin


# left-rotate function definition
def left_rotate(x, c):
    return (x << c) | (x >> (32 - c))


# NOT x = x XOR mask
def bitwise_not(x):
    return x ^ 0x11111111


def md5(message):
    """ md5 algorithm
    # Note: All variables are unsigned 32 bit and wrap modulo 2^32 when calculating

    :param message: <int>
    :return: digest: <str> (hex) - 128bits hash
    """
    # K, S = {}, []
    # S specifies the per-round shift amounts
    S = [
        7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
        5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
        4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
        6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21
    ]
    '''
    # Use binary integer part of the sines of integers (Radians) as constants:
    for i in range(64):
        K[i] = floor(pow(2, 32) * abs(sin(i + 1)))
    '''
    # Or just use Precomputed table :
    K = {
        0: 3614090360, 1: 3905402710, 2: 606105819, 3: 3250441966, 4: 4118548399,
        5: 1200080426, 6: 2821735955, 7: 4249261313, 8: 1770035416, 9: 2336552879,
        10: 4294925233, 11: 2304563134, 12: 1804603682, 13: 4254626195, 14: 2792965006,
        15: 1236535329, 16: 4129170786, 17: 3225465664, 18: 643717713, 19: 3921069994,
        20: 3593408605, 21: 38016083, 22: 3634488961, 23: 3889429448, 24: 568446438,
        25: 3275163606, 26: 4107603335, 27: 1163531501, 28: 2850285829, 29: 4243563512,
        30: 1735328473, 31: 2368359562, 32: 4294588738, 33: 2272392833, 34: 1839030562,
        35: 4259657740, 36: 2763975236, 37: 1272893353, 38: 4139469664, 39: 3200236656,
        40: 681279174, 41: 3936430074, 42: 3572445317, 43: 76029189, 44: 3654602809,
        45: 3873151461, 46: 530742520, 47: 3299628645, 48: 4096336452, 49: 1126891415,
        50: 2878612391, 51: 4237533241, 52: 1700485571, 53: 2399980690, 54: 4293915773,
        55: 2240044497, 56: 1873313359, 57: 4264355552, 58: 2734768916, 59: 1309151649,
        60: 4149444226, 61: 3174756917, 62: 718787259, 63: 3951481745
    }

    h0, h1, h2, h3 = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476

    # Pre-processing: padding
    # append "1" bit to message
    message = bin(message)[2:] + '1'
    original_message_len = len(message)  # grabing message len
    # append "0" bit until message length in bits ≡ 448 (mod 512)
    message = message.ljust(512 * ceil(original_message_len / 512) - 64, '0')
    # append original length on 64 bits to message
    message = message + str(bin(original_message_len)[2:].zfill(64))
    assert len(message) % 512 == 0

    # Process the message in successive 512-bit chunks:
    message_chunk = []
    for i in range(len(message) // 512):
        message_chunk.append(message[i * 512:512 + i * 512])
        # for each 512-bit chunk of padded message
        # break chunk into 16 32-bit words M[j], 0 ≤ j ≤ 15
        M = []
        for count in range(16):
            M.append(int(message_chunk[i][count * 32:32 + count * 32], 2))  # conversion to int
        assert len(M) == 16
        # Initialize hash value for this chunk:
        A, B, C, D = h0, h1, h2, h3
        # Main loop:
        for j in range(64):
            F, g = 0, 0
            if (0 <= j <= 15):
                F = (B & C) | ((~B) & D)  # F = D ^ (B & (C ^ D))
                g = j
            elif (16 <= j <= 31):
                F = (D & B) | ((~D) & C)  # F = (C ^ (D & (B ^ C)))
                g = (5 * j + 1) % 16
            elif (32 <= j <= 47):
                F = B ^ C ^ D
                g = (3 * j + 5) % 16
            elif (48 <= j <= 63):
                F = C ^ (B | (~D))
                g = (7 * j) % 16
            # print(i, j, F, F < 0x100000000, g)
            # Be wary of the below definitions of a,b,c,d
            F = (F + A + K[j] + M[g]) & 0xffffffff
            A = D
            D = C
            C = B
            B = (B + left_rotate(F, S[j])) & 0xffffffff
            assert F < 4294967296 and A < 4294967296 and B < 4294967296 and C < 4294967296 and D < 4294967296

        # Add this chunk's hash to result so far:
        h0 = (h0 + A) & 0xffffffff
        h1 = (h1 + B) & 0xffffffff
        h2 = (h2 + C) & 0xffffffff
        h3 = (h3 + D) & 0xffffffff

    digest = (hex(h0)[2:] + hex(h1)[2:] + hex(h2)[2:] + hex(h3)[2:]).zfill(32)
    return digest


if __name__ == "__main__":
    message = 'bonjour'
    result = hashlib.md5(str.encode(message, 'utf-8'))

    ################################################################################
    # message = input("Message to hash: ")
    message_as_bytes = str.encode(message, 'utf-8')  # to bytes
    message_as_int = int.from_bytes(message_as_bytes, 'little')  # to little endians
    hashier = md5(message_as_int)

    print(result.hexdigest())
    print(hashier)

    pass
