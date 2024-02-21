import json
from base64 import b64decode
from Crypto.Cipher import AES

# We assume that the key was securely shared beforehand
try:
    json_input = '{"key": "k5uXOpFd8QfAmh0R8DQneg==", "nonce": "w1Nm6njoIW+S9HeJLyz/zQ==", "header": "aGVhZGVy", "ciphertext": "CznNqpFEF77oeySd4JTjBCjcp/KhwNLBiBN9rg9SQJ0=", "tag": "qMDS1m0YDn/lpShirViYQg=="}'
    b64 = json.loads(json_input)
    json_k = ['key', 'nonce', 'header', 'ciphertext', 'tag' ]
    jv = {k:b64decode(b64[k]) for k in json_k}

    key = jv['key']
    cipher = AES.new(key, AES.MODE_GCM, nonce=jv['nonce'])
    cipher.update(jv['header'])
    plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
    print("The message was: " + plaintext.decode('utf-8'))
except (ValueError, KeyError):
    print("Incorrect decryption")