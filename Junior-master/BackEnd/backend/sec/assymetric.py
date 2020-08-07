from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa,padding
from cryptography.hazmat.primitives import serialization,hashes
import os

class AEncryptor:

    def __init__(self):
        self.GeneratePrivateKey()
        self.GeneratePublicKey()
    
    def GeneratePrivateKey(self,KeySize=4096):
        self.private_key=rsa.generate_private_key(
            public_exponent=65537,
            key_size=KeySize,
            backend=default_backend()
        )

    def GeneratePublicKey(self):
        self.public_key=self.private_key.public_key()

        return self.public_key
    def WritePrivateKey(self,filename):
        private_pem=self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(f'{filename}.pem','wb') as f:
            f.write(private_pem)

    def WritepublicKey(self,filename):
        public_pem=self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open(f'{filename}.pem','wb') as f:
            f.write(public_pem)

    def ReadPrivateKey(self,filename):
        with open(filename,'rb') as f:
            self.private_key=serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )

    def ReadPublicKey(self,filename):
        with open(filename,'rb') as f:
            self.public_key=serialization.load_pem_public_key(
                f.read(),
                backend=default_backend()
            )

    def Encrypt(self,message):
        cipher=self.public_key.encrypt(
            message,
            padding=padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return cipher

    def Decrypt(self,cipher):
        plain_text=self.private_key.decrypt(
            message=cipher,
            padding=padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plain_text

    def EncryptFile(self,filename):
        with open(filename,'rb') as f:
            plain_text=f.read()
        cipher=self.Encrypt(plain_text)
        with open(filename+'.enc','wb') as f:
            f.write(cipher)
        os.remove(filename)


    def DecryptFile(self,filename):
        with open(filename,'rb') as f:
            cipher=f.read()
            plain_text=self.Decrypt(cipher)
        with open(filename[:-4],'wb') as f:
            f.write(plain_text)
        os.remove(filename)






