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

from test_generation import (
    TestGenerator, TestQuestion, TestSet, 
    ContextExpandedFilteredRetriever,
    evaluate_test_answers, get_user_tests, get_test_by_id,
    generate_and_save_test, set_collections
)

class TestTestGenerator(unittest.TestCase):

    @patch('test_generation.ChatOllama')
    @patch('test_generation.OllamaEmbeddings')
    @patch('test_generation.FAISS')
    def setUp(self, mock_faiss, mock_embeddings, mock_llm):
        """Set up test environment with mocked dependencies"""
        # Configure mocks
        self.mock_llm_instance = MagicMock()
        mock_llm.return_value = self.mock_llm_instance
        
        self.mock_embeddings_instance = MagicMock()
        mock_embeddings.return_value = self.mock_embeddings_instance
        
        self.mock_vector_store = MagicMock()
        mock_faiss.load_local.return_value = self.mock_vector_store
        
        # Create generator instance
        self.generator = TestGenerator("mock_index_path")
        
        # Set mock collections
        self.mock_tests_collection = MagicMock()
        self.mock_attempts_collection = MagicMock()
        set_collections(self.mock_tests_collection, self.mock_attempts_collection)

    def test_generator_initialization(self):
        """Test if TestGenerator initializes correctly"""
        self.assertIsNotNone(self.generator)
        self.assertEqual(self.generator.llm, self.mock_llm_instance)
        self.assertEqual(self.generator.embeddings, self.mock_embeddings_instance)
        self.assertEqual(self.generator.vector_store, self.mock_vector_store)

    def test_generate_test_structure(self):
        """Test generate_test method produces correct structure"""
        # Mock LLM output as if it returned JSON with questions
        sample_json = """
        [
          {
            "question_text": "What is 2+2?",
            "options": ["3", "4", "5", "6"],
            "correct_answer": "B",
            "explanation": "2+2 equals 4"
          },
          {
            "question_text": "What is differentiation?",
            "options": ["Finding area", "Finding volume", "Finding rate of change", "Finding pressure"],
            "correct_answer": "C",
            "explanation": "Differentiation is finding rate of change"
          }
        ]
        """
        
        # Configure mock to return this JSON
        self.mock_llm_instance.invoke.return_value = sample_json
        
        # Call generate_test
        test_data = self.generator.generate_test(
            topic="Math Basics",
            grade="11",
            subjects=["math"],
            num_questions=2
        )
        
        # Check structure
        self.assertIsInstance(test_data, dict)
        self.assertIn('topic', test_data)
        self.assertEqual(test_data['topic'], "Math Basics")
        
        # Check questions array
        self.assertIn('questions', test_data)
        self.assertIsInstance(test_data['questions'], list)
        self.assertEqual(len(test_data['questions']), 2)
        
        # Check question structure
        q1 = test_data['questions'][0]
        self.assertIn('question_text', q1)
        self.assertIn('options', q1)
        self.assertIn('correct_answer', q1)
        self.assertIn('explanation', q1)
        
        # Verify correct_answer conversion from letter to text
        self.assertEqual(q1['correct_answer'], "4")  # B converted to the text of option B

    def test_generate_and_save_test(self):
        """Test generate_and_save_test function"""
        # Mock TestGenerator.generate_test to return test data
        with patch('test_generation.TestGenerator.generate_test') as mock_generate:
            # Prepare mock return data
            mock_generate.return_value = {
                'topic': 'Math Basics',
                'questions': [
                    {
                        'question_text': 'What is 2+2?',
                        'options': ['3', '4', '5', '6'],
                        'correct_answer': '4',
                        'explanation': '2+2 equals 4'
                    }
                ]
            }
            
            # Mock the MongoDB insert
            self.mock_tests_collection.insert_one.return_value = MagicMock()
            self.mock_tests_collection.insert_one.return_value.inserted_id = ObjectId('1234567890abcdef12345678')
            
            # Call the function
            result = generate_and_save_test(
                user_id='1234567890abcdef12345678',
                title='Math Test',
                topic='Math Basics',
                grade='11',
                subjects=['math'],
                num_questions=1
            )
            
            # Check the result
            self.assertTrue(result['success'])
            self.assertEqual(result['test_id'], '1234567890abcdef12345678')
            
            # Verify MongoDB was called correctly
            self.mock_tests_collection.insert_one.assert_called_once()
            args = self.mock_tests_collection.insert_one.call_args[0][0]
            self.assertEqual(args['title'], 'Math Test')
            self.assertEqual(args['topic'], 'Math Basics')
            self.assertEqual(args['grade'], '11')
            self.assertEqual(args['subjects'], ['math'])
            self.assertEqual(len(args['questions']), 1)

    def test_evaluate_test_answers(self):
        """Test evaluate_test_answers function"""
        # Mock getting test from MongoDB
        test_id = '1234567890abcdef12345678'
        user_id = '1234567890abcdef87654321'
        
        # Create a mock test in the collection
        mock_test = {
            '_id': ObjectId(test_id),
            'user_id': ObjectId(user_id),
            'title': 'Math Test',
            'topic': 'Math Basics',
            'questions': [
                {
                    'question_text': 'What is 2+2?',
                    'options': ['3', '4', '5', '6'],
                    'correct_answer': '4',
                    'explanation': '2+2 equals 4'
                },
                {
                    'question_text': 'What is 3+3?',
                    'options': ['4', '5', '6', '7'],
                    'correct_answer': '6',
                    'explanation': '3+3 equals 6'
                }
            ]
        }
        
        self.mock_tests_collection.find_one.return_value = mock_test
        
        # User answers
        answers = [
            {'question_id': 0, 'answer': '4'},  # Correct
            {'question_id': 1, 'answer': '5'}   # Incorrect
        ]
        
        # Call the function
        result = evaluate_test_answers(user_id, test_id, answers)
        
        # Check the result
        self.assertTrue(result['success'])
        self.assertEqual(result['test_title'], 'Math Test')
        self.assertEqual(result['test_topic'], 'Math Basics')
        
        # Check evaluation array
        self.assertEqual(len(result['evaluation']), 2)
        self.assertTrue(result['evaluation'][0]['is_correct'])
        self.assertFalse(result['evaluation'][1]['is_correct'])
        
        # Check score
        self.assertEqual(result['score']['correct'], 1)
        self.assertEqual(result['score']['total'], 2)
        self.assertEqual(result['score']['percentage'], 50.0)
        
        # Verify attempt was saved
        self.mock_attempts_collection.insert_one.assert_called_once()

    def test_get_user_tests(self):
        """Test get_user_tests function"""
        user_id = '1234567890abcdef87654321'
        
        # Mock tests in the collection
        mock_tests = [
            {
                '_id': ObjectId('1234567890abcdef12345678'),
                'user_id': ObjectId(user_id),
                'title': 'Math Test',
                'topic': 'Math Basics',
                'grade': '11',
                'subjects': ['math'],
                'created_at': datetime.now(pytz.UTC),
                'questions': [{'question_text': 'What is 2+2?'}] * 5
            },
            {
                '_id': ObjectId('1234567890abcdef12345679'),
                'user_id': ObjectId(user_id),
                'title': 'Physics Test',
                'topic': 'Mechanics',
                'grade': '11',
                'subjects': ['physics'],
                'created_at': datetime.now(pytz.UTC),
                'questions': [{'question_text': 'What is force?'}] * 3
            }
        ]
        
        # Mock find method on collection
        self.mock_tests_collection.find.return_value.sort.return_value.skip.return_value.limit.return_value = mock_tests
        self.mock_tests_collection.count_documents.return_value = 2
        
        # No attempts yet for these tests
        self.mock_attempts_collection.find.return_value.sort.return_value.limit.return_value = []
        
        # Call the function
        result = get_user_tests(user_id)
        
        # Check the result
        self.assertTrue(result['success'])
        self.assertEqual(len(result['tests']), 2)
        self.assertEqual(result['total'], 2)
        self.assertEqual(result['page'], 1)
        
        # Check test structure
        test1 = result['tests'][0]
        self.assertEqual(test1['title'], 'Math Test')
        self.assertEqual(test1['num_questions'], 5)
        self.assertIn('attempt_history', test1)

    def test_get_test_by_id(self):
        """Test get_test_by_id function"""
        user_id = '1234567890abcdef87654321'
        test_id = '1234567890abcdef12345678'
        
        # Mock test in the collection
        mock_test = {
            '_id': ObjectId(test_id),
            'user_id': ObjectId(user_id),
            'title': 'Math Test',
            'topic': 'Math Basics',
            'grade': '11',
            'subjects': ['math'],
            'created_at': datetime.now(pytz.UTC),
            'questions': [
                {
                    'question_type': 'mcq',
                    'question_text': 'What is 2+2?',
                    'options': ['3', '4', '5', '6'],
                    'correct_answer': '4',
                    'explanation': '2+2 equals 4'
                }
            ]
        }
        
        self.mock_tests_collection.find_one.return_value = mock_test
        
        # Call the function
        result = get_test_by_id(test_id, user_id)
        
        # Check the result
        self.assertTrue(result['success'])
        
        # Check test structure
        test = result['test']
        self.assertEqual(test['title'], 'Math Test')
        self.assertEqual(test['grade'], '11')
        self.assertEqual(test['subjects'], ['math'])
        
        # Check if correct answer is not included (default hide_answers=False)
        self.assertNotIn('correct_answer', test['questions'][0])
        
        # Now check with show_answers=True
        result_with_answers = get_test_by_id(test_id, user_id, show_answers=True)
        self.assertIn('correct_answer', result_with_answers['test']['questions'][0])


if __name__ == '__main__':
    unittest.main()
