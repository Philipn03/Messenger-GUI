# Philip Nguyen
# philipbn@uci.edu
# 57277528

import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box

class NaClDSEncoder:

    def generate(self):
        # call the key generator function from the nacl library.
        raw = PrivateKey.generate()
        # the raw keypair, stored as PrivateKey.
        self.raw_keypair = raw
        # the private key, encoded from bytes to string
        self.private_key = raw.encode(encoder=nacl.encoding.Base64Encoder).decode(encoding = 'UTF-8')
        # the public key, encoded from bytes to string
        self.public_key = raw.public_key.encode(encoder=nacl.encoding.Base64Encoder).decode(encoding = 'UTF-8')
        # the keypair, useful for storage, but primarily a convenience attribute
        # that simply concatenates the public and private keys and stores them as a string.
        self.keypair = self.public_key + self.private_key
    
    def encode_public_key(self, public_key:str) -> PublicKey:
        return PublicKey(public_key, nacl.encoding.Base64Encoder)
    
    def encode_private_key(self, private_key:str) -> PrivateKey:
        return PrivateKey(private_key, nacl.encoding.Base64Encoder)
    
    def create_box(self, encoded_private_key:PrivateKey, encoded_public_key:PublicKey) -> Box:
        return Box(encoded_private_key, encoded_public_key)
    
    def encrypt_message(self, box:Box, message:str) -> str:
        #first convert the message to bytes
        bmsg = message.encode(encoding='UTF-8')
        # encrypt message
        encrypted_msg = box.encrypt(bmsg, encoder=nacl.encoding.Base64Encoder)
        # convert back to str
        msg = encrypted_msg.decode(encoding='UTF-8')

        return msg # string to bytes
    
    def decrypt_message(self, box:Box, message:str) -> str:
        #first conver the message to bytes
        bmsg = message.encode(encoding='UTF-8')
        decrypted_msg = box.decrypt(bmsg, encoder=nacl.encoding.Base64Encoder)
        # convert back to str
        msg = decrypted_msg.decode(encoding='UTF-8')

        return msg # bytes to string