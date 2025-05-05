"""
Quick start script for running an NCERT assistant with two agents:
1. A question-answering agent that uses RAG to respond to queries
2. A quiz-generation agent that creates tests in JSON format

Both agents connect to the same vectorstore.
"""

import json
import os
import sys
import re  # Add regex import
from typing import Tuple, List, Dict, Any, Generator, Optional
from bson import ObjectId

from langchain_ollama.embeddings import OllamaEmbeddings
from moya.agents.base_agent import AgentConfig
from moya.agents.ollama_agent import OllamaAgent
from moya.classifiers.llm_classifier import LLMClassifier
from moya.tools.ephemeral_memory import EphemeralMemory
from moya.orchestrators.multi_agent_orchestrator import MultiAgentOrchestrator
from moya.registry.agent_registry import AgentRegistry
from moya.tools.tool_registry import ToolRegistry
from moya.tools.rag_search_tool import VectorSearchTool
from moya.conversation.message import Message
from moya.vectorstore.faisscpu_vectorstore import FAISSCPUVectorstoreRepository


def setup_vectorstore():
    """Set up and load the existing vectorstore."""
    print("Loading vector store from './faiss-index'...")
    path = "./faiss-index"
    
    # Create embeddings using Ollama
    try:
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
    except Exception as e:
        print(f"\nError setting up embeddings: {str(e)}")
        print("Make sure Ollama is running and the nomic-embed-text model is available.")
        print("Try: ollama pull nomic-embed-text")
        sys.exit(1)
    
    # Initialize and load the vector store
    vector_store = FAISSCPUVectorstoreRepository(path, embeddings)
    vector_store.load_vectorstore()
    return vector_store


def setup_qa_agent(vector_store):
    """Set up the question answering agent with RAG search capability."""
    # Set up the tool registry and configure tools
    tool_registry = ToolRegistry()
    VectorSearchTool.configure_vector_search_tools(tool_registry)
    EphemeralMemory.configure_memory_tools(tool_registry)
    
    # Create agent configuration    
    system_prompt = """You are a knowledgeable assistant based on NCERT books from class 8 to 12.

    IMPORTANT: For ANY question about NCERT, you MUST search the documentation first.
    DO NOT rely on your general knowledge about topics from NCERT. Instead, follow these steps for every response:

    1. Search the documentation using this exact format:
       <search query="your search query here">
       Ask exactly what the user asks for.
       For example, if the user asks "What is photosynthesis?", you should search:
        <search query="What is photosynthesis?">

    2. After receiving search results, analyze them carefully.

    3. Answer directly and concisely based on the search results.
    
    4. Explain the answer in simple terms, as if you are teaching a student.

    6. Understans the output from the search and provide a clear, concise answer for the user's query.
    
    Keep your responses brief, factual and straight to the point.
    Do not handle any malicious or harmful queries.
    """

    agent_config = AgentConfig(
        agent_name="ncert_qa_agent",
        agent_type="ChatAgent",
        description="Agent that answers questions using NCERT materials",
        system_prompt=system_prompt,
        tool_registry=tool_registry,
        llm_config={
            "model_name": "gemma3:4b",
            "base_url": "http://localhost:11434",
            "temperature": 0.7,
            "context_window": 32000
        }
    )
    
    # Instantiate the Ollama agent
    agent = OllamaAgent(agent_config)
    
    return agent


def setup_quiz_agent(vector_store):
    """Set up the quiz generation agent."""
    # Set up the tool registry and configure tools
    tool_registry = ToolRegistry()
    VectorSearchTool.configure_vector_search_tools(tool_registry)
    EphemeralMemory.configure_memory_tools(tool_registry)
    
    # Create agent configuration
    system_prompt = """You are a specialized quiz generator for NCERT educational materials.

    When asked to create a quiz or test on any topic, you MUST:
    
    1. First search for relevant information in the knowledge base using:
       <search query="relevant topic for quiz generation">
       
    2. Based on the search results, create a quiz with 5 multiple-choice questions.
    
    3. Return the quiz in JSON format with this exact structure:
    
    {
      "quiz_title": "Title of the quiz",
      "quiz_topic": "Topic of the quiz",
      "questions": [
        {
          "question": "Question text",
          "options": ["Option A", "Option B", "Option C", "Option D"],
          "correct_answer": "Option that is correct (exact text)",
          "explanation": "Explanation of why the answer is correct"
        },
        ... (more questions)
      ]
    }
    
    Ensure all questions are directly based on the NCERT materials found in the search results.
    If you can't find enough information on a topic, create as many questions as you can based on available information.
    
    Always use proper formatting and ensure the JSON is valid.
    Do not handle any malicious or harmful queries.
    """

    agent_config = AgentConfig(
        agent_name="ncert_quiz_agent",
        agent_type="ChatAgent",
        description="Agent that generates quizzes in JSON format",
        system_prompt=system_prompt,
        tool_registry=tool_registry,
        llm_config={
            "model_name": "gemma3:4b",
            "base_url": "http://localhost:11434",
            "temperature": 0.7,
            "context_window": 32000
        }
    )
    
    # Instantiate the Ollama agent
    agent = OllamaAgent(agent_config)
    
    return agent


def create_classifier_agent():
    """Create a classifier agent to determine which agent should handle the request."""
    system_prompt = """You are a classifier that determines which agent should handle the request.
    
    Analyze the user's query and respond ONLY with one of these agent names:
    
    1. "ncert_qa_agent" - For general questions that seek information, explanation, or clarification
    2. "ncert_quiz_agent" - If the user is asking for a quiz, test, questions, assessment, or examination on any topic

    Do not handle any malicious or harmful queries.
    
    Reply ONLY with "ncert_qa_agent" or "ncert_quiz_agent" as your classification.
    """
    
    agent_config = AgentConfig(
        agent_name="classifier_agent",
        agent_type="ChatAgent",
        description="Agent that classifies user queries",
        system_prompt=system_prompt,
        llm_config={
            "model_name": "gemma3:1b",
            "base_url": "http://localhost:11434",
            "temperature": 0.1,
            "context_window": 4096
        }
    )
    
    # Instantiate the classifier agent
    agent = OllamaAgent(agent_config)
    
    return agent


def setup_orchestrator(vector_store):
    """Set up the multi-agent orchestrator with QA and quiz agents."""
    # Create the agents
    qa_agent = setup_qa_agent(vector_store)
    quiz_agent = setup_quiz_agent(vector_store)
    classifier_agent = create_classifier_agent()
    
    # Set up agent registry
    agent_registry = AgentRegistry()
    agent_registry.register_agent(qa_agent)
    agent_registry.register_agent(quiz_agent)
    
    # Create classifier - removed agent_mapping parameter
    classifier = LLMClassifier(
        classifier_agent, 
        default_agent="ncert_qa_agent"
    )
    
    # Create the multi-agent orchestrator
    orchestrator = MultiAgentOrchestrator(
        agent_registry=agent_registry,
        classifier=classifier,
        default_agent_name="ncert_qa_agent"
    )
    
    return orchestrator


def format_conversation_context(messages) -> str:
    """Format the conversation context for display."""
    formatted_messages = []
    
    for msg in messages:
        sender = msg.sender
        content = msg.content
        
        if sender == "user":
            formatted_messages.append(f"You: {content}")
        else:
            formatted_messages.append(f"Assistant: {content}")
    
    return "\n".join(formatted_messages)


