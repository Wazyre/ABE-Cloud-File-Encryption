from KPABE import EKPabe
import json
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
with open('test.txt', 'rb') as file:
    file_contents = file.read()
    #print(file_contents)



def main():
    groupObj = PairingGroup('MNT224')
    kpabe = EKPabe(groupObj)

    attributes = [ 'ONE', 'TWO', 'THREE', 'FOUR' ]

    (pk, mk) = kpabe.setup(attributes)

    # policy = '(ONE or THREE) and (THREE or TWO)'
    policy = 'THREE and (ONE or TWO)'
    msg = file_contents

    mykey = kpabe.keygen(pk, mk, policy)

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