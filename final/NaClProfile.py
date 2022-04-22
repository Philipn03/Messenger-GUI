# Philip Nguyen
# philipbn@uci.edu
# 57277528

import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box

from Profile import Profile
from Profile import Post
from NaClDSEncoder import NaClDSEncoder
import json, time, os
from pathlib import Path
import ds_client

class DsuFileError(Exception):
    pass

class DsuProfileError(Exception):
    pass

class NaClProfile(Profile):

    def __init__(self):
        super().__init__()
        self.public_key = None
        self.private_key = None
        self.keypair = None
        # self.nacl_enc = NaClDSEncoder()
        
    def generate_keypair(self) -> str:

        nacl_enc = NaClDSEncoder()
        nacl_enc.generate()
        self.public_key = nacl_enc.public_key
        self.private_key = nacl_enc.private_key
        self.keypair = nacl_enc.keypair
        return self.keypair

    def import_keypair(self, keypair: str):
        
        index = 0
    
        for i in range(len(keypair)):
            if keypair[i:i+1] == '=':
                index = keypair.index('=')
                break

        self.public_key = keypair[:index+1]
        self.private_key = keypair[index+1:]
        self.keypair = keypair
    
    # def x(self):
    #     public_key_obj = NaClDSEncoder.encode_public_key(NaClProfile, self.public_key)
    #     private_key_obj =  NaClDSEncoder.encode_private_key(NaClProfile, self.private_key)
    #     box = NaClDSEncoder.create_box(NaClProfile, private_key_obj, public_key_obj)
    #     return box

    # before post is added to profile, should be encrypted
    def add_post(self, entry: Post):
        public_key_obj = NaClDSEncoder.encode_public_key(self, self.public_key)
        private_key_obj =  NaClDSEncoder.encode_private_key(self, self.private_key)
        box = NaClDSEncoder.create_box(self, private_key_obj, public_key_obj)
        
        entry['entry'] = NaClDSEncoder.encrypt_message(self, box, entry['entry'])
        super().add_post(entry)

    # decrypt post entries, return Post
    def get_posts(self):
        x = NaClDSEncoder()
        lst = super().get_posts()

        public_key_obj = x.encode_public_key(self.public_key)
        private_key_obj =  x.encode_private_key(self.private_key)
        box = x.create_box(private_key_obj, public_key_obj)
        try:
            for i in lst:
                i['entry'] = x.decrypt_message(box, i['entry'])
            # msg_lst = self.nacl_enc.decrypt_message(box, lst['entry'])
            return lst
        except:
            return lst
        
    def load_profile(self, path: str) -> None:
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                self.keypair = obj['keypair']
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()

    # public key that DS server gives
    def encrypt_entry(self, entry:str, public_key:str) -> bytes:
        public_key_obj = NaClDSEncoder.encode_public_key(self, public_key)
        private_key_obj =  NaClDSEncoder.encode_private_key(self, self.private_key)
        box = NaClDSEncoder.create_box(self, private_key_obj, public_key_obj)
        msg = NaClDSEncoder.encrypt_message(self, box, entry)
        return msg # msg in bytes

# np = NaClProfile()
# np.generate_keypair()
# post = Post()
# post.set_entry('Post an encrytped message')
# np.add_post(post)
# msg = np.get_posts()[0].entry

# token = ds_client.connect('168.235.86.101', 3021, 'dino321', 'rose', np.public_key)

# msg = np.encrypt_entry(msg, token)
# result = ds_client.send_message(msg, np.public_key)
# # np = NaClProfile()
# kp = np.generate_keypair()

# # Test encryption with 3rd party public key
# ds_pubkey = "jIqYIh2EDibk84rTp0yJcghTPxMWjtrt5NW4yPZk3Cw="
# ee = np.encrypt_entry("Encrypted Message for DS Server", ds_pubkey)
# print(ee)

# # Add a post to the profile and check that it is decrypted.
# np.add_post(Post("Hello alted World!"))
# p_list = np.get_posts()
# print(p_list[0].get_entry())

# # Save the profile
# np.save_profile('/Users/philip_bmn/Desktop/ICS32/mark.dsu')

# print("Open DSU file to check if message is encrypted.")
# input("Press Enter to Continue")

# Create a new NaClProfile object and load the dsu file.
# np2 = NaClProfile()
# np2.load_profile(PATH/TO/DSU)
# # Import the keys
# np2.import_keypair(kp)

# # Verify the post decrypts properly
# p_list = np2.get_posts()
# print(p_list[0].get_entry())
