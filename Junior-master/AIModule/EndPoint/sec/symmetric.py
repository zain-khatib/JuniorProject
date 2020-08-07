from Crypto import Random
from Crypto.Cipher import AES
import os


class Encryptor:
    def __init__(self,key):
        self.key=key

    def pad(self,s):
        return s+b"\0"*(AES.block_size - len(s) % AES.block_size)

    def encrypt(self,message,key,key_size=32):
        message=self.pad(message)
        iv=Random.new().read(AES.block_size)#inilaization vector
        cipher=AES.new(key,AES.MODE_CBC,iv)
        return iv+cipher.encrypt(message)   

    def encrypt_file(self,file_name):
        with open(file_name,'rb') as f:
            plaintext=f.read()
            enc=self.encrypt(plaintext,self.key)
        with open(file_name+'.enc','wb') as f:
            f.write(enc)
        os.remove(file_name)

    def decrypt(self,cipher_text,key):
        iv=cipher_text[:AES.block_size]
        cipher=AES.new(key,AES.MODE_CBC,iv)
        plaintext=cipher.decrypt(cipher_text[AES.block_size:])
        return plaintext.rstrip(b'\0')


    def decrypt_file(self,file_name):
        with open(file_name,'rb') as f:
            cipher_text=f.read()
        dec=self.decrypt(cipher_text,self.key)
        with open(file_name[:-4],'wb') as f:
            f.write(dec)
        os.remove(file_name)