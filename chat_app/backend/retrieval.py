import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.retrievers import BaseRetriever
from typing import List, Any
from langchain_core.documents import Document
from pydantic import Field

from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings

import faiss
from langchain_community.vectorstores import FAISS

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "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" # Replace with your API Key


class ContextExpandedFilteredRetriever(BaseRetriever):
    """Retriever that fetches top result plus surrounding context chunks with filtering."""
    
    # Explicitly define fields using Pydantic Field
    vectorstore: Any = Field(description="Vector store for retrievals")
    grade: str = Field(description="Grade level for filtering")
    subjects: List[str] = Field(description="List of subject codes for filtering")
    context_window: int = Field(default=5, description="Number of context chunks to retrieve")
    
    def _get_relevant_documents(self, query: str) -> List[Document]:
        # Create a filter for grade and subjects
        filter_dict = {
            "$and": [
                {"grade": self.grade},
                {"subject_code": {"$in": self.subjects}}
            ]
        }
        
        # Get the top result with filters
        results = self.vectorstore.similarity_search(
            query, 
            k=1,
            filter=filter_dict
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
                    {"grade": self.grade},
                    {"subject_code": subject_code},
                    {"chapter_code": chapter_code},
                    {"split_number": i}
                ]
            }
            
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
                    {"grade": self.grade},
                    {"subject_code": subject_code},
                    {"chapter_code": chapter_code},
                    {"split_number": i}
                ]
            }
            
            context_docs = self.vectorstore.similarity_search(
                "", # Empty query to avoid biasing results
                k=1,
                filter=split_filter
            )
            
            if context_docs:
                expanded_results.append(context_docs[0])  # Add after top result
        
        return expanded_results

class Generator:
    def __init__(self):
        self.llm = ChatOllama(model="llama3.1", temperature=0)
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.vector_store = FAISS.load_local("faiss-index", self.embeddings, allow_dangerous_deserialization=True)
        self.template = """Answer the question based only on the following context and expand upon it. If it is a question you otherwise know the answer to, answer it in your way.:
                    {context}
                    Question: {question}
                    """

    def generate(self, grade, subjects, query):
        """Generate a response based on the input query."""
        print("Generating response for query:", grade, subjects, query)
        retriever = ContextExpandedFilteredRetriever(
            vectorstore=self.vector_store,  # Your vector store instance
            grade=grade,
            subjects=subjects,
            context_window=5  # Retrieve 5 chunks before and after
        )

        # Create the prompt template
        prompt = ChatPromptTemplate.from_template(self.template)

        # Build the chain
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

        for chunk in chain.stream(query):
            yield chunk

if __name__ == "__main__":
    # Required initialization code
    agent = Generator()

    # TC1
    print("Test case 1")
    grade = "11"
    subjects = ["bio", "chem", "phy", "math"]
    query = "What is differentiation"

    for chunk in agent.generate(grade, subjects, query):
        print(chunk, end="", flush=True)
    print("\n")

    # TC2
    print("Test case 2")
    grade = "11"
    subjects = ["chem", "phy", "math", "comp"]
    query = "What is differentiation"

    for chunk in agent.generate(grade, subjects, query):
        print(chunk, end="", flush=True)
    print("\n")

    # TC3
    print("Test case 3")
    grade = "10"
    subjects = ["english", "english2", "history", "math"]
    query = "What did Lencho ask God"

    for chunk in agent.generate(grade, subjects, query):
        print(chunk, end="", flush=True)
    print("\n")
