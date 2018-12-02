# -*-coding:UTF-8 -*
# !/usr/bin/env python

""" Implémentation de Diffie-Hellman
___________________________________________________
RFCs :
@see https://tools.ietf.org/html/rfc2409#section-6
@see https://tools.ietf.org/html/rfc5114#section-2.1
"""

import secrets
import math
from time import process_time
from GS15.DH import utils


#########################
#                       #
#    PRIME GENERATOR    #
#                       #
#########################

def prime_gen(bit_len=1024):
    t = process_time()
    probably_prime = 0
    while not utils.rabin_miller(probably_prime):
        probably_prime = secrets.randbits(bit_len)

    print("Prime successfully generated in", process_time() - t)
    return probably_prime


#########################
#                       #
#    PRIMITIVE ROOTS    #
#                       #
#########################

def prim_roots(Zp):
    """
    Generate the prime roots for Zp
    :param Zp: <int> - modulo
    :return:
    """
    # 2) Calcul de ses diviseurs premier (on vérifie qu'aucun de divise m)
    coprime_list = {num for num in range(1, Zp) if math.gcd(num, Zp) == 1}
    print("coprime_list successfuly generated")
    # 4) Calcul de m^(φ(n)/p)[n] in range(1,...,k)
    roots = [i for i in range(1, Zp) if coprime_list == {pow(i, powers, Zp) for powers in range(1, Zp)}]
    # rand_root = roots[secrets.randbelow(len(roots))]

    return roots  # rand_root


#########################
#                       #
#    Diffie-Hellman     #
#                       #
#########################

def diffie_hellman(p_len=1024, std=True):
    """ Local Diffie-Hellman implementation

    Process :
    1. Alice choisit un entier premier (grand), noté p;
    2. Alice cherche un générateur g du corps Zp; (g)
    3. Alice choisit un entier a ∈ Zp et calcule A=g^a;
        => ce résultat est envoyé à Bob;
    4. Bob choisit un entier b ∈ Zp et calcule B = g^b
        => Ce résultat est envoyé à Alice
    5. Alice et Bob calcul B^a et A^b, les deux résultats étant égaux : la clé !
        (B^a = A^b = g * (a*b)

    :param p_len: <int> - bit-length of prime number
    :param std: <boolean> - use standard prime or generate new one
    :return: a_key: <int>
    """

    if std:
        if p_len == 1024:  # 160-bit prime order subgroup
            #  https://tools.ietf.org/html/rfc5114#section-2.1
            p = 0xB10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371
            g = 0xA4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5
            # q = 0xF518AA8781A8DF278ABA4E7D64B7CB9D49462353
        if p_len == 2048:  # 224-bit prime order subgroup
            p = 0xAD107E1E9123A9D0D660FAA79559C51FA20D64E5683B9FD1B54B1597B61D0A75E6FA141DF95A56DBAF9A3C407BA1DF15EB3D688A309C180E1DE6B85A1274A0A66D3F8152AD6AC2129037C9EDEFDA4DF8D91E8FEF55B7394B7AD5B7D0B6C12207C9F98D11ED34DBF6C6BA0B2C8BBC27BE6A00E0A0B9C49708B3BF8A317091883681286130BC8985DB1602E714415D9330278273C7DE31EFDC7310F7121FD5A07415987D9ADC0A486DCDF93ACC44328387315D75E198C641A480CD86A1B9E587E8BE60E69CC928B2B9C52172E413042E9B23F10B0E16E79763C9B53DCF4BA80A29E3FB73C16B8E75B97EF363E2FFA31F71CF9DE5384E71B81C0AC4DFFE0C10E64F
            g = 0xAC4032EF4F2D9AE39DF30B5C8FFDAC506CDEBE7B89998CAF74866A08CFE4FFE3A6824A4E10B9A6F0DD921F01A70C4AFAAB739D7700C29F52C57DB17C620A8652BE5E9001A8D66AD7C17669101999024AF4D027275AC1348BB8A762D0521BC98AE247150422EA1ED409939D54DA7460CDB5F6C6B250717CBEF180EB34118E98D119529A45D6F834566E3025E316A330EFBB77A86F0C1AB15B051AE3D428C8F8ACB70A8137150B8EEB10E183EDD19963DDD9E263E4770589EF6AA21E7F5F2FF381B539CCE3409D13CD566AFBB48D6C019181E1BCFE94B30269EDFE72FE9B6AA4BD7B5A0F1C71CFFF4C19C418E1F6EC017981BC087F2A7065B384B890D3191F2BFA
            # q = 0x801C0D34C58D93FE997177101F80535A4738CEBCBF389A99B36371EB
    else:
        # p = prime_gen(p_len)
        p = 17
        g = prim_roots(p)

    a_private = secrets.randbelow(pow(2, 256))
    b_private = secrets.randbelow(pow(2, 256))

    a_public = pow(g, a_private, p)
    b_public = pow(g, b_private, p)

    a_key = pow(b_public, a_private, p)
    b_key = pow(a_public, b_private, p)
    assert a_key == b_key

    return a_key


if __name__ == "__main__":
    key = diffie_hellman(1024, True)
    print(key)

    pass
