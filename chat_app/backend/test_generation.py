import os
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import time  # Add import for time module

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from pydantic import BaseModel, Field  # Updated import

from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings

import faiss
from langchain_community.vectorstores import FAISS
import json
from bson import ObjectId
from bson.errors import InvalidId  # Fixed import for InvalidId
import datetime
import pytz
import re

# MongoDB collections (to be set by the Flask app)
tests_collection = None
test_attempts_collection = None

# Timezone configuration
IST = pytz.timezone('Asia/Kolkata')

# Define this function at the module level so it can be imported
def set_collections(tests_coll, attempts_coll):
    """Set MongoDB collections for tests and attempts."""
    global tests_collection, test_attempts_collection
    tests_collection = tests_coll
    test_attempts_collection = attempts_coll


class TestQuestion(BaseModel):
    """Schema for a test question with multiple choice options."""
    question_text: str = Field(description="The text of the question")
    options: List[str] = Field(description="List of possible answer options")
    correct_answer: str = Field(description="The correct answer option")
    explanation: str = Field(description="Explanation of why the answer is correct")


class TestSet(BaseModel):
    """Schema for a complete test set."""
    topic: str = Field(description="The topic of this test")
    questions: List[TestQuestion] = Field(description="List of test questions")


class ContextExpandedFilteredRetriever(BaseRetriever):
    """Retriever that fetches top result plus surrounding context chunks with filtering."""
    
    vectorstore: Any = Field(description="Vector store for retrievals")
    grade: Optional[str] = Field(default=None, description="Grade level for filtering")
    subjects: Optional[List[str]] = Field(default=None, description="List of subject codes for filtering")
    context_window: int = Field(default=5, description="Number of context chunks to retrieve")
    
    def _get_relevant_documents(self, query: str) -> List[Document]:
        # Create filters if grade and subjects are provided
        filter_dict = {}
        if self.grade and self.subjects:
            filter_dict = {
                "$and": [
                    {"grade": self.grade},
                    {"subject_code": {"$in": self.subjects}}
                ]
            }
        elif self.grade:
            filter_dict = {"grade": self.grade}
        elif self.subjects:
            filter_dict = {"subject_code": {"$in": self.subjects}}
        
        # Get the top result with filters
        results = self.vectorstore.similarity_search(
            query, 
            k=1,
            filter=filter_dict if filter_dict else None
        )
        if not results:
            return []
            
        top_result = results[0]
        
        # Extract metadata to identify position
        split_number = top_result.metadata.get("split_number", 0)
        total_splits = top_result.metadata.get("total_splits", 0)
        chapter_code = top_result.metadata.get("chapter_code")
        subject_code = top_result.metadata.get("subject_code")
        
        # Calculate range of splits to retrieve
        start_split = max(1, split_number - self.context_window)
        end_split = min(total_splits, split_number + self.context_window)
        
        # Retrieve all the relevant splits
        expanded_results = [top_result]  # Start with the top result
        
        # Get context before the top result
        for i in range(start_split, split_number):
            # Create a filter for this specific split
            split_filter = {
                "$and": [
                    {"subject_code": subject_code},
                    {"chapter_code": chapter_code},
                    {"split_number": i}
                ]
            }
            if self.grade:
                split_filter["$and"].append({"grade": self.grade})
            
            context_docs = self.vectorstore.similarity_search(
                "", # Empty query to avoid biasing results
                k=1,
                filter=split_filter
            )
            
            if context_docs:
                expanded_results.insert(0, context_docs[0])  # Add before top result
        
        # Get context after the top result
        for i in range(split_number + 1, end_split + 1):
            # Create a filter for this specific split
            split_filter = {
                "$and": [
                    {"subject_code": subject_code},
                    {"chapter_code": chapter_code},
                    {"split_number": i}
                ]
            }
            if self.grade:
                split_filter["$and"].append({"grade": self.grade})
            
            context_docs = self.vectorstore.similarity_search(
                "", # Empty query to avoid biasing results
                k=1,
                filter=split_filter
            )
            
            if context_docs:
                expanded_results.append(context_docs[0])  # Add after top result
        
        return expanded_results


class TestGenerator:
    def __init__(self, index_path="faiss_index"):
        """Initialize the test generator with the given FAISS index path."""
        self.llm = ChatOllama(model="llama3.1", temperature=0.2)
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        # Fixed FAISS index loading
        try:
            # Try to load as a directory first
            index_path_obj = Path(index_path)
            if index_path_obj.is_dir():
                self.vector_store = FAISS.load_local(index_path, self.embeddings, allow_dangerous_deserialization=True)
            else:
                # If not a directory, assume it's a single file
                # Load from a single file format
                self.vector_store = self._load_faiss_from_file(index_path)
        except Exception as e:
            print(f"Error loading FAISS index: {e}")
            print("Creating an empty FAISS index for demonstration")
            # Create an empty index for demonstration
            example_texts = ["This is a placeholder document for the empty index."]
            self.vector_store = FAISS.from_texts(example_texts, self.embeddings)
        
        self.question_template = """Generate {num_questions} multiple choice test questions based ONLY on the following context:
        
        {context}
        
        Topic to focus on: {topic}
        
        For each question:
        1. Create a clear, challenging but fair question about the topic
        2. Provide exactly 4 answer options (A, B, C, D)
        3. Clearly indicate which option is correct
        4. Provide a brief explanation for why the correct answer is right
        
        Format each question PRECISELY as a JSON object with these fields:
        - question_text: the question
        - options: array of 4 options with each option as a separate string in quotes ["Option A", "Option B", "Option C", "Option D"]
        - correct_answer: which option is correct (just the letter A, B, C, or D)
        - explanation: why the correct answer is right
        
        Return an array of these question objects in valid JSON format like this:
        ```json
        [
          {{
            "question_text": ,
            "options": 
            "correct_answer": ,
            "explanation":
          }},
          ...
        ]
        ```
        
        Ensure ALL JSON syntax is valid with proper quotes around strings and commas between elements.
        """
        
        self.answer_template = """Based on the following context:
        
        {context}
        
        Answer the multiple choice question below. Choose the BEST answer based ONLY on the information in the context.
        
        Question: {question}
        Options: {options}
        
        Provide:
        1. The correct answer (A, B, C, or D)
        2. A detailed explanation of why this answer is correct and why the others are incorrect
        """
    
    def _load_faiss_from_file(self, index_file):
        """Helper method to load FAISS from a single file."""
        # This is a simplified implementation - you may need to adapt this
        # to your specific FAISS index format
        index = faiss.read_index(index_file)
        return FAISS(self.embeddings.embed_query, index, {}, {})

    def generate_test(self, topic: str, grade: Optional[str] = None, subjects: Optional[List[str]] = None, num_questions: int = 5):
        """Generate a test on a specific topic with the given parameters."""
        print(f"Generating test on topic: {topic}, Grade: {grade}, Subjects: {subjects}")
        
        # Create retriever with optional grade and subject filters
        retriever = ContextExpandedFilteredRetriever(
            vectorstore=self.vector_store,
            grade=grade,
            subjects=subjects,
            context_window=5
        )
        
        # Create the prompt template for question generation
        question_prompt = ChatPromptTemplate.from_template(self.question_template)
        
        # Build the question generation chain
        question_chain = (
            {"context": retriever, "topic": RunnablePassthrough(), "num_questions": lambda _: num_questions}
            | question_prompt
            | self.llm
        )
        
        # Add delay before generation to ensure model is ready
        time.sleep(1)  # Wait 1 second before starting generation
        
        # Get the response and parse it into JSON
        max_retries = 2
        retry_delay = 2  # seconds
        raw_questions = None
        
        for attempt in range(max_retries + 1):
            try:
                print(f"Attempt {attempt + 1} for test generation...")
                raw_questions = question_chain.invoke(topic)
                # Add a delay after generation to ensure completion
                time.sleep(2)  # Wait 2 seconds after generation
                break
            except Exception as e:
                print(f"Error in generation attempt {attempt + 1}: {e}")
                if attempt < max_retries:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    raise
        
        # Print raw output for debugging
        print(f"Raw LLM output type: {type(raw_questions)}")
        raw_output_str = raw_questions.content if hasattr(raw_questions, 'content') else str(raw_questions)
        print(f"Raw LLM output preview: {raw_output_str[:200]}...")
        
        try:
            # Extract the content from the response
            question_content = raw_questions.content if hasattr(raw_questions, 'content') else str(raw_questions)
            
            # Extract JSON from markdown code blocks if present
            json_match = re.search(r'```(?:json)?\s*\n([\s\S]*?)\n```', question_content)
            if json_match:
                question_content = json_match.group(1).strip()
                print("Extracted JSON from code block")
            
            # Clean the JSON content to handle common formatting issues
            question_content = question_content.strip()
            
            # Add another delay before parsing to ensure complete response
            time.sleep(1)
            
            # Try to parse as an array of questions directly
            try:
                questions = json.loads(question_content)
                print(f"Successfully parsed JSON: found {len(questions)} questions")
                
                # Additional delay after successful parsing
                time.sleep(1)
            except json.JSONDecodeError as e:
                print(f"Initial JSON parsing failed: {e}")
                
                # Try to extract just the questions array if it's part of a larger JSON object
                array_match = re.search(r'"questions"\s*:\s*(\[[\s\S]*?\])', question_content)
                if array_match:
                    try:
                        questions = json.loads(array_match.group(1))
                        print(f"Extracted questions array: found {len(questions)} questions")
                        # Add delay after parsing from array
                        time.sleep(1)
                    except json.JSONDecodeError:
                        raise  # Let the outer exception handler deal with it
                else:
                    raise  # Re-raise if we couldn't find a questions array
            
            # Process questions to ensure "correct_answer" has full text instead of just A, B, C, D
            for question in questions:
                # Standardize question format - ensure all required fields exist
                if "question_text" not in question and "question" in question:
                    question["question_text"] = question["question"]
                
                # If correct_answer is a single letter (A, B, C, D)
                if question.get('correct_answer') in ['A', 'B', 'C', 'D']:
                    # Convert to index (0, 1, 2, 3)
                    index = ord(question['correct_answer']) - ord('A')
                    # Replace letter with full option text if index is valid
                    if 0 <= index < len(question['options']):
                        question['correct_answer'] = question['options'][index]
            
            # Format for return
            test_set = {
                "topic": topic,
                "questions": questions,
                "metadata": {
                    "grade": grade,
                    "subjects": subjects,
                    "num_questions": num_questions
                }
            }
            
            # Final delay before returning to ensure everything is ready
            time.sleep(2)
            
            return test_set
            
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"Error parsing question response: {e}")
            print(f"Raw response sample: {str(raw_questions)[:500]}")
            
            # Add delay before fallback
            time.sleep(1)
            
            # Attempt to extract JSON manually as a fallback
            try:
                # Try multiple extraction strategies
                content_str = str(raw_questions)
                
                # Strategy 1: Find array pattern [...]
                json_start = content_str.find('[')
                json_end = content_str.rfind(']') + 1
                
                if json_start >= 0 and json_end > json_start:
                    extracted_json = content_str[json_start:json_end]
                    print(f"Found JSON array from position {json_start} to {json_end}")
                    questions = json.loads(extracted_json)
                    
                    # Process correct_answer fields as above
                    for question in questions:
                        if question.get('correct_answer') in ['A', 'B', 'C', 'D']:
                            index = ord(question['correct_answer']) - ord('A')
                            if 0 <= index < len(question['options']):
                                question['correct_answer'] = question['options'][index]
                    
                    test_set = {
                        "topic": topic,
                        "questions": questions,
                        "metadata": {
                            "grade": grade,
                            "subjects": subjects,
                            "num_questions": len(questions)
                        }
                    }
                    return test_set
                
                # Strategy 2: Try to find questions with regex
                question_pattern = r'\{[\s\S]*?"question(?:_text)?"\s*:\s*"([^"]+)"[\s\S]*?\}'
                question_matches = re.findall(question_pattern, content_str)
                
                if question_matches:
                    print(f"Found {len(question_matches)} question matches with regex")
                    
                    # Try to reconstruct a minimal valid JSON array
                    reconstructed_questions = []
                    for q_text in question_matches[:num_questions]:  # Limit to requested number
                        reconstructed_questions.append({
                            "question_text": q_text,
                            "options": ["Option A", "Option B", "Option C", "Option D"],
                            "correct_answer": "Option A",  # Default
                            "explanation": "Generated through fallback parsing. Please review."
                        })
                    
                    if reconstructed_questions:
                        test_set = {
                            "topic": topic,
                            "questions": reconstructed_questions,
                            "metadata": {
                                "grade": grade,
                                "subjects": subjects,
                                "num_questions": len(reconstructed_questions)
                            }
                        }
                        print(f"Created {len(reconstructed_questions)} questions through regex fallback")
                        return test_set
                
            except Exception as fallback_error:
                print(f"Fallback extraction failed: {fallback_error}")
            
            # Try a different approach with the LLM
            try:
                print("Attempting to regenerate with simpler prompt...")
                # Create a simpler prompt that explicitly requires valid JSON
                simpler_prompt = ChatPromptTemplate.from_template(
                    """Create {num_questions} multiple choice test questions about {topic}.
                    
                    Return ONLY a valid JSON array of question objects with NO explanation or other text.
                    Each question must have these fields:
                    - question_text: the question text
                    - options: an array of 4 possible answers
                    - correct_answer: the full text of the correct option
                    - explanation: brief explanation of the answer
                    
                    Example format:
                    [
                      {
                        "question_text": "What is 2+2?",
                        "options": ["3", "4", "5", "6"],
                        "correct_answer": "4",
                        "explanation": "2+2 equals 4"
                      }
                    ]
                    """
                )
                
                # Try again with simpler prompt
                simpler_chain = (
                    {"topic": RunnablePassthrough(), "num_questions": lambda _: num_questions}
                    | simpler_prompt
                    | self.llm
                    | StrOutputParser()
                )
                
                retry_result = simpler_chain.invoke(topic)
                
                # Extract JSON - simpler output should have less formatting issues
                retry_content = retry_result.strip()
                json_match = re.search(r'(\[\s*\{.*\}\s*\])', retry_content, re.DOTALL)
                
                if json_match:
                    retry_json = json_match.group(1)
                    questions = json.loads(retry_json)
                    print(f"Retry successful! Generated {len(questions)} questions")
                    
                    test_set = {
                        "topic": topic,
                        "questions": questions,
                        "metadata": {
                            "grade": grade,
                            "subjects": subjects,
                            "num_questions": len(questions)
                        }
                    }
                    return test_set
                else:
                    print("Retry didn't produce valid JSON")
            
            except Exception as retry_error:
                print(f"Retry generation failed: {str(retry_error)}")
            
            # Return a simplified version with the raw output if all parsing fails
            return {
                "topic": topic,
                "error": "Failed to parse questions: " + str(e),
                "raw_output": raw_output_str[:1000]  # Truncate to avoid excessive output
            }

    # Other methods remain unchanged...

def is_valid_objectid(id_str):
    """Check if a string is a valid MongoDB ObjectId."""
    if not id_str or id_str == 'undefined' or id_str == 'null':
        return False
    try:
        ObjectId(id_str)
        return True
    except (InvalidId, TypeError):
        return False

def evaluate_test_answers(user_id: str, test_id: str, answers: List[Dict]) -> Dict[str, Any]:
    """
    Evaluate user answers for a test and save the attempt.
    
    Args:
        user_id: User ID submitting the answers
        test_id: ID of the test being taken
        answers: List of user answers with question_id and answer
        
    Returns:
        Dictionary with evaluation results
    """
    if tests_collection is None or test_attempts_collection is None:
        raise ValueError("MongoDB collections not initialized")
    
    # Validate test_id
    if not is_valid_objectid(test_id):
        return {
            'success': False,
            'error': 'Invalid test ID format'
        }
    
    # Get the test from the database
    test = tests_collection.find_one({'_id': ObjectId(test_id)})
    if not test:
        return {
            'success': False,
            'error': 'Test not found'
        }
    
    # Initialize the test generator for LLM evaluation
    generator = TestGenerator("./faiss-index")
    
    # Create a mapping of question_id to answer for faster lookups
    answer_map = {}
    for answer_data in answers:
        if isinstance(answer_data, dict) and 'question_id' in answer_data and 'answer' in answer_data:
            answer_map[answer_data['question_id']] = answer_data['answer']
        elif isinstance(answer_data, str):
            # Handle legacy format where answers is just a list of strings
            # Index in the list corresponds to question index
            answer_map[len(answer_map)] = answer_data
    
    # Evaluate answers
    evaluation_results = []
    correct_count = 0
    
    for i, question in enumerate(test['questions']):
        # Try to get the answer by question index or by explicit question_id
        user_answer = answer_map.get(i, None)
        if user_answer is None:
            # If no answer for this question, mark as incorrect
            evaluation_results.append({
                'question_number': i + 1,
                'question_text': question['question_text'],
                'user_answer': 'No answer provided',
                'correct_answer': question['correct_answer'],
                'is_correct': False,
                'explanation': 'No answer was provided for this question.'
            })
            continue
        
        # For MCQ questions, compare directly with correct answer
        if question.get('question_type', 'mcq') == 'mcq':
            # Direct comparison for multiple choice
            is_correct = user_answer.strip().lower() == question['correct_answer'].strip().lower()
            
            evaluation_results.append({
                'question_number': i + 1,
                'question_text': question['question_text'],
                'user_answer': user_answer,
                'correct_answer': question['correct_answer'],
                'is_correct': is_correct,
                'explanation': question.get('explanation', 'No explanation available.')
            })
            
            if is_correct:
                correct_count += 1
        else:
            # For non-MCQ questions, use LLM evaluation
            options = question.get('options', [])
            
            # Evaluate with LLM
            llm_evaluation = generator.evaluate_answer_with_llm(
                question_text=question['question_text'],
                correct_answer=question['correct_answer'],
                user_answer=user_answer,
                options=options,
                grade=test.get('grade'),
                subjects=test.get('subjects')
            )
            
            is_correct = llm_evaluation['is_correct']
            feedback = llm_evaluation['feedback']
            
            evaluation_results.append({
                'question_number': i + 1,
                'question_text': question['question_text'],
                'user_answer': user_answer,
                'correct_answer': question['correct_answer'],
                'is_correct': is_correct,
                'explanation': feedback or question.get('explanation', 'No explanation available.')
            })
            
            if is_correct:
                correct_count += 1
    
    # Calculate score
    total_questions = len(test['questions'])
    attempted_questions = len(answers)
    score_percentage = round((correct_count / total_questions) * 100, 1) if total_questions > 0 else 0
    
    # Create test attempt record
    test_attempt = {
        'user_id': ObjectId(user_id),
        'test_id': ObjectId(test_id),
        'timestamp': datetime.datetime.now(IST),
        'answers': answers,
        'evaluation_results': evaluation_results,
        'score': {
            'correct': correct_count,
            'total': total_questions,
            'percentage': score_percentage
        }
    }
    
    # Save the attempt to the database
    test_attempts_collection.insert_one(test_attempt)
    
    return {
        'success': True,
        'test_title': test['title'],
        'test_topic': test['topic'],
        'evaluation': evaluation_results,
        'score': {
            'correct': correct_count,
            'total': total_questions,
            'attempted': attempted_questions,
            'percentage': score_percentage
        }
    }

def get_test_by_id(test_id: str, user_id: str, show_answers: bool = False) -> Dict[str, Any]:
    """
    Get a specific test by ID.
    
    Args:
        test_id: ID of the test to retrieve
        user_id: User ID requesting the test
        show_answers: Whether to include correct answers
        
    Returns:
        Dictionary with test details
    """
    if tests_collection is None:
        raise ValueError("MongoDB collections not initialized")
    
    # Validate test_id
    if not is_valid_objectid(test_id):
        return {
            'success': False,
            'error': 'Invalid test ID format'
        }
    
    # Get the test from the database
    test = tests_collection.find_one({'_id': ObjectId(test_id)})
    if not test:
        return {
            'success': False,
            'error': 'Test not found'
        }
        
    # Check if the user has access to this test
    if str(test['user_id']) != user_id:
        return {
            'success': False,
            'error': 'You do not have access to this test'
        }
    
    # Format the test for response
    formatted_test = {
        'test_id': str(test['_id']),
        'title': test['title'],
        'topic': test['topic'],
        'grade': test['grade'],
        'subjects': test['subjects'],
        'created_at': test['created_at'].isoformat(),
        'questions': []
    }
    
    for question in test['questions']:
        q = {
            'question_type': question['question_type'],
            'question_text': question['question_text']
        }
        
        if question['question_type'] == 'mcq':
            q['options'] = question['options']
        
        if show_answers:
            q['correct_answer'] = question['correct_answer']
            q['explanation'] = question['explanation']
            if question['question_type'] == 'short_answer' and 'keywords' in question:
                q['keywords'] = question['keywords']
        
        formatted_test['questions'].append(q)
    
    return {
        'success': True,
        'test': formatted_test
    }

def get_user_tests(user_id: str, page: int = 1, per_page: int = 10, 
                  topic_filter: str = None, grade_filter: str = None, 
                  subject_filter: str = None) -> Dict[str, Any]:
    """
    Get a list of tests for a user with pagination and optional filtering.
    
    Args:
        user_id: User ID to get tests for
        page: Page number for pagination
        per_page: Number of items per page
        topic_filter: Optional filter for test topic
        grade_filter: Optional filter for grade level
        subject_filter: Optional filter for subject
        
    Returns:
        Dictionary with list of tests and pagination info
    """
    if tests_collection is None:
        raise ValueError("MongoDB collections not initialized")
    
    # Pagination parameters
    skip = (page - 1) * per_page
    
    # Filtering options
    filters = {'user_id': ObjectId(user_id)}
    
    # Optional topic filter
    if topic_filter:
        filters['topic'] = {'$regex': topic_filter, '$options': 'i'}
        
    # Optional grade filter
    if grade_filter:
        filters['grade'] = grade_filter
        
    # Optional subject filter
    if subject_filter:
        filters['subjects'] = subject_filter
    
    # Get total count for pagination
    total_tests = tests_collection.count_documents(filters)
    
    # Get the tests with pagination
    tests_cursor = tests_collection.find(filters).sort('created_at', -1).skip(skip).limit(per_page)
    
    # Format the tests for the response
    tests_list = []
    for test in tests_cursor:
        test_id = test['_id']
        
        # Get previous attempts for this test (limit to 5)
        previous_attempts = list(test_attempts_collection.find(
            {'user_id': ObjectId(user_id), 'test_id': test_id}
        ).sort('timestamp', -1).limit(5))
        
        # Format previous attempts
        attempt_history = []
        for attempt in previous_attempts:
            attempt_score = attempt.get('score', {})
            percentage = attempt_score.get('percentage', 0) if isinstance(attempt_score, dict) else attempt_score
            
            attempt_history.append({
                'score': percentage,
                'timestamp': attempt['timestamp'].isoformat(),
                'attempt_id': str(attempt['_id'])
            })
        
        formatted_test = {
            'test_id': str(test_id),
            'title': test['title'],
            'topic': test['topic'],
            'grade': test['grade'],
            'subjects': test['subjects'],
            'created_at': test['created_at'].isoformat(),
            'num_questions': len(test['questions']),
            'attempts': test.get('attempts', 0),
            'best_score': test.get('best_score', 0),
            'last_attempt_score': test.get('last_attempt_score', 0),
            'last_attempt_date': test.get('last_attempt_date', '').isoformat() if test.get('last_attempt_date') else None,
            'attempt_history': attempt_history
        }
        tests_list.append(formatted_test)
    
    return {
        'success': True,
        'tests': tests_list,
        'total': total_tests,
        'page': page,
        'per_page': per_page,
        'total_pages': (total_tests + per_page - 1) // per_page
    }

def generate_and_save_test(user_id: str, title: str, topic: str, grade: str, 
                          subjects: List[str], num_questions: int = 5) -> Dict[str, Any]:
    """
    Generate a test and save it to MongoDB.
    
    Args:
        user_id: User ID who is generating the test
        title: Title for the test
        topic: Topic to generate questions about
        grade: Grade level (e.g., "10", "11", "12")
        subjects: List of subjects to focus on
        num_questions: Number of questions to generate
        
    Returns:
        Dictionary with test details and ID
    """
    if tests_collection is None:
        raise ValueError("MongoDB collections not initialized")
    
    # Initialize the test generator
    generator = TestGenerator("./faiss-index")
    
    print(f"Starting test generation for topic: {topic}")
    
    # Generate the test with increased timeout
    start_time = time.time()
    test_data = generator.generate_test(
        topic=topic,
        grade=grade,
        subjects=subjects,
        num_questions=num_questions
    )
    generation_time = time.time() - start_time
    print(f"Test generation completed in {generation_time:.2f} seconds")
    
    # If there was an error in test generation
    if "error" in test_data:
        return {
            'success': False,
            'error': test_data['error'],
            'raw_output': test_data.get('raw_output', '')
        }
    
    # Add delay before saving to database to ensure all content is ready
    time.sleep(1)
    
    # Format the test for MongoDB
    current_time = datetime.datetime.now(IST)
    test_document = {
        'user_id': ObjectId(user_id),
        'title': title,
        'topic': test_data['topic'],
        'created_at': current_time,
        'grade': grade,
        'subjects': subjects,
        'questions': []
    }
    
    # Format the questions (currently all MCQ from TestGenerator)
    for q in test_data['questions']:
        question_doc = {
            'question_type': 'mcq',
            'question_text': q['question_text'],
            'options': q['options'],
            'correct_answer': q['correct_answer'],
            'explanation': q['explanation']
        }
        test_document['questions'].append(question_doc)
    
    # Insert into database
    result = tests_collection.insert_one(test_document)
    test_id = str(result.inserted_id)
    
    print(f"Test saved to database with ID: {test_id}")
    
    # Final delay before returning to ensure complete saving
    time.sleep(1)
    
    return {
        'success': True,
        'test_id': test_id,
        'test': {
            'title': test_document['title'],
            'topic': test_document['topic'],
            'grade': test_document['grade'],
            'subjects': test_document['subjects'],
            'questions': test_document['questions'],
            'num_questions': len(test_document['questions'])
        }
    }

if __name__ == "__main__":
    # Specify the path to your FAISS index
    index_path = "./faiss-index"  # Modify this to your actual index path
    
    # Create test generator
    generator = TestGenerator(index_path)
    
    print("Test Generator initialized successfully!")
    print("Running example test generation...")
    
    # Example: Generate a simple test
    simple_test = generator.generate_test(
        topic="Python Programming Fundamentals",
        num_questions=3
    )
    generator.print_test(simple_test)