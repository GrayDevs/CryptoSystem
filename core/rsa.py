
""" RSA (Rivest-Shamir-Adelman) function implementation.

https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Code
"""

from core import utils


class RSA(object):
    """ / """

    def __init__(self, keysize=2048):
        """ / """
        self.keysize = keysize
        pass

    def generate(self):
        """ Generate a k-bit RSA public/private key pair
        @see https://en.wikipedia.org/wiki/RSA_(cryptosystem)

        :param: keysize: <int> - bitlength of desired RSA modulus n (should be even)
        :return: Result of RSA generation (<int> triplet)
        """

        # Variables for key generation
        e=0x10001  # use fixed public exponent
        # p, q, carmichael = 0, 0, 0

        # generate p and q such that Carmichael(n) = lcm(p-1, q-1) is coprime with e
        # and |p-q| >= 2^(keysize/2 -100)
        p = utils.prime_gen(self.keysize // 2)
        q = utils.prime_gen(self.keysize // 2)
        carmichael = utils.lcm(p-1, q-1)
        while (utils.gcd(e, carmichael) != 1) or (abs(p-q) < pow(2, (self.keysize // 2 - 100))):
            p = utils.prime_gen(self.keysize // 2)
            q = utils.prime_gen(self.keysize // 2)
            carmichael = utils.lcm(p-1, q-1)
            # print(utils.gcd(e, carmichael))
        # print("*** Primes:\np=%d\nq=%d" % (p, q))

        n = p*q                             # Public Key (I)
        # e                                 # Public Key (Part II)
        d = utils.mod_inv(e, carmichael)    # Private Key : d = e^(-1) mod Carmichael(n)
        assert d*e % carmichael == 1
        return n, e, d

    def encrypt(self, message, e, n):
        """ RSA Encryption

        :param message: <int> - the message to be encrypted
        :param e: <int> - e value returned from RSA.generate() (public key II)
        :param n: <int> - n value returned from RSA.generate() (public key I)
        :return: <int> - encrypted message
        """
        return pow(message, e, n)  # c(m) = m^(e) % n

    def decrypt(self, cypher, d, n):
        """ RSA Decryption

        :param cypher: <int> - the message to be decrypted (encrypted with RSA.encrypt())
        :param d: <int> - d value returned from RSA.generate() (private key)
        :param n: <int> - n value returned from RSA.generate() (public key I)
        :return: <int> - decrypted message
        """
        return pow(cypher, d, n)  # m(c) = c^(d) % n


if __name__ == "__main__":
    message = int(input("Entrez un nombre: "))      # message
    rsa = RSA(2048)                                 # Creating an object
    n, e, d = RSA.generate(rsa)                     # Generating the key
    cypher = RSA.encrypt(rsa, message, e, n)        # Encryption
    plain_text = RSA.decrypt(rsa, cypher, d, n)     # Decryption

    print("***KEY PAIR:\nn={0}\ne={1}\nd={2}".format(n, e, d))
    print("***RSA RESULTS:\nmessage={0}\ncypher={1}\nplain={2}".format(message, cypher, plain_text))
    assert message == plain_text
    print("\n*OPERATION SUCCESSFULL*")
    pass
