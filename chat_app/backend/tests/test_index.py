import unittest
from unittest.mock import patch, MagicMock, ANY
import sys
import os
import json
from datetime import datetime
import pytz
from bson import ObjectId

# Add the parent directory to sys.path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from index import app

class TestAPIEndpoints(unittest.TestCase):
    
    def setUp(self):
        """Set up the Flask test client"""
        self.app = app.test_client()
        self.app.testing = True
    
    @patch('index.users_collection')
    @patch('index.bcrypt')
    def test_register_endpoint(self, mock_bcrypt, mock_users_collection):
        """Test the /register endpoint"""
        # Configure mocks
        mock_bcrypt.generate_password_hash.return_value = b'hashed_password'
        mock_users_collection.find_one.return_value = None  # User doesn't exist
        mock_users_collection.insert_one.return_value = MagicMock()
        mock_users_collection.insert_one.return_value.inserted_id = ObjectId('1234567890abcdef12345678')
        
        # Test data
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'grade': '11'
        }
        
        # Make request
        response = self.app.post(
            '/register',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        # Check response
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response_data['success'])
        self.assertIn('access_token', response_data)
        self.assertEqual(response_data['user_id'], '1234567890abcdef12345678')
        
        # Verify password was hashed
        mock_bcrypt.generate_password_hash.assert_called_once_with('password123')
        
        # Verify user was saved with expected fields
        insert_call_args = mock_users_collection.insert_one.call_args[0][0]
        self.assertEqual(insert_call_args['username'], 'testuser')
        self.assertEqual(insert_call_args['email'], 'test@example.com')
        self.assertEqual(insert_call_args['grade'], '11')
        
    @patch('index.users_collection')
    @patch('index.bcrypt')
    def test_login_endpoint(self, mock_bcrypt, mock_users_collection):
        """Test the /login endpoint"""
        # Configure mocks
        mock_user = {
            '_id': ObjectId('1234567890abcdef12345678'),
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'hashed_password',
            'grade': '11'
        }
        mock_users_collection.find_one.return_value = mock_user
        mock_bcrypt.check_password_hash.return_value = True
        
        # Test data
        login_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }
        
        # Make request
        response = self.app.post(
            '/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        # Check response
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data['success'])
        self.assertIn('access_token', response_data)
        
        # Verify password was checked
        mock_bcrypt.check_password_hash.assert_called_once_with('hashed_password', 'password123')
    
    @patch('index.get_jwt_identity')
    @patch('index.users_collection')
    def test_get_user_profile(self, mock_users_collection, mock_get_jwt_identity):
        """Test the /user GET endpoint"""
        # Configure mocks
        mock_get_jwt_identity.return_value = '1234567890abcdef12345678'
        mock_user = {
            '_id': ObjectId('1234567890abcdef12345678'),
            'username': 'testuser',
            'email': 'test@example.com',
            'grade': '11',
            'current_streak': 5,
            'longest_streak': 10,
            'streak_history': ['2023-01-01', '2023-01-02'],
            'last_active_date': '2023-01-02'
        }
        mock_users_collection.find_one.return_value = mock_user
        
        # Make request
        response = self.app.get(
            '/user',
            headers={'Authorization': 'Bearer fake_token'}
        )
        
        # Check response
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['user']['username'], 'testuser')
        self.assertEqual(response_data['user']['email'], 'test@example.com')
        
        # Check streak data
        self.assertIn('streak_data', response_data['user'])
        self.assertEqual(response_data['user']['streak_data']['current_streak'], 5)
        self.assertEqual(response_data['user']['streak_data']['longest_streak'], 10)
    
    @patch('index.get_jwt_identity')
    @patch('index.chat_ollama')
    @patch('index.chats_collection')
    @patch('index.encryption_manager')
    def test_generate_endpoint(self, mock_encryption, mock_chats, mock_chat_ollama, mock_get_jwt_identity):
        """Test the /generate endpoint"""
        # Configure mocks
        mock_get_jwt_identity.return_value = '1234567890abcdef12345678'
        
        # Mock generator to yield a few chunks
        mock_chat_ollama.generate.return_value = [
            "This ", "is ", "a ", "test ", "response."
        ]
        
        # Mock encryption
        mock_encryption.encrypt_field.return_value = "encrypted_data"
        
        # Test data
        generate_data = {
            'grade': '11',
            'subjects': ['math', 'physics'],
            'query': 'What is differentiation?',
            'conversation_id': None
        }
        
        # Mock ObjectId for new conversation
        mock_result = MagicMock()
        mock_result.inserted_id = ObjectId('1234567890abcdef12345679')
        mock_chats.insert_one.return_value = mock_result
        
        # Make request
        response = self.app.post(
            '/generate',
            data=json.dumps(generate_data),
            content_type='application/json',
            headers={'Authorization': 'Bearer fake_token'}
        )
        
        # Check response is streaming
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/event-stream')
        
        # For SSE endpoints we can't easily check the response body due to streaming
        # but we can verify that the correct functions were called
        mock_chat_ollama.generate.assert_called_once()
        mock_chats.insert_one.assert_called_once()
    
    @patch('index.get_jwt_identity')
    @patch('index.tests_collection')
    @patch('index.test_attempts_collection')
    @patch('index.generate_and_save_test')
    def test_generate_test_endpoint(self, mock_generate_test, mock_attempts, mock_tests, mock_get_jwt_identity):
        """Test the /api/generate_test endpoint"""
        # Configure mocks
        mock_get_jwt_identity.return_value = '1234567890abcdef12345678'
        
        # Mock generate_and_save_test return value
        mock_generate_test.return_value = {
            'success': True,
            'test_id': '1234567890abcdef12345679',
            'test': {
                'title': 'Math Test',
                'topic': 'Differentiation',
                'grade': '11',
                'subjects': ['math'],
                'questions': [{'question_text': 'What is differentiation?'}] * 5,
                'num_questions': 5
            }
        }
        
        # Test data
        test_data = {
            'title': 'Math Test',
            'topic': 'Differentiation',
            'grade': '11',
            'subjects': ['math'],
            'num_questions': 5
        }
        
        # Make request
        response = self.app.post(
            '/api/generate_test',
            data=json.dumps(test_data),
            content_type='application/json',
            headers={'Authorization': 'Bearer fake_token'}
        )
        
        # Check response
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['test_id'], '1234567890abcdef12345679')
        self.assertEqual(response_data['test']['title'], 'Math Test')
        
        # Verify generate_and_save_test was called correctly
        mock_generate_test.assert_called_once_with(
            user_id='1234567890abcdef12345678',
            title='Math Test',
            topic='Differentiation',
            grade='11',
            subjects=['math'],
            num_questions=5
        )
    
    @patch('index.get_jwt_identity')
    @patch('index.evaluate_test_answers')
    def test_evaluate_test_endpoint(self, mock_evaluate, mock_get_jwt_identity):
        """Test the /api/evaluate_test endpoint"""
        # Configure mocks
        mock_get_jwt_identity.return_value = '1234567890abcdef12345678'
        
        # Mock evaluate_test_answers return value
        mock_evaluate.return_value = {
            'success': True,
            'test_title': 'Math Test',
            'test_topic': 'Differentiation',
            'evaluation': [
                {
                    'question_number': 1,
                    'question_text': 'What is differentiation?',
                    'user_answer': 'Finding rate of change',
                    'correct_answer': 'Finding rate of change',
                    'is_correct': True,
                    'explanation': 'Correct!'
                }
            ],
            'score': {
                'correct': 1,
                'total': 1,
                'percentage': 100.0
            }
        }
        
        # Mock tests_collection and test_attempts_collection
        with patch('index.tests_collection') as mock_tests:
            with patch('index.test_attempts_collection') as mock_attempts:
                # Mock test retrieval
                mock_tests.find_one.return_value = {
                    '_id': ObjectId('1234567890abcdef12345679'),
                    'title': 'Math Test',
                    'user_id': ObjectId('1234567890abcdef12345678'),
                    'attempts': 0,
                    'best_score': 0
                }
                
                # Mock attempt retrieval
                mock_attempts.find.return_value.sort.return_value.limit.return_value = []
                
                # Test data
                eval_data = {
                    'test_id': '1234567890abcdef12345679',
                    'answers': [{'question_id': 0, 'answer': 'Finding rate of change'}]
                }
                
                # Make request
                response = self.app.post(
                    '/api/evaluate_test',
                    data=json.dumps(eval_data),
                    content_type='application/json',
                    headers={'Authorization': 'Bearer fake_token'}
                )
                
                # Check response
                response_data = json.loads(response.data)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response_data['success'])
                self.assertEqual(response_data['score'], 100.0)
                self.assertEqual(len(response_data['evaluation']), 1)
                
                # Verify evaluate_test_answers was called correctly
                mock_evaluate.assert_called_once_with(
                    user_id='1234567890abcdef12345678',
                    test_id='1234567890abcdef12345679',
                    answers=[{'question_id': 0, 'answer': 'Finding rate of change'}]
                )


if __name__ == '__main__':
    unittest.main()
