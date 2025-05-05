import unittest
import json
import os
import sys
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import datetime
import logging
import warnings
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load environment variables
load_dotenv()

# Import the Flask app from index.py
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from index import app, users_collection, jwt, chats_collection, tests_collection, test_attempts_collection, IST, encryption_manager

class UserManagementTestCase(unittest.TestCase):
    """Test cases for user management features (registration, login, profile editing, logout)."""

    def setUp(self):
        """Set up test client and create a test database."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        self.app.config['SERVER_NAME'] = 'localhost'
        
        # Create test user data
        self.test_user = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123",
            "grade": "10"
        }
        
        # Clear test user if it exists from previous test runs
        users_collection.delete_many({
            "$or": [
                {"email": self.test_user["email"]},
                {"username": self.test_user["username"]},
                {"email": "new_email@example.com"},  # For email update tests
                {"username": "newusername"}  # For username update tests
            ]
        })
        
        self.access_token = None
    
    def tearDown(self):
        """Clean up after each test."""
        # Remove test users
        users_collection.delete_many({
            "$or": [
                {"email": self.test_user["email"]},
                {"username": self.test_user["username"]},
                {"email": "new_email@example.com"},
                {"username": "newusername"}
            ]
        })
    
    # UC-01: User Registration Tests
    
    def test_01_valid_user_registration(self):
        """Test Case 1: Verify successful user registration with valid credentials."""
        response = self.client.post(
            '/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['success'])
        self.assertIn('access_token', data)
        self.assertIn('user_id', data)
        self.assertEqual(data['message'], 'User registered successfully')
        
        # Verify user exists in database
        user = users_collection.find_one({"email": self.test_user["email"]})
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], self.test_user["username"])
        
        logger.info("Test 1 - Valid user registration: PASSED")
    
    def test_02_invalid_email_format(self):
        """Test Case 2: Verify registration fails with invalid email format."""
        invalid_user = self.test_user.copy()
        invalid_user["email"] = "invalid-email-format"
        
        response = self.client.post(
            '/register',
            data=json.dumps(invalid_user),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertIn('errors', data)
        self.assertTrue(any("Invalid email format" in error for error in data['errors']))
        
        logger.info("Test 2 - Invalid email format: PASSED")
    
    def test_03_weak_password(self):
        """Test Case 3: Verify registration fails with password not meeting requirements."""
        weak_password_user = self.test_user.copy()
        weak_password_user["password"] = "weak"  # Too short
        
        response = self.client.post(
            '/register',
            data=json.dumps(weak_password_user),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertIn('errors', data)
        self.assertTrue(any("Password must be at least 8 characters long" in error for error in data['errors']))
        
        logger.info("Test 3 - Weak password: PASSED")
    
    def test_04_duplicate_email(self):
        """Test Case 4: Verify registration fails with already registered email."""
        # First register a user
        self.client.post(
            '/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        
        # Try to register again with the same email
        duplicate_user = self.test_user.copy()
        duplicate_user["username"] = "different_username"  # Change username to isolate email duplication
        
        response = self.client.post(
            '/register',
            data=json.dumps(duplicate_user),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 409)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Email already registered')
        
        logger.info("Test 4 - Duplicate email: PASSED")
    
    # UC-02: User Login Tests
    
    def test_05_valid_login(self):
        """Test Case 5: Verify successful login with valid credentials."""
        # First register a user
        self.client.post(
            '/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        
        # Login with registered credentials
        login_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"]
        }
        
        response = self.client.post(
            '/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('access_token', data)
        self.assertEqual(data['message'], 'Login successful')
        
        # Save token for later tests
        self.access_token = data['access_token']
        
        logger.info("Test 5 - Valid login: PASSED")
    
    def test_06_invalid_password(self):
        """Test Case 6: Verify login fails with incorrect password."""
        # First register a user
        self.client.post(
            '/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        
        # Try to login with wrong password
        login_data = {
            "email": self.test_user["email"],
            "password": "WrongPassword123"
        }
        
        response = self.client.post(
            '/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Invalid credentials')
        
        logger.info("Test 6 - Invalid password: PASSED")
    
    def test_07_unregistered_user_login(self):
        """Test Case 7: Verify login fails with unregistered username/email."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "SomePassword123"
        }
        
        response = self.client.post(
            '/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Invalid credentials')
        
        logger.info("Test 7 - Unregistered user login: PASSED")
    
    # UC-03: Edit User Profile Tests
    
    def test_08_update_username(self):
        """Test Case 8: Verify successful username update."""
        # First register and login to get token
        self.client.post(
            '/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        
        login_response = self.client.post(
            '/login',
            data=json.dumps({
                "email": self.test_user["email"],
                "password": self.test_user["password"]
            }),
            content_type='application/json'
        )
        
        login_data = json.loads(login_response.data)
        token = login_data['access_token']
        
        # Update username
        update_data = {
            "username": "newusername"
        }
        
        response = self.client.put(
            '/api/user/username',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Username updated successfully')
        
        # Verify username was updated in database
        user = users_collection.find_one({"email": self.test_user["email"]})
        self.assertEqual(user["username"], "newusername")
        
        logger.info("Test 8 - Update username: PASSED")
    
    def test_09_update_password(self):
        """Test Case 9: Verify successful password update."""
        # First register and login
        self.client.post(
            '/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        
        login_response = self.client.post(
            '/login',
            data=json.dumps({
                "email": self.test_user["email"],
                "password": self.test_user["password"]
            }),
            content_type='application/json'
        )
        
        login_data = json.loads(login_response.data)
        token = login_data['access_token']
        
        # Update password
        update_data = {
            "current_password": self.test_user["password"],
            "new_password": "NewStrongPassword123"
        }
        
        response = self.client.put(
            '/api/user/password',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Password updated successfully')
        
        # Verify can login with new password
        new_login_response = self.client.post(
            '/login',
            data=json.dumps({
                "email": self.test_user["email"],
                "password": "NewStrongPassword123"
            }),
            content_type='application/json'
        )
        
        new_login_data = json.loads(new_login_response.data)
        
        self.assertEqual(new_login_response.status_code, 200)
        self.assertTrue(new_login_data['success'])
        
        logger.info("Test 9 - Update password: PASSED")
    
    def test_10_invalid_profile_update(self):
        """Test Case 10: Verify profile update fails with invalid input."""
        # First register and login
        self.client.post(
            '/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        
        login_response = self.client.post(
            '/login',
            data=json.dumps({
                "email": self.test_user["email"],
                "password": self.test_user["password"]
            }),
            content_type='application/json'
        )
        
        login_data = json.loads(login_response.data)
        token = login_data['access_token']
        
        # Try to update with weak password
        weak_password_update = {
            "current_password": self.test_user["password"],
            "new_password": "weak"  # Too short
        }
        
        response = self.client.put(
            '/api/user/password',
            data=json.dumps(weak_password_update),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'New password must be at least 8 characters long')
        
        logger.info("Test 10 - Invalid profile update: PASSED")
    
    # UC-04: Logout User Tests
    
    def test_11_user_logout(self):
        """Test Case 11: Verify successful logout."""
        # First register and login
        self.client.post(
            '/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        
        login_response = self.client.post(
            '/login',
            data=json.dumps({
                "email": self.test_user["email"],
                "password": self.test_user["password"]
            }),
            content_type='application/json'
        )
        
        login_data = json.loads(login_response.data)
        token = login_data['access_token']
        
        # Logout
        response = self.client.post(
            '/logout',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Logout successful')
        
        # Verify token is invalidated by trying to access a protected route
        user_response = self.client.get(
            '/user',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        # Should get 401 Unauthorized
        self.assertEqual(user_response.status_code, 401)
        
        logger.info("Test 11 - User logout: PASSED")


# Add these new test classes after the UserManagementTestCase class
class SubjectDetectionTestCase(unittest.TestCase):
    """Test cases for subject detection and intent recognition."""

    def setUp(self):
        """Set up test client and create a test database."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        # Create test user data
        self.test_user = {
            "username": "subjectuser",
            "email": "subject@example.com",
            "password": "TestPassword123",
            "grade": "10"
        }
        
        # Clean test user if it exists from previous test runs
        users_collection.delete_many({
            "$or": [
                {"email": self.test_user["email"]},
                {"username": self.test_user["username"]}
            ]
        })
        
        # Register user and get token
        response = self.client.post(
            '/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.access_token = data['access_token']
    
    def tearDown(self):
        """Clean up after each test."""
        # Remove test users
        users_collection.delete_many({
            "$or": [
                {"email": self.test_user["email"]},
                {"username": self.test_user["username"]}
            ]
        })
    
    def test_12_specific_subject_detection(self):
        """Test Case 12: Enter query clearly related to a specific subject."""
        # This test only verifies if a response is generated, not its content
        
        query_data = {
            "grade": "10",
            "subjects": ["biology", "physics", "chemistry"],
            "query": "Explain photosynthesis"
        }
        
        response = self.client.post(
            '/generate',
            data=json.dumps(query_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        # We expect a 200 response for a streaming response
        self.assertEqual(response.status_code, 200)
        
        # Check that the response has the expected content type for SSE
        # Updated to check if content_type starts with 'text/event-stream' instead of exact equality
        self.assertTrue(response.content_type.startswith('text/event-stream'))
        
        logger.info("Test 12 - Specific subject detection: PASSED")
    
    def test_13_multi_subject_query(self):
        """Test Case 13: Enter query that could relate to multiple subjects."""
        # This test only verifies if a response is generated, not its content
        
        query_data = {
            "grade": "10",
            "subjects": ["biology", "physics", "chemistry"],
            "query": "What is energy?"
        }
        
        response = self.client.post(
            '/generate',
            data=json.dumps(query_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        # We expect a 200 response for a streaming response
        self.assertEqual(response.status_code, 200)
        
        # Check that the response has the expected content type for SSE
        # Updated to check if content_type starts with 'text/event-stream' instead of exact equality
        self.assertTrue(response.content_type.startswith('text/event-stream'))
        
        logger.info("Test 13 - Multi-subject query: PASSED")
    
    def test_14_vague_query(self):
        """Test Case 14: Enter a vague or unclear query."""
        # This test only verifies if a response is generated, not its content
        
        query_data = {
            "grade": "10",
            "subjects": ["biology", "physics", "chemistry"],
            "query": "Tell me about stuff"
        }
        
        response = self.client.post(
            '/generate',
            data=json.dumps(query_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        # We expect a 200 response for a streaming response
        self.assertEqual(response.status_code, 200)
        
        # Check that the response has the expected content type for SSE
        # Updated to check if content_type starts with 'text/event-stream' instead of exact equality
        self.assertTrue(response.content_type.startswith('text/event-stream'))
        
        logger.info("Test 14 - Vague query: PASSED")


class AdaptiveContentTestCase(unittest.TestCase):
    """Test cases for adaptive content delivery based on grade level."""

    def setUp(self):
        """Set up test client and create a test database."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        # Create elementary grade test user
        self.elementary_user = {
            "username": "elementaryuser",
            "email": "elementary@example.com",
            "password": "TestPassword123",
            "grade": "10"  # Grade 10 is the lowest available in this system
        }
        
        # Create high school test user
        self.high_school_user = {
            "username": "highschooluser",
            "email": "highschool@example.com",
            "password": "TestPassword123",
            "grade": "12"  # Grade 12 represents high school
        }
        
        # Clean test users if they exist from previous test runs
        users_collection.delete_many({
            "$or": [
                {"email": self.elementary_user["email"]},
                {"username": self.elementary_user["username"]},
                {"email": self.high_school_user["email"]},
                {"username": self.high_school_user["username"]}
            ]
        })
        
        # Register elementary user and get token
        elem_response = self.client.post(
            '/register',
            data=json.dumps(self.elementary_user),
            content_type='application/json'
        )
        elem_data = json.loads(elem_response.data)
        self.elementary_token = elem_data['access_token']
        
        # Register high school user and get token
        high_response = self.client.post(
            '/register',
            data=json.dumps(self.high_school_user),
            content_type='application/json'
        )
        high_data = json.loads(high_response.data)
        self.high_school_token = high_data['access_token']
    
    def tearDown(self):
        """Clean up after each test."""
        # Remove test users
        users_collection.delete_many({
            "$or": [
                {"email": self.elementary_user["email"]},
                {"username": self.elementary_user["username"]},
                {"email": self.high_school_user["email"]},
                {"username": self.high_school_user["username"]}
            ]
        })
    
    def test_15_elementary_grade_content(self):
        """Test Case 15: Query response for elementary grade level."""
        # This test only verifies if a response is generated, not its content
        
        query_data = {
            "grade": "10",
            "subjects": ["biology"],
            "query": "Explain what DNA is"
        }
        
        response = self.client.post(
            '/generate',
            data=json.dumps(query_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.elementary_token}'}
        )
        
        # We expect a 200 response for a streaming response
        self.assertEqual(response.status_code, 200)
        
        # Check that the response has the expected content type for SSE
        # Updated to check if content_type starts with 'text/event-stream' instead of exact equality
        self.assertTrue(response.content_type.startswith('text/event-stream'))
        
        logger.info("Test 15 - Elementary grade content: PASSED")
    
    def test_16_high_school_grade_content(self):
        """Test Case 16: Query response for high school grade level."""
        # This test only verifies if a response is generated, not its content
        
        query_data = {
            "grade": "12",
            "subjects": ["biology"],
            "query": "Explain what DNA is"
        }
        
        response = self.client.post(
            '/generate',
            data=json.dumps(query_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.high_school_token}'}
        )
        
        # We expect a 200 response for a streaming response
        self.assertEqual(response.status_code, 200)
        
        # Check that the response has the expected content type for SSE
        # Updated to check if content_type starts with 'text/event-stream' instead of exact equality
        self.assertTrue(response.content_type.startswith('text/event-stream'))
        
        logger.info("Test 16 - High school grade content: PASSED")


class IntentDetectionTestCase(unittest.TestCase):
    """Test cases for intent detection in user queries."""

    def setUp(self):
        """Set up test client and create a test database."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        # Create test user
        self.test_user = {
            "username": "intentuser",
            "email": "intent@example.com",
            "password": "TestPassword123",
            "grade": "11"
        }
        
        # Clean test user if it exists from previous test runs
        users_collection.delete_many({
            "$or": [
                {"email": self.test_user["email"]},
                {"username": self.test_user["username"]}
            ]
        })
        
        # Register user and get token
        response = self.client.post(
            '/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.access_token = data['access_token']
    
    def tearDown(self):
        """Clean up after each test."""
        # Remove test users
        users_collection.delete_many({
            "$or": [
                {"email": self.test_user["email"]},
                {"username": self.test_user["username"]}
            ]
        })
    
    def test_17_explanation_intent(self):
        """Test Case 17: Query asking for an explanation."""
        # This test only verifies if a response is generated, not its content
        
        query_data = {
            "grade": "11",
            "subjects": ["physics"],
            "query": "Explain Newton's laws of motion"
        }
        
        response = self.client.post(
            '/generate',
            data=json.dumps(query_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        # We expect a 200 response for a streaming response
        self.assertEqual(response.status_code, 200)
        
        # Check that the response has the expected content type for SSE
        # Updated to check if content_type starts with 'text/event-stream' instead of exact equality
        self.assertTrue(response.content_type.startswith('text/event-stream'))
        
        logger.info("Test 17 - Explanation intent: PASSED")
    
    def test_18_practice_problem_intent(self):
        """Test Case 18: Query asking for practice problems."""
        # This test only verifies if a response is generated, not its content
        
        query_data = {
            "grade": "11",
            "subjects": ["mathematics"],
            "query": "Give me practice problems on quadratic equations"
        }
        
        response = self.client.post(
            '/generate',
            data=json.dumps(query_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        # We expect a 200 response for a streaming response
        self.assertEqual(response.status_code, 200)
        
        # Check that the response has the expected content type for SSE
        # Updated to check if content_type starts with 'text/event-stream' instead of exact equality
        self.assertTrue(response.content_type.startswith('text/event-stream'))
        
        logger.info("Test 18 - Practice problem intent: PASSED")
    
    def test_19_ambiguous_intent(self):
        """Test Case 19: Query with ambiguous intent."""
        # This test only verifies if a response is generated, not its content
        
        query_data = {
            "grade": "11",
            "subjects": ["mathematics", "physics"],
            "query": "Tell me about calculus applications"
        }
        
        response = self.client.post(
            '/generate',
            data=json.dumps(query_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        # We expect a 200 response for a streaming response
        self.assertEqual(response.status_code, 200)
        
        # Check that the response has the expected content type for SSE
        # Updated to check if content_type starts with 'text/event-stream' instead of exact equality
        self.assertTrue(response.content_type.startswith('text/event-stream'))
        
        logger.info("Test 19 - Ambiguous intent: PASSED")


class QuizGenerationTestCase(unittest.TestCase):
    """Test cases for quiz generation functionality."""

    def setUp(self):
        """Set up test client and create a test database."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        # Create test user
        self.test_user = {
            "username": "quizuser",
            "email": "quiz@example.com",
            "password": "TestPassword123",
            "grade": "11"
        }
        
        # Clean test user if it exists from previous test runs
        users_collection.delete_many({
            "$or": [
                {"email": self.test_user["email"]},
                {"username": self.test_user["username"]}
            ]
        })
        
        # Register user and get token
        response = self.client.post(
            '/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.access_token = data['access_token']
        self.user_id = data['user_id']
    
    def tearDown(self):
        """Clean up after each test."""
        # Remove test user
        users_collection.delete_many({
            "$or": [
                {"email": self.test_user["email"]},
                {"username": self.test_user["username"]}
            ]
        })
        
        # Remove test quizzes
        tests_collection.delete_many({"user_id": ObjectId(self.user_id)})
    
    def test_20_quiz_generation(self):
        """Test Case 20: Request a quiz on a specific subject."""
        quiz_data = {
            "title": "Physics Test",
            "topic": "Newton's Laws of Motion",
            "grade": "11",
            "subjects": ["physics"],
            "num_questions": 3  # Smaller number for faster testing
        }
        
        response = self.client.post(
            '/api/generate_test',
            data=json.dumps(quiz_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('test_id', data)
        self.assertIn('test', data)
        
        # Verify the test has the correct structure
        test = data['test']
        self.assertEqual(test['title'], quiz_data['title'])
        self.assertEqual(test['topic'], quiz_data['topic'])
        self.assertEqual(test['grade'], quiz_data['grade'])
        self.assertIn('questions', test)
        self.assertTrue(len(test['questions']) > 0)
        
        logger.info("Test 20 - Quiz generation: PASSED")


class ChatHistoryTestCase(unittest.TestCase):
    """Test cases for chat history functionality."""

    def setUp(self):
        """Set up test client and create a test database."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        # Create test user
        self.test_user = {
            "username": "chathistoryuser",
            "email": "chathistory@example.com",
            "password": "TestPassword123",
            "grade": "11"
        }
        
        # Clean test user if it exists from previous test runs
        users_collection.delete_many({
            "$or": [
                {"email": self.test_user["email"]},
                {"username": self.test_user["username"]}
            ]
        })
        
        # Register user and get token
        response = self.client.post(
            '/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.access_token = data['access_token']
        self.user_id = data['user_id']
        
        # Create a test conversation
        chat_data = {
            "user_input": "What is the capital of France?",
            "bot_response": "The capital of France is Paris.",
            "grade": "11",
            "subjects": ["geography"]
        }
        
        chat_response = self.client.post(
            '/api/chats',
            data=json.dumps(chat_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        chat_data = json.loads(chat_response.data)
        self.conversation_id = chat_data['conversation_id']
    
    def tearDown(self):
        """Clean up after each test."""
        # Remove test user
        users_collection.delete_many({
            "$or": [
                {"email": self.test_user["email"]},
                {"username": self.test_user["username"]}
            ]
        })
        
        # Remove test conversations
        chats_collection.delete_many({"user_id": ObjectId(self.user_id)})
    
    def test_21_view_chat_history(self):
        """Test Case 21: User accesses Chat History to view past conversations."""
        response = self.client.get(
            '/api/chats',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('conversations', data)
        self.assertTrue(len(data['conversations']) > 0)
        
        # Verify the conversation has the correct structure
        conversation = data['conversations'][0]
        self.assertIn('conversation_id', conversation)
        self.assertIn('name', conversation)
        self.assertIn('last_message', conversation)
        
        logger.info("Test 21 - View chat history: PASSED")
    
    def test_22_select_previous_conversation(self):
        """Test Case 22: User selects a previous conversation and adds to it."""
        # First, get the specific conversation
        response = self.client.get(
            f'/api/chats/{self.conversation_id}/messages',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('messages', data)
        
        # Now add a new message to this conversation
        new_message = {
            "conversation_id": self.conversation_id,
            "user_input": "What is the population of Paris?",
            "bot_response": "The population of Paris is approximately 2.2 million people.",
            "grade": "11",
            "subjects": ["geography"]
        }
        
        response = self.client.post(
            '/api/chats',
            data=json.dumps(new_message),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        self.assertEqual(response.status_code, 201)
        
        # Verify the conversation was updated
        response = self.client.get(
            f'/api/chats/{self.conversation_id}/messages',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        data = json.loads(response.data)
        self.assertEqual(len(data['messages']), 2)  # Should now have 2 messages
        
        logger.info("Test 22 - Select previous conversation: PASSED")


class StreakTrackerTestCase(unittest.TestCase):
    """Test cases for learning streak tracking functionality."""

    def setUp(self):
        """Set up test client and create a test database."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        # Create test user
        self.test_user = {
            "username": "streakuser",
            "email": "streak@example.com",
            "password": "TestPassword123",
            "grade": "11"
        }
        
        # Clean test user if it exists from previous test runs
        users_collection.delete_many({
            "$or": [
                {"email": self.test_user["email"]},
                {"username": self.test_user["username"]}
            ]
        })
        
        # Register user and get token
        response = self.client.post(
            '/register',
            data=json.dumps(self.test_user),
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.access_token = data['access_token']
        self.user_id = data['user_id']
    
    def tearDown(self):
        """Clean up after each test."""
        # Remove test user
        users_collection.delete_many({
            "$or": [
                {"email": self.test_user["email"]},
                {"username": self.test_user["username"]}
            ]
        })
    
    def test_23_increment_streak(self):
        """Test Case 23: User initiates conversation and streak increments."""
        # First, get the current streak
        response = self.client.get(
            '/user',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        initial_data = json.loads(response.data)
        initial_streak = initial_data['user']['streak_data']['current_streak']
        
        # Now record activity
        response = self.client.post(
            '/api/user/activity',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Verify streak was incremented
        response = self.client.get(
            '/user',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        updated_data = json.loads(response.data)
        updated_streak = updated_data['user']['streak_data']['current_streak']
        
        self.assertEqual(updated_streak, initial_streak + 1)
        
        logger.info("Test 23 - Increment streak: PASSED")
    
    def test_24_visualize_streak(self):
        """Test Case 24: User visits profile page and sees streak visualization."""
        # Record activity to ensure there's something to visualize
        self.client.post(
            '/api/user/activity',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        # Now get the profile
        response = self.client.get(
            '/user',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('streak_data', data['user'])
        self.assertIn('current_streak', data['user']['streak_data'])
        self.assertIn('streak_history', data['user']['streak_data'])
        
        # Check that the streak history contains at least one date
        self.assertTrue(len(data['user']['streak_data']['streak_history']) > 0)
        
        logger.info("Test 24 - Visualize streak: PASSED")
    
    def test_25_reset_streak(self):
        """Test Case 25: Streak resets when engagement is missed."""
        # Note: This test cannot be fully automated as it would require manipulating time
        # Instead, we'll test the streak reset functionality directly
        
        # First set a non-zero streak
        users_collection.update_one(
            {"_id": ObjectId(self.user_id)},
            {"$set": {"current_streak": 5}}
        )
        
        # Set the last active date to 2 days ago to simulate missed engagement
        two_days_ago = (datetime.datetime.now(IST) - datetime.timedelta(days=2)).date().isoformat()
        users_collection.update_one(
            {"_id": ObjectId(self.user_id)},
            {"$set": {"last_active_date": two_days_ago}}
        )
        
        # Now record new activity
        response = self.client.post(
            '/api/user/activity',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Verify streak was reset to 1
        response = self.client.get(
            '/user',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        data = json.loads(response.data)
        current_streak = data['user']['streak_data']['current_streak']
        
        self.assertEqual(current_streak, 1)
        
        logger.info("Test 25 - Reset streak: PASSED")


# Add this class to capture test results
class TestResultCollector:
    """Collect test results and generate a summary report."""
    
    def __init__(self):
        self.results = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.error_tests = 0
        
    def add_result(self, test_id, test_name, result, error=None):
        """Add a test result to the collector."""
        self.total_tests += 1
        
        if result == 'PASS':
            self.passed_tests += 1
        elif result == 'FAIL':
            self.failed_tests += 1
        else:  # ERROR
            self.error_tests += 1
            
        self.results[test_id] = {
            'id': test_id,
            'name': test_name,
            'result': result,
            'error': error
        }
    
    def generate_report(self):
        """Generate a summary report of all test results."""
        report = [
            "\n" + "=" * 80,
            "TEST EXECUTION SUMMARY",
            "=" * 80,
            f"Total tests executed: {self.total_tests}",
            f"Tests passed: {self.passed_tests} ({self.passed_tests / self.total_tests * 100:.1f}%)",
            f"Tests failed: {self.failed_tests} ({self.failed_tests / self.total_tests * 100:.1f}%)",
            f"Tests with errors: {self.error_tests} ({self.error_tests / self.total_tests * 100:.1f}%)",
            "-" * 80,
            "DETAILED TEST RESULTS:",
            "-" * 80
        ]
        
        # Group tests by use case
        use_cases = {}
        for test_id, data in self.results.items():
            # Extract use case from test ID (e.g., test_01_valid_user_registration -> UC-01)
            if '_' in test_id:
                parts = test_id.split('_')
                if len(parts) > 1 and parts[1].isdigit():
                    test_num = int(parts[1])
                    if test_num <= 4:
                        use_case = "UC-01: User Registration"
                    elif test_num <= 7:
                        use_case = "UC-02: User Login"
                    elif test_num <= 10:
                        use_case = "UC-03: Edit User Profile" 
                    elif test_num <= 11:
                        use_case = "UC-04: Logout User"
                    elif test_num <= 14:
                        use_case = "UC-05: Subject Detection"
                    elif test_num <= 16:
                        use_case = "UC-06: Adaptive Content Delivery"
                    elif test_num <= 19:
                        use_case = "UC-07: Intent Detection"
                    elif test_num <= 20:
                        use_case = "UC-08: Quiz Generation"
                    elif test_num <= 22:
                        use_case = "UC-09: Chat History"
                    elif test_num <= 25:
                        use_case = "UC-10: Learning Streak Tracker"
                    else:
                        use_case = "Other"
                else:
                    use_case = "Other"
            else:
                use_case = "Other"
                
            if use_case not in use_cases:
                use_cases[use_case] = []
            use_cases[use_case].append(data)
        
        # Generate report by use case
        for use_case, tests in sorted(use_cases.items()):
            report.append(f"\n{use_case}")
            report.append("-" * len(use_case))
            
            for test in sorted(tests, key=lambda x: x['id']):
                result_indicator = "✅" if test['result'] == 'PASS' else "❌"
                report.append(f"{result_indicator} {test['id']}: {test['name']}")
                if test['error']:
                    report.append(f"   Error: {test['error']}")
        
        report.append("\n" + "=" * 80)
        return "\n".join(report)


# Create a custom test result class
class CustomTextTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collector = TestResultCollector()
    
    def addSuccess(self, test):
        super().addSuccess(test)
        test_id = test.id().split('.')[-1]
        test_name = test.shortDescription() or str(test)
        self.collector.add_result(test_id, test_name, 'PASS')
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        test_id = test.id().split('.')[-1]
        test_name = test.shortDescription() or str(test)
        self.collector.add_result(test_id, test_name, 'FAIL', str(err[1]))
    
    def addError(self, test, err):
        super().addError(test, err)
        test_id = test.id().split('.')[-1]
        test_name = test.shortDescription() or str(test)
        self.collector.add_result(test_id, test_name, 'ERROR', str(err[1]))
    
    def printSummary(self):
        """Print the summary report at the end of the test run."""
        print(self.collector.generate_report())


# Create a custom test runner that uses our custom result class
class CustomTextTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, **kwargs):
        kwargs['resultclass'] = CustomTextTestResult
        super().__init__(*args, **kwargs)
    
    def run(self, test):
        result = super().run(test)
        result.printSummary()
        return result


# Modify the main block to use our custom test runner
if __name__ == '__main__':
    # Create a test suite with all test cases
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_suite.addTest(unittest.makeSuite(UserManagementTestCase))
    test_suite.addTest(unittest.makeSuite(SubjectDetectionTestCase))
    test_suite.addTest(unittest.makeSuite(AdaptiveContentTestCase))
    test_suite.addTest(unittest.makeSuite(IntentDetectionTestCase))
    test_suite.addTest(unittest.makeSuite(QuizGenerationTestCase))
    test_suite.addTest(unittest.makeSuite(ChatHistoryTestCase))
    test_suite.addTest(unittest.makeSuite(StreakTrackerTestCase))
    
    # Run the tests with our custom runner
    runner = CustomTextTestRunner(verbosity=2)
    runner.run(test_suite)
