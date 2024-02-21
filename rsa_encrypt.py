import rsa
def rsa_encrypt(message):
    (publickey, privatekey) = rsa.newkeys(1024)
    
