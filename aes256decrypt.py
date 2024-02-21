import json
from base64 import b64decode
from Crypto.Cipher import AES

def aes256decrypt(message):
    # We assume that the key was securely shared beforehand
    try:
        # json_input = '{"key": "4C1f8sJbljYhKQjEwAKs7w==", "nonce": "/LrTGZ2ZZWxFJblfSZcL5w==", "ciphertext": "tpA6CwsEQ8s794vplSTO7ZGqPgnKHmKlVA+py2GKmQc=", "tag": "MayxMH/dOipL9SHLYCSgdw=="}'
        json_input = message
        b64 = json.loads(json_input)
        # json_k = ['key', 'nonce', 'header', 'ciphertext', 'tag' ]
        json_k = ['key', 'nonce', 'ciphertext', 'tag' ]
        jv = {k:b64decode(b64[k]) for k in json_k}

        key = jv['key']
        cipher = AES.new(key, AES.MODE_GCM, nonce=jv['nonce'])
        # cipher.update(jv['header'])
        plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
        # print("The message was: " + plaintext.decode('utf-8'))
        plaintext = plaintext.decode()
        return plaintext
    except (ValueError, KeyError):
        print("Incorrect decryption")