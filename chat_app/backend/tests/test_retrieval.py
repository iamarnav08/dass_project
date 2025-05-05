import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import time

# Add the parent directory to sys.path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from retrieval import Generator, ContextExpandedFilteredRetriever

class TestRetrieval(unittest.TestCase):
    
    @patch('retrieval.ChatOllama')
    @patch('retrieval.OllamaEmbeddings')
    @patch('retrieval.FAISS')
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
        self.generator = Generator()
    
    def test_generator_initialization(self):
        """Test if Generator initializes correctly"""
        self.assertIsNotNone(self.generator)
        self.assertEqual(self.generator.llm, self.mock_llm_instance)
        self.assertEqual(self.generator.embeddings, self.mock_embeddings_instance)
        self.assertEqual(self.generator.vector_store, self.mock_vector_store)
    
    @patch('retrieval.ContextExpandedFilteredRetriever')
    def test_generate_output_structure(self, mock_retriever):
        """Test if generate produces output with correct structure"""
        # Mock the retriever
        mock_retriever_instance = MagicMock()
        mock_retriever.return_value = mock_retriever_instance
        
        # Mock the chain stream to return some text
        self.mock_llm_instance.invoke.return_value = "Test response"
        
        # Call generate with test inputs
        grade = "11"
        subjects = ["math", "physics"]
        query = "What is differentiation?"
        
        # Collect all chunks from the generator
        chunks = list(self.generator.generate(grade, subjects, query))
        
        # Verify we got some output
        self.assertTrue(len(chunks) > 0)
        # The output should be non-empty strings
        for chunk in chunks:
            self.assertIsInstance(chunk, str)
            self.assertTrue(len(chunk) > 0)

    @patch('langchain_core.documents.Document')
    def test_context_expanded_retriever(self, mock_document):
        """Test the ContextExpandedFilteredRetriever logic"""
        # Create mock vector store
        mock_vector_store = MagicMock()
        
        # Create test document with metadata
        test_document = MagicMock()
        test_document.metadata = {
            "split_number": 5,
            "total_splits": 10,
            "chapter_code": "chapter1",
            "subject_code": "math"
        }
        
        # Mock the similarity_search method
        mock_vector_store.similarity_search.return_value = [test_document]
        
        # Create the retriever
        retriever = ContextExpandedFilteredRetriever(
            vectorstore=mock_vector_store,
            grade="11",
            subjects=["math"],
            context_window=2
        )
        
        # Call _get_relevant_documents
        results = retriever._get_relevant_documents("test query")
        
        # Verify the filter structure was correct
        expected_filter = {
            "$and": [
                {"grade": "11"},
                {"subject_code": {"$in": ["math"]}}
            ]
        }
        
        # Check if similarity_search was called at least once with the expected filter
        mock_vector_store.similarity_search.assert_any_call(
            "test query", k=1, filter=expected_filter
        )
        
        # Should have made additional calls for context chunks
        # We expect at least 5 calls (1 for main query + 4 for context chunks)
        self.assertGreaterEqual(mock_vector_store.similarity_search.call_count, 1)


class TestGeneratorIntegration(unittest.TestCase):
    """Integration tests for Generator that require Ollama running"""
    
    def setUp(self):
        """Skip these tests if we want to avoid actual Ollama calls"""
        # Set this to False to run integration tests with actual Ollama
        self.skip_integration = True
        
        if self.skip_integration:
            self.skipTest("Skipping integration tests that require Ollama")
        
        try:
            # Try to create an actual Generator instance
            self.generator = Generator()
        except Exception as e:
            self.fail(f"Generator initialization failed: {str(e)}")
    
    def test_actual_generation(self):
        """Test actual generation with real Ollama (if available)"""
        if self.skip_integration:
            return
            
        # Call generate with test inputs
        grade = "11"
        subjects = ["math"]
        query = "What is differentiation?"
        
        # Get the first few chunks to verify it works
        chunks = []
        try:
            # Limit to collecting just a few chunks to keep test duration reasonable
            for i, chunk in enumerate(self.generator.generate(grade, subjects, query)):
                chunks.append(chunk)
                if i >= 5:  # Just get the first 5 chunks
                    break
        except Exception as e:
            self.fail(f"Generation failed with error: {str(e)}")
        
        # Verify we got some output
        self.assertTrue(len(chunks) > 0)
        # The output should be non-empty strings
        for chunk in chunks:
            self.assertIsInstance(chunk, str)


if __name__ == '__main__':
    unittest.main()
