import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import logging


logger = logging.getLogger('encryption')

KEY_FILE = 'crypto_key.bin'
IV = b'\x00' *16 

class Crypto_encryption:
    def genrate_key(self):
        return os.urandom(32)
    

    def store_key(self, file_path, key):
        with open(file_path, 'wb')  as key_file:
            key_file.write(key)
        logger.info(f'Key stored in {file_path}')
        return key
    
    def retrive_key(self, file_path):
        with open(file_path, 'rb') as key_file:
            key = key_file.read()
        return key
    
    def get_key(self):
        if not os.path.exists(KEY_FILE):
            key = self.genrate_key()
            self.store_key(KEY_FILE, key)
        else:
            key = self.retrive_key(KEY_FILE)
        return key
    
    def encrypt_value(self, value):
        key = self.get_key()
        plain_text = value.encode()
        pad_length = 16 - len(plain_text) % 16
        plain_text += bytes([pad_length])*pad_length

        cipher = Cipher(algorithms.AES(key), modes.CBC(IV), backend=default_backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plain_text) + encryptor.finalize()

        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt_value(self, value):
        key = self.get_key()
        ciphertext = base64.b64decode(value)

        cipher = Cipher(algorithms.AES(key), modes.CBC(IV), backend=default_backend)
        decryptor = cipher.decryptor()
        decryptor_padded = decryptor.update(ciphertext) + decryptor.finalize()

        pad_length = decryptor_padded[-1]
        plain_text = decryptor_padded[:-pad_length]
        return plain_text.decode()