from base64 import b64decode
from cryptography.fernet import Fernet
import os
from pymongo import MongoClient
from pymongo.encryption import ClientEncryption
from bson.codec_options import CodecOptions
from bson.binary import STANDARD, Binary, UUID_SUBTYPE

class EncryptionManager:
    def __init__(self, mongodb_uri):
        # Generate or load master key
        self.mongo_master_key = self._get_or_create_master_key()
        self.fernet_key = self._get_or_create_fernet_key()
        # print(len(self.mongo_master_key))
        # print(len(self.fernet_key))
        
        # Configure encryption
        self.kms_providers = {
            "local": {
                "key": Binary(self.mongo_master_key)  # Convert to BSON Binary
            }
        }
        
        # Create MongoDB client
        self.client = MongoClient(mongodb_uri)
        
        # Create encryption client
        self.client_encryption = ClientEncryption(
            self.kms_providers,
            "encryption.__keyVault",
            self.client,
            CodecOptions(),
            # kms_providers="local"
        )
        
        # Initialize Fernet cipher for field encryption
        self.cipher = Fernet(self.fernet_key)

    def _get_or_create_master_key(self):
        key_path = os.path.join(os.path.dirname(__file__), ".master.key")
        if os.path.exists(key_path):
            with open(key_path, "rb") as f:
                key = f.read()
                # print("Loaded master key length:", len(key)) 
                if len(key) != 96:
                    raise ValueError("Invalid MongoDB master key length")
                return key
        else:
            key = os.urandom(96)
            # print("Generated new master key length:", len(key))  
            os.makedirs(os.path.dirname(key_path), exist_ok=True)
            with open(key_path, "wb") as f:
                f.write(key)
            return key


    def encrypt_field(self, data):
        """Encrypt a single field"""
        if not data:
            return data
        if isinstance(data, str):
            return self.cipher.encrypt(data.encode()).decode()
        return data

    def decrypt_field(self, encrypted_data):
        """Decrypt a single field"""
        if not encrypted_data:
            return encrypted_data
        if isinstance(encrypted_data, str):
            return self.cipher.decrypt(encrypted_data.encode()).decode()
        return encrypted_data
    
    def _get_or_create_fernet_key(self):
        """Generate or load a Fernet key for field encryption"""
        key_path = os.path.join(os.path.dirname(__file__), ".fernet.key")
        if os.path.exists(key_path):
            with open(key_path, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            os.makedirs(os.path.dirname(key_path), exist_ok=True)
            with open(key_path, "wb") as f:
                f.write(key)
            return key

    def close(self):
        """Close the encryption clients"""
        if hasattr(self, 'client_encryption'):
            self.client_encryption.close()
        if hasattr(self, 'client'):
            self.client.close()