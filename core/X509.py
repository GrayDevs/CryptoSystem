# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime


class Certificate(object):
    """ This class is responsible for managing the certificates. """

    def __init__(self):
        pass

    def new_certificate(self, public_key):

        data = {
            'version_number': 3,
            'serial_number': 0x10e6fc62b7418ad5005e45b6, # Generating
            'signature_algorithm_ID': "sha3WithRSAEncryption",
            'issuer_name': "C=FR, O=UTT",
            'validity_period': [
                {'not_before': datetime.now()},
                {'not_after':  datetime.now().replace(datetime.now().year + 1)}
            ],
            'subject_name': "C=FR, L=Troyes, O=GS15",
            'subject_public_key_info': [
                {'public_key_algorithm': "id-RSAPublicKey, 1024 bits"},
                {'Subject_public_key': 0x00c92269318ad66ceadac37f2caca5afc002ea81cb65b9fd0c6d465bc91e9d3bef},
            ],
        }

        signature = 0x8bc3edd19d396faf4072bd1e185e30542335

        certificate = (data, signature)
        return certificate

if __name__ == "__main__":


    pass
