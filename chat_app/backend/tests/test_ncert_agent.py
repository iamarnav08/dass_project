import unittest
from unittest.mock import patch, MagicMock, ANY
import sys
import os
import json

# Add the parent directory to sys.path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import quick_start_ncert_agent
from quick_start_ncert_agent import NCERTGenerator, setup_vectorstore

class TestNCERTAgent(unittest.TestCase):

    @patch('quick_start_ncert_agent.setup_vectorstore')
    @patch('quick_start_ncert_agent.setup_orchestrator')
    def setUp(self, mock_setup_orchestrator, mock_setup_vectorstore):
        """Set up test environment with mocked dependencies"""
        # Configure mocks
        self.mock_vector_store = MagicMock()
        mock_setup_vectorstore.return_value = self.mock_vector_store
        
        self.mock_orchestrator = MagicMock()
        mock_setup_orchestrator.return_value = self.mock_orchestrator

        # Create generator instance with mocks
        with patch.object(NCERTGenerator, '__init__', return_value=None):
            self.generator = NCERTGenerator()
            self.generator.vector_store = self.mock_vector_store
            self.generator.orchestrator = self.mock_orchestrator

    def test_chunk_response(self):
        """Test the _chunk_response method"""
        test_response = "This is a test response that should be split into chunks based on the specified chunk size."
        chunks = list(self.generator._chunk_response(test_response, chunk_size=5))
        
        # Check that we got the right number of chunks
        expected_chunks = 3  # With chunk size 5, we expect around 3 chunks
        self.assertGreaterEqual(len(chunks), expected_chunks - 1)
        self.assertLessEqual(len(chunks), expected_chunks + 1)
        
        # Reconstruct the response and check it matches
        reconstructed = ' '.join(chunks)
        self.assertEqual(reconstructed, test_response)

    @patch('quick_start_ncert_agent.Message')
    @patch('quick_start_ncert_agent.EphemeralMemory')
    def test_generate_nonexistent_conversation(self, mock_memory, mock_message):
        """Test generate method with a new conversation"""
        # Mock classifier to return QA agent
        self.mock_orchestrator.classifier.classify.return_value = "ncert_qa_agent"
        
        # Mock agent handling
        mock_qa_agent = MagicMock()
        mock_qa_agent.handle_message.return_value = "Test response from QA agent"
        self.mock_orchestrator.agent_registry.get_agent.return_value = mock_qa_agent
        
        # Set up memory mock
        mock_memory.memory_repository.get_thread.return_value = None
        
        # Call generate with test inputs
        grade = "11"
        subjects = ["math"]
        query = "What is differentiation?"
        
        # Collect generator output
        response_chunks = list(self.generator.generate(
            grade=grade,
            subjects=subjects,
            query=query,
            conversation_id=None,
            store_messages=True
        ))
        
        # Verify interaction with orchestrator
        self.mock_orchestrator.classifier.classify.assert_called_once()
        self.mock_orchestrator.agent_registry.get_agent.assert_called_once()
        
        # Check we got response
        self.assertTrue(len(response_chunks) > 0)
        
        # Verify stored message in memory
        mock_memory.store_message.assert_called()

    @patch('quick_start_ncert_agent.EphemeralMemory')
    def test_search_pattern_handling(self, mock_memory):
        """Test handling of search patterns in agent responses"""
        # Set up mocks
        self.mock_orchestrator.classifier.classify.return_value = "ncert_qa_agent"
        
        # Create mock agent that includes search tags
        mock_qa_agent = MagicMock()
        mock_qa_agent.handle_message.return_value = '<search query="differentiation">We should search for info about differentiation</search>'
        self.mock_orchestrator.agent_registry.get_agent.return_value = mock_qa_agent
        
        # Mock thread
        mock_thread = MagicMock()
        mock_thread.messages = []
        mock_memory.memory_repository.get_thread.return_value = mock_thread
        
        # Mock VectorSearchTool
        with patch('quick_start_ncert_agent.VectorSearchTool') as mock_search_tool:
            # Set up search results
            mock_search_tool.search_vectorstore.return_value = json.dumps({
                "results": [
                    {"content": "Differentiation is the process of finding the derivative.", 
                     "metadata": {"source": "Math Chapter 3"}}
                ]
            })
            
            # Call generate
            response_chunks = list(self.generator.generate(
                grade="11",
                subjects=["math"],
                query="What is differentiation?",
                conversation_id="test_convo",
                store_messages=True
            ))
            
            # Verify search was called
            mock_search_tool.search_vectorstore.assert_called_once()
            
            # Check response
            self.assertTrue(len(response_chunks) > 0)
            combined_response = ''.join(response_chunks)
            self.assertIn("Here's what I found", combined_response)

    @patch('quick_start_ncert_agent.test_generation')
    @patch('quick_start_ncert_agent.EphemeralMemory')
    def test_quiz_generation(self, mock_memory, mock_test_generation):
        """Test quiz generation flow"""
        # Set up mocks for quiz agent
        self.mock_orchestrator.classifier.classify.return_value = "ncert_quiz_agent"
        
        # Mock the test generation result
        mock_test_generation.generate_and_save_test.return_value = {
            'success': True,
            'test_id': '1234567890abcdef12345678',
            'test': {
                'title': 'Test on Differentiation',
                'topic': 'Differentiation',
                'questions': [{'question_text': 'Test question'}] * 5
            }
        }
        
        # Set up memory mock
        mock_thread = MagicMock()
        mock_thread.messages = []
        mock_thread.metadata = {'user_id': '1234567890'}
        mock_memory.memory_repository.get_thread.return_value = mock_thread
        
        # Call generate for quiz
        response_chunks = list(self.generator.generate(
            grade="11",
            subjects=["math"],
            query="Create a quiz on differentiation",
            conversation_id="test_convo",
            store_messages=True
        ))
        
        # Check test generation was called
        mock_test_generation.generate_and_save_test.assert_called_once()
        
        # Verify response contains test link
        combined_response = ''.join(response_chunks)
        self.assertIn("I've created a test", combined_response)
        self.assertIn("test/", combined_response)

    def test_setup_vectorstore(self):
        """Test vectorstore setup with mocked dependencies"""
        with patch('quick_start_ncert_agent.OllamaEmbeddings') as mock_embeddings:
            with patch('quick_start_ncert_agent.FAISSCPUVectorstoreRepository') as mock_repo:
                # Configure mocks
                mock_embeddings_instance = MagicMock()
                mock_embeddings.return_value = mock_embeddings_instance
                
                mock_repo_instance = MagicMock()
                mock_repo.return_value = mock_repo_instance
                
                # Call the function
                result = quick_start_ncert_agent.setup_vectorstore()
                
                # Check the result
                self.assertEqual(result, mock_repo_instance)
                mock_repo_instance.load_vectorstore.assert_called_once()


if __name__ == '__main__':
    unittest.main()
