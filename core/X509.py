# -*- coding: utf-8 -*-

import hashlib
import textwrap
from datetime import datetime
import secrets

from core.rsa import RSA

""" Implementation of basics signature system based on the X509 standard

* TODO *

- Completing certificate Data (with issuer things, ...)
- Actually use those Data (checking validity period, ...)
- Implement PKI things such as:
    - Saving Certficate Object
    - Revoke lists
    - etc...
- Uses JSON (maybe)
"""

#########################
#                       #
#      CERTIFICATE      #
#                       #
#########################

class Certificate(object):
    """ This class is responsible for managing the certificates. """

    def __init__(self, subject_public_key):
        """ class constructor

        :param subject_public_key: [A, g, p (,Su)] <list>
        """
        self.subject_public_key = subject_public_key
        self.data = {}  # init
        self.data_hash = ''  # init
        self.new_certificate()
        pass

    def new_certificate(self):
        """ Generate the necessary data for a new certificate"""

        self.data = {
            'version_number': 3,
            'serial_number': hex(secrets.randbits(70)).zfill(20),  # Generating
            'signature_algorithm_ID': "sha3WithRSAEncryption",
            'validity_period': [
                {'not_before': datetime.now()},
                {'not_after': datetime.now().replace(datetime.now().year + 1)}
            ],
            'subject_name': "C=FR, L=Troyes, O=GS15",
            'subject_public_key_info': [
                {'public_key_algorithm': "id-RSAPublicKey, 2048 bits"},
                {'Subject_public_key': self.subject_public_key},
            ],
        }

        # Signing the certificate
        self.data_hash = '0x' + hashlib.sha3_256(str(self.data).encode('utf-8')).hexdigest()

        pass

    def integrity_check(self):
        data_hash = '0x' + hashlib.sha3_256(str(self.data).encode('utf-8')).hexdigest()
        if self.data_hash == data_hash:
            print("\033[1;32m[+]\033[1;m \x1b[0mCERTIFICATE INTEGRITY CHECK SUCCESSFUL")
        else:
            raise ValueError("\033[1;31m[-] CERTIFICATE INTEGRITY ERROR \033[1;m \x1b[0m")
        pass

    def signing_public_key(self, d, n):
        """ RSA Signature process

        :param d: <int> - private key
        :param n: <int> - public key (part I)
        """
        if len(self.subject_public_key) != 3:
            raise ValueError("\033[1;31m[-]\033[1;m \x1b[0mThe public key has already been signed")

        signature = RSA().encrypt(self.subject_public_key[0], d, n)
        self.subject_public_key.append(signature)
        pass

    def pk_signature_check(self, n, e):
        """ RSA Signature Verification process

        :param n: <int> - public key (part I)
        :param e: <int> - public key (part II)
        :return:
        """

        if len(self.subject_public_key) != 4:
            raise ValueError("\033[1;31m[-]\033[1;m \x1b[0mThe public key hasn't been signed\x1b[0m")

        decrypt = RSA().decrypt(self.subject_public_key[3], e, n)
        if self.subject_public_key[0] == decrypt:
            print("\033[1;32m[+]\x1b[0m Signature successfully verified")
        else:
            raise ValueError("\033[1;31m[-] \x1b[0mAn Error occure during the Signature Verification")
        pass


#########################
#                       #
#     UTT FUNCTIONS     #
#                       #
#########################

def UTT_Keys():
    """ UTT keys uses for signing certificates

    :return:
    """
    n = 1377509098008480396127958303819748433992949105181377053140915891376695195883290778221218088933434962641973110015445353418542569309002067115686248571002867189875217936404182802544731910461799455768010892400854168964736401754570445438641929199621147242389260768483864796511842511995505453651626335564527176888448927257182162891637497794363979001504448653142166088741568698662999277614491789821278421843862664666539304146276411982745178033236600257029151419927641556768990923858522467633561139237526453872497837105060069739337300261981819229092271970867556634847421738664731446368101923316045696830444511280987189062459
    e = 65537
    d = 190104536932384774139483328179466785346433742493751083466332205922708083970374344929151578579404802166948834910580214214779563729118958695512829015677181321983404925855739984399893613747528040308433015187138952518448485369626507068828248602254809744629593497116931125197237584871802936899036184018392145679034415203329144901072654601882084269449563972156700365310051854683440509827884157816995816274520217554951745117281220104019495384335953066813768105976095544280101713101181787149951134738704579538572139893603098294271329250298914673572078731179141664342050434426309395830527141022637844333071775999920254211017
    return n, e, d


def UTT_Signature(certificate):
    """ UTT is a trusted third party
    This function allows it to "sign" a certificate (adding it's signature to the public key)

    :type certificate: Certificate
    """
    n, e, d = UTT_Keys()
    certificate.signing_public_key(d, n)
    assert len(certificate.subject_public_key) == 4
    print("\033[1;32m[+]\x1b[0m Certificate Successfuly Signed by UTT")
    pass


# TEST ZONE
if __name__ == "__main__":
    """
    # Process Certificat :
    # 1) Alice crée un certificat (avec sa clé publique) et l'envoie à l'UTT
    # 2) L'UTT signe A avec RSA (sa clé privé u) et obtient Su
    #    |-> Su est ajouté à sa clé publique d'alice : (A, g, p, Su)
    # 4) Alice envoie sa clé publique (certificat) à Bob
    # 6) Bob récupère la clé publique de l'UTT
    # 8) Bob déchiffre Su avec U et vérifie que le résultat soit égale à A 
    """

    # Alice do things
    alice_public_key = [
        90779587712507862442748289529535431344913230003114226416420162003348238866135784051214937565216847644100296499214182449570456040044057986423938704896792732613354086607713637008343756922632950562377271698122597265755324212834070825425399438807630409010150747600848338965233992108325360704963443363685215413023,
        115740200527109164239523414760926155534485715860090261532154107313946218459149402375178179458041461723723231563839316251515439564315555249353831328479173170684416728715378198172203100328308536292821245983596065287318698169565702979765910089654821728828592422299160041156491980943427556153020487552135890973413,
        124325339146889384540494091085456630009856882741872806181731279018491820800119460022367403769795008250021191767583423221479185609066059226301250167164084041279837566626881119772675984258163062926954046545485368458404445166682380071370274810671501916789361956272226105723317679562001235501455748016154805420913
    ]
    # Alice is getting her certificate
    alice_cert = Certificate(alice_public_key)

    # UTT's job
    UTT_Signature(alice_cert)

    # Bob's part
    utt_n, utt_e = UTT_Keys()[:2]
    wrap_n = textwrap.fill(hex(utt_n), 94, initial_indent="\t", subsequent_indent="\t\t")
    print("\033[1;97m[~]\x1b[0m UTT Public Keys:\n\tn:{0}\n\te:\t{1}".format(wrap_n, hex(utt_e)))
    alice_cert.pk_signature_check(utt_n, utt_e)

    pass
