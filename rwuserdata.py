import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import pickle
import os

def encrypt(key, source, encode=True):
    key = SHA256.new(key).digest()
    IV = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size
    source += bytes([padding]) * padding
    data = IV + encryptor.encrypt(source)
    return base64.b64encode(data).decode("latin-1") if encode else data

def decrypt(key, source, decode=True):
    if decode:
        source = base64.b64encode(source.encode("latin-1"))
    key = SHA256.new(key).digest()
    IV = source[:AES.block_size]
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])
    padding = data[-1]
    if data[-padding:] != bytes([padding]) * padding:
        raise ValueError("Invalid padding...")
    return data[:-padding]

def encryptObj(key, obj, path):
    byteObj = pickle.dumps(obj)
    encryptedObj = encrypt(key, byteObj, encode=False)
    with open(path, "wb") as file:
        pickle.dump(encryptedObj, file)

def decryptObj(key, path):
    if os.path.exists(path):
        with open(path, "rb") as file:
            file_cont = pickle.load(file)
        file_decrypted = decrypt(key, file_cont, decode=False)
        return pickle.loads(file_decrypted)
    else:
        raise Exception("File does not Exsist.")