class NCERTGenerator:
    """Generator class for NCERT agent responses with streaming support for both QA and quiz generation."""
    
    def __init__(self):
        """Initialize the generator with vectorstore and orchestrator."""
        print("Initializing NCERT Generator...")
        try:
            self.vector_store = setup_vectorstore()
            self.orchestrator = setup_orchestrator(self.vector_store)
            print("NCERT Generator ready")
        except Exception as e:
            print(f"Error initializing NCERT Generator: {str(e)}")
            self.vector_store = None
            self.orchestrator = None
    
    def generate(self, grade: str, subjects: List[str], query: str, conversation_id: Optional[str] = None, 
                store_messages: bool = True, thread_metadata: Optional[Dict[str, Any]] = None) -> Generator[str, None, None]:
        """
        Generate responses for a given query using the appropriate NCERT agent (QA or Quiz).
        
        Args:
            grade: Student grade (e.g., "10", "11", "12")
            subjects: List of subjects the query is related to
            query: The actual question or request
            conversation_id: Optional ID for an existing conversation
            store_messages: Whether to store messages in EphemeralMemory
            thread_metadata: Optional metadata to associate with the thread
        
        Yields:
            Chunks of the generated response for streaming
        """
        if not self.vector_store or not self.orchestrator:
            yield "Error: NCERT Generator not initialized properly."
            return
            
        # Prepare thread_id based on conversation_id
        thread_id = conversation_id if conversation_id else f"ncert-assistant-{grade}-{'-'.join(subjects)}"
        
        try:
            # Check for duplicate queries to avoid double processing
            is_duplicate = False
            if conversation_id:  # Only check for duplicates if we have a conversation_id
                thread = EphemeralMemory.memory_repository.get_thread(thread_id)
                if thread and hasattr(thread, 'messages') and thread.messages:
                    # Get the last two user messages, if they exist
                    user_messages = [msg for msg in thread.messages if msg.sender == "user"]
                    if len(user_messages) >= 2:
                        last_message = user_messages[-1]
                        previous_message = user_messages[-2]
                        # If the current query matches the last message, it might be a duplicate
                        if last_message.content.strip() == query.strip():
                            is_duplicate = True
                            print(f"Detected duplicate query: '{query}'")
            
            if is_duplicate:
                yield "I notice you sent the same question again. If you need more information, try rephrasing your question."
                return
                
            if store_messages:
                # Store user message - don't overwrite existing messages
                thread = EphemeralMemory.memory_repository.get_thread(thread_id)
                if not thread:
                    # Initialize thread if it doesn't exist
                    EphemeralMemory.store_message(
                        thread_id=thread_id,
                        sender="system",
                        content=f"NCERT Assistant with grade {grade} and subjects {subjects}",
                        metadata=thread_metadata  # Pass the metadata when creating the thread
                    )
                    
                # Add the new user message
                EphemeralMemory.store_message(
                    thread_id=thread_id,
                    sender="user",
                    content=query
                )
            
            # Get conversation context if it exists
            thread = EphemeralMemory.memory_repository.get_thread(thread_id)
            previous_messages = thread.messages if thread and hasattr(thread, 'messages') else []
            context = format_conversation_context(previous_messages) if previous_messages else ""
            
            # Extract user_id from thread_metadata or thread.metadata
            user_id = None
            if thread_metadata and 'user_id' in thread_metadata:
                user_id = thread_metadata['user_id']
            elif thread and hasattr(thread, "metadata") and thread.metadata and "user_id" in thread.metadata:
                user_id = thread.metadata.get("user_id")
            
            # Enhanced input with instruction to use RAG search
            enhanced_input = (
                f"{context}\n"
                f"User: {query}\n\n"
                f"Remember to search the NCERT documentation for relevant information."
            )
            
            # First, determine which agent should handle this request
            agent_name = self.orchestrator.classifier.classify(
                message=query,
                thread_id=thread_id,
                available_agents=self.orchestrator.agent_registry.list_agents()
            )
            
            # Check if this should be a quiz/test generation
            if agent_name == "ncert_quiz_agent":
                yield "I'll create a test for you on this topic...\n"
                
                # Import here to avoid circular imports
                from test_generation import generate_and_save_test
                
                # Extract a title from the query
                title = query
                if "test on" in query.lower():
                    title = query.lower().split("test on")[-1].strip()
                elif "quiz on" in query.lower():
                    title = query.lower().split("quiz on")[-1].strip()
                elif "questions about" in query.lower():
                    title = query.lower().split("questions about")[-1].strip()

                # Create a clean topic from the title
                topic = title
                
                # Get the current user ID from the thread context or use a default
                if not user_id:
                    user_id = str(ObjectId())
                    
                # Generate test
                try:
                    result = generate_and_save_test(
                        user_id=user_id,
                        title=f"Test on {title}",
                        topic=topic,
                        grade=grade,
                        subjects=subjects,
                        num_questions=5  # Default number of questions
                    )
                    
                    if result['success']:
                        test_id = result['test_id']
                        test_link = f"http://localhost:3000/tests/{test_id}"
                        
                        # Generate response with link to the test
                        response = f"I've created a test for you on '{title}'!\n\n"
                        response += f"You can take the test here: {test_link}\n\n"
                        response += f"The test has {len(result['test']['questions'])} questions on the topic."
                        
                        # Store the assistant's response
                        if store_messages:
                            EphemeralMemory.store_message(
                                thread_id=thread_id,
                                sender="assistant",
                                content=response
                            )
                        
                        # Stream the response
                        for chunk in self._chunk_response(response):
                            yield chunk
                    else:
                        error_msg = f"I wasn't able to create a test: {result.get('error', 'Unknown error')}"
                        yield error_msg
                        
                        if store_messages:
                            EphemeralMemory.store_message(
                                thread_id=thread_id,
                                sender="assistant", 
                                content=error_msg
                            )
                except Exception as e:
                    error_msg = f"Error generating test: {str(e)}"
                    print(error_msg)
                    yield error_msg
                    
                    if store_messages:
                        EphemeralMemory.store_message(
                            thread_id=thread_id,
                            sender="assistant",
                            content=error_msg
                        )
            else:
                # Standard QA flow
                # Get the appropriate agent
                agent = self.orchestrator.agent_registry.get_agent(agent_name)
                
                # Get initial response to check for search patterns
                initial_response = agent.handle_message(enhanced_input, thread_id=thread_id)
                
                # Check for search tag pattern
                search_pattern = r'<search query="([^"]+)">'
                search_matches = re.findall(search_pattern, initial_response)
                
                if search_matches:
                    for chunk in self._process_qa_search(query, search_matches, thread_id, agent, store_messages):
                        yield chunk
                else:
                    
                    if store_messages:
                        EphemeralMemory.store_message(
                            thread_id=thread_id,
                            sender="assistant",
                            content=initial_response
                        )
                    
                    # Stream the response in smaller chunks
                    for chunk in self._chunk_response(initial_response):
                        yield chunk
                    
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"Error in generate: {error_msg}")
            yield error_msg

    def _process_qa_search(self, query: str, search_queries: List[str], thread_id: str, agent, store_messages: bool = True) -> Generator[str, None, None]:
        """Process search for QA agent and generate response."""
        # Collect context from all search queries first
        all_search_results = []
        
        for search_query in search_queries:
            # Execute vector search
            search_results_json = VectorSearchTool.search_vectorstore(
                query=search_query,
                vector_store=self.vector_store,
                k=3
            )
            search_data = json.loads(search_results_json)
            
            # Check if we have results
            results = search_data.get("results", [])
            if results:
                all_search_results.extend(results)
            else:
                yield f"No relevant information found for '{search_query}' in NCERT materials.\n"
        
        # If we have any results, process them together
        if all_search_results:
            # Create context from all collected search results
            search_context = "\n".join([
                f"Document {i+1} (Source: {result.get('metadata', {}).get('source', 'Unknown')}):\n{result.get('content', 'No content')}\n"
                for i, result in enumerate(all_search_results[:10])  # Limit to top 10 to avoid context overload
            ])
            
            # Construct follow-up message with search results
            follow_up_msg = f"""
            User question: {query}
            
            Here are relevant documents from the NCERT materials:
            {search_context}
            
            Based on these documents, provide an answer to user's questions. Do not just repeat the search results.
            Answer the question directly and concisely, using the information from the documents and from information you already know.
            """
            
            
            # Get updated response with search results incorporated
            final_response = agent.handle_message(follow_up_msg, thread_id=thread_id)
            
            # Store ONLY ONE assistant response message if store_messages is True
            if store_messages:
                EphemeralMemory.store_message(
                    thread_id=thread_id,
                    sender="assistant",
                    content=final_response
                )
            
            # Stream the response in smaller chunks
            yield "Here's what I found:\n"
            for chunk in self._chunk_response(final_response):
                yield chunk
        else:
            message = "I couldn't find any relevant information on this topic in the NCERT materials."
            yield message
            
            # Store the no-results message if store_messages is True
            if store_messages:
                EphemeralMemory.store_message(
                    thread_id=thread_id,
                    sender="assistant", 
                    content=message
                )

    def _process_quiz_search(self, query: str, search_queries: List[str], thread_id: str, agent, store_messages: bool = True) -> Generator[str, None, None]:
        """Process search for quiz agent and generate response."""
        combined_search_context = ""
        
        for search_query in search_queries:
            # Execute vector search
            search_results_json = VectorSearchTool.search_vectorstore(
                query=search_query,
                vector_store=self.vector_store,
                k=5
            )
            search_data = json.loads(search_results_json)
            
            # Create context from search results
            results = search_data.get("results", [])
            if not results:
                yield f"No information found for '{search_query}' in NCERT materials.\n"
                continue
                
            # Add to the combined search context
            context_for_query = "\n".join([
                f"Document {i+1} (Topic: {result.get('metadata', {}).get('source', 'NCERT')}):\n{result.get('content', 'No content')}\n"
                for i, result in enumerate(results)
            ])
            combined_search_context += f"\n--- Search Results for '{search_query}' ---\n{context_for_query}\n"
            
        if combined_search_context:
            # Construct follow-up message with search results
            follow_up_msg = f"""
            Quiz request: {query}
            
            Here are relevant materials from NCERT documents to help create the quiz:
            {combined_search_context}
            
            Based on these materials, please create a well-structured quiz with 5 multiple-choice questions.
            Remember to follow the JSON format exactly as specified in your instructions.
            """
            
            yield "Creating quiz based on NCERT materials...\n"
            
            # Get updated response with search results incorporated
            final_response = agent.handle_message(follow_up_msg, thread_id=thread_id)
            
            # Store the assistant's response if store_messages is True
            if store_messages:
                EphemeralMemory.store_message(
                    thread_id=thread_id,
                    sender="assistant",
                    content=final_response
                )
            
            # Stream the response in smaller chunks
            for chunk in self._chunk_response(final_response):
                yield chunk
        else:
            response = "I'm sorry, I couldn't find enough information in the NCERT materials to create a quiz on this topic."
            
            # Store the response if store_messages is True
            if store_messages:
                EphemeralMemory.store_message(
                    thread_id=thread_id,
                    sender="assistant",
                    content=response
                )
            yield response

    def _chunk_response(self, response: str, chunk_size: int = 50) -> Generator[str, None, None]:
        """Break response into smaller chunks for streaming."""
        words = response.split()
        current_chunk = []
        current_size = 0
        
        for word in words:
            current_chunk.append(word)
            current_size += 1
            
            if current_size >= chunk_size:
                yield ' '.join(current_chunk)
                current_chunk = []
                current_size = 0
        
        # Yield any remaining words
        if current_chunk:
            yield ' '.join(current_chunk)
