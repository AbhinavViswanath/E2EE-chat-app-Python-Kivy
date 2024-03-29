import json
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
def aes256encrypt(message):
    # header = b"header"
    # data = b"secret"
    message = message.encode()
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_GCM)
    # cipher.update(header)
    ciphertext, tag = cipher.encrypt_and_digest(message)
    print(cipher, type(cipher))
    # json_k = ['key', 'nonce', 'header', 'ciphertext', 'tag' ]
    json_k = ['key', 'nonce', 'ciphertext', 'tag' ]
    json_v = [ b64encode(x).decode('utf-8') for x in (key, cipher.nonce, ciphertext, tag) ]
    result = json.dumps(dict(zip(json_k, json_v)))
    return result
    # print(key, result)
    #'result' string is to be passed as json_input to decrypt program, along with the key