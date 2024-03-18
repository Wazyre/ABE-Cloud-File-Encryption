
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.symcrypto import SymmetricCryptoAbstraction
from charm.toolbox.ABEnc import ABEnc
from charm.schemes.abenc.abenc_lsw08 import KPabe
from charm.core.math.pairing import hashPair as extractor
from time import clock
from share import *


debug = False
class EKPabe(ABEnc):
    """
    >>> from charm.toolbox.pairinggroup import PairingGroup,GT
    >>> group = PairingGroup('MNT224')
    >>> kpabe = EKPabe(group)
    >>> attributes = [ 'ONE', 'TWO', 'THREE', 'FOUR' ]
    >>> (master_public_key, master_key) = kpabe.setup(attributes)
    >>> policy = '(ONE or THREE) and (THREE or TWO)'
    >>> secret_key = kpabe.keygen(master_public_key, master_key, policy)
    >>> msg = b"Some Random Message"
    >>> cipher_text = kpabe.encrypt(master_public_key, msg, attributes)
    >>> decrypted_msg = kpabe.decrypt(cipher_text, secret_key)
    >>> decrypted_msg == msg
    True
    """

    def __init__(self, groupObj, verbose=False):
        ABEnc.__init__(self)
        global group, util
        group = groupObj
        util = SecretUtil(group, verbose)        

    def setup(self, attributes):
        s = group.random(ZR)
        g = group.random(G1)
        
        self.attributeSecrets = {}
        self.attribute = {}
        for attr in attributes:
            #si = group.random(ZR)
            #self.attributeSecrets[attr] = si
            self.attribute[attr] = g
        return (g**s, s) # (pk, mk)
    
    def keygen(self, mk, policy_str):
        policy = createPolicy(policy_str)  
        attr_list = util.getAttributeList(policy)
        s = mk
        shares = {}
        accstruct = LSSS(policy)
        share = 0
        for key in accstruct:
            for line in accstruct[key]:
                share += line
            share = (share*s)
            shares[key] = share
            share = 0
        #print(shares)
        d = {}
        D = { 'policy': policy_str, 'Du': d }
        for x in attr_list:
            y = util.strip_index(x)
            d[y] = self.attribute[y] ** shares[x]
            if debug: print(str(y) + " d[y] " + str(d[y]))
        if debug: print("Access Policy for key: %s" % policy)
        if debug: print("Attribute list: %s" % attr_list)
        print(D)
        return D
    
    def encrypt(self, pk, M, attr_list): 
        if debug: print('Encryption Algorithm...')
        #k = group.random(ZR)
        Cs = pk
        #print("Cs:", Cs)
        """Ci = {}
        for attr in attr_list:
            Ci[attr] = self.attribute[attr] ** k"""
        
        symcrypt = SymmetricCryptoAbstraction(extractor(Cs))
        C = symcrypt.encrypt(M)
        
        return { 'C': C, 'attributes': attr_list }
    
    def decrypt(self, C, D):
        policy = util.createPolicy(D['policy'])
        print("policy:",policy)
        attrs = util.prune(policy, C['attributes'])
        if attrs == False:
            return False
        
        
        Z = {}
        prodT = 1
        for i in range(len(attrs)):
            x = attrs[i].getAttribute()
            y = attrs[i].getAttributeAndIndex()
            Z[y] = D['Du'][x]
            prodT *= Z[y]
        #print("prodT:", prodT)
        symcrypt = SymmetricCryptoAbstraction(extractor(prodT))
        
        return symcrypt.decrypt(C['C'])

def main():
    groupObj = PairingGroup('MNT224')
    kpabe = EKPabe(groupObj)

    attributes = [ 'ONE', 'TWO', 'THREE', 'FOUR' ]

    (pk, mk) = kpabe.setup(attributes)

    # policy = '(ONE or THREE) and (THREE or TWO)'
    policy = 'THREE and (ONE or TWO)'
    msg = b"Some Random Message"
    if debug: print(msg)
    mykey = kpabe.keygen(mk, policy)
    if debug: print("mykey", mykey)
    if debug: print("Encrypt under these attributes: ", attributes)
    ciphertext = kpabe.encrypt(pk, msg, attributes)
    if debug: print(ciphertext)

    rec_msg = kpabe.decrypt(ciphertext, mykey)
    assert rec_msg
    if debug: print("rec_msg=%s" % str(rec_msg))

    assert msg == rec_msg
    if debug: print("Successful Decryption!")



if __name__ == "__main__":
    debug = True
    main()
    #benchmark()