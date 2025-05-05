import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
import tempfile
import shutil

# Add the parent directory to sys.path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from encryption import EncryptionManager

class TestEncryption(unittest.TestCase):
    
    def setUp(self):
        """Create a temporary directory for storing keys during tests"""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create paths to mock key files
        self.master_key_path = os.path.join(self.temp_dir, ".master.key")
        self.fernet_key_path = os.path.join(self.temp_dir, ".fernet.key")
        
        # Mock MongoDB connection parameters
        self.mongo_uri = "mongodb://localhost:27017/test"
    
    def tearDown(self):
        """Clean up temporary files"""
        shutil.rmtree(self.temp_dir)
    
    @patch('os.path.dirname')
    @patch('pymongo.MongoClient')
    @patch('pymongo.encryption.ClientEncryption')
    def test_encryption_manager_initialization(self, mock_client_encryption, 
                                             mock_mongo_client, mock_dirname):
        """Test the initialization of EncryptionManager"""
        # Configure mocks
        mock_dirname.return_value = self.temp_dir
        mock_mongo_client.return_value = MagicMock()
        mock_client_encryption.return_value = MagicMock()
        
        # Mock key files to simulate they don't exist yet
        with patch('os.path.exists', return_value=False):
            with patch('builtins.open', mock_open()) as mock_file:
                # Create instance
                manager = EncryptionManager(self.mongo_uri)
                
                # Verify files were created
                self.assertEqual(mock_file.call_count, 2)  # Two files opened for writing
        
        # Check if the mongo client was created
        mock_mongo_client.assert_called_once_with(self.mongo_uri)
        
        # Check if the encryption client was created
        mock_client_encryption.assert_called_once()
    
    @patch('os.path.dirname')
    @patch('pymongo.MongoClient')
    @patch('pymongo.encryption.ClientEncryption')
    def test_existing_keys_loading(self, mock_client_encryption, 
                                 mock_mongo_client, mock_dirname):
        """Test loading existing keys"""
        # Configure mocks
        mock_dirname.return_value = self.temp_dir
        mock_mongo_client.return_value = MagicMock()
        mock_client_encryption.return_value = MagicMock()
        
        # Create mock key files
        master_key = os.urandom(96)
        fernet_key = os.urandom(32)
        
        # Mock key files to simulate they exist
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=master_key)):
                # Create instance
                manager = EncryptionManager(self.mongo_uri)
                
                # Verify files were opened for reading
                # This is simplified in the test as we're using the same mock for both files
                
        # Key length should match the expected length
        self.assertEqual(len(manager.mongo_master_key), 96)
    
    @patch('os.path.dirname')
    @patch('pymongo.MongoClient')
    @patch('pymongo.encryption.ClientEncryption')
    @patch('cryptography.fernet.Fernet')
    def test_encrypt_decrypt_field(self, mock_fernet, mock_client_encryption, 
                                 mock_mongo_client, mock_dirname):
        """Test encryption and decryption of fields"""
        # Configure mocks
        mock_dirname.return_value = self.temp_dir
        mock_mongo_client.return_value = MagicMock()
        mock_client_encryption.return_value = MagicMock()
        
        # Create a mock Fernet instance
        mock_fernet_instance = MagicMock()
        mock_fernet.return_value = mock_fernet_instance
        mock_fernet.generate_key.return_value = b'mock_fernet_key_for_testing_purposes=='
        
        # Mock encrypt/decrypt methods
        test_input = "secret message"
        encrypted_bytes = b'encrypted_data'
        mock_fernet_instance.encrypt.return_value = encrypted_bytes
        mock_fernet_instance.decrypt.return_value = test_input.encode()
        
        # Mock key files to simulate they exist
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=os.urandom(96))):
                # Create instance
                manager = EncryptionManager(self.mongo_uri)
        
        # Test encryption
        encrypted = manager.encrypt_field(test_input)
        mock_fernet_instance.encrypt.assert_called_once_with(test_input.encode())
        
        # Test decryption
        decrypted = manager.decrypt_field(encrypted)
        self.assertEqual(decrypted, test_input)
        mock_fernet_instance.decrypt.assert_called_once()
    
    @patch('os.path.dirname')
    @patch('pymongo.MongoClient')
    @patch('pymongo.encryption.ClientEncryption')
    def test_close_method(self, mock_client_encryption, mock_mongo_client, mock_dirname):
        """Test the close method"""
        # Configure mocks
        mock_dirname.return_value = self.temp_dir
        mock_client = MagicMock()
        mock_mongo_client.return_value = mock_client
        
        mock_encryption = MagicMock()
        mock_client_encryption.return_value = mock_encryption
        
        # Mock key files
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=os.urandom(96))):
                # Create instance
                manager = EncryptionManager(self.mongo_uri)
        
        # Test close method
        manager.close()
        
        # Verify both clients were closed
        mock_encryption.close.assert_called_once()
        mock_client.close.assert_called_once()
    
    @patch('os.path.dirname')
    @patch('pymongo.MongoClient')
    @patch('pymongo.encryption.ClientEncryption')
    def test_none_value_handling(self, mock_client_encryption, 
                               mock_mongo_client, mock_dirname):
        """Test handling of None values"""
        # Configure mocks
        mock_dirname.return_value = self.temp_dir
        mock_mongo_client.return_value = MagicMock()
        mock_client_encryption.return_value = MagicMock()
        
        # Mock key files
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=os.urandom(96))):
                # Create instance
                manager = EncryptionManager(self.mongo_uri)
        
        # Test encryption with None
        result = manager.encrypt_field(None)
        self.assertIsNone(result)
        
        # Test decryption with None
        result = manager.decrypt_field(None)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
