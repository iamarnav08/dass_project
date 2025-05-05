import os
import re
import glob
import gc
from typing import List, Dict, Any
import pandas as pd

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "YOUR_API_KEY" # Replace with your API Key

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

embeddings = OllamaEmbeddings(model="llama3.1")
vector_store = Chroma(embedding_function=embeddings, persist_directory="./chroma_db")

# Load CSV files
def load_csv_data():
    textbooks_df = pd.read_csv("textbooks.csv")
    special_chapters_df = pd.read_csv("special_chapters.csv")
    return textbooks_df, special_chapters_df

# Extract information from folder name - CORRECTED FORMAT
def parse_folder_name(folder_name: str) -> Dict[str, Any]:
    parts = folder_name.split('_')
    
    if len(parts) < 3:
        print(f"Warning: Folder name '{folder_name}' doesn't match expected format.")
        return None
    
    # CORRECTED ORDER: {subjectcode}_{grade}_{chapterno}
    subject_code = parts[0]
    grade = parts[1]
    
    # Extract chapter number - may contain letters for special chapters
    chapter_code = '_'.join(parts[2:]) if len(parts) > 3 else parts[2]
    
    return {
        "grade": grade,
        "subject_code": subject_code,
        "chapter_code": chapter_code
    }

# Format chapter title based on special chapter code
def format_chapter_title(chapter_code: str, special_chapters_df, grade: str, subject_code: str) -> str:
    # Check if this is a special chapter
    match = re.match(r'([a-zA-Z]+)(\d+)', chapter_code)
    
    if match:
        letter_code = match.group(1)
        number = match.group(2)
        
        # Look up special chapter in dataframe
        special_chapter = special_chapters_df[
            (special_chapters_df['grade'] == int(grade)) & 
            (special_chapters_df['subjectcode'] == subject_code) & 
            (special_chapters_df['special_chaptercode'] == letter_code)
        ]
        
        if not special_chapter.empty:
            chapter_type = special_chapter['chaptertype'].iloc[0]
            return f"{chapter_type} {number}"
    
    # If it's just a number or didn't match any special chapter
    if chapter_code.isdigit():
        return f"Chapter {chapter_code}"
    
    # Default case: return as is
    return chapter_code

# Process a single markdown file
def process_markdown_file(filepath: str, textbooks_df, special_chapters_df) -> List[Document]:
    # Get folder name from file path
    folder_name = os.path.basename(os.path.dirname(filepath))
    
    # Parse folder name to extract subject code, grade, and chapter code
    parsed_info = parse_folder_name(folder_name)
    if not parsed_info:
        return []
    
    grade = parsed_info["grade"]
    subject_code = parsed_info["subject_code"]
    chapter_code = parsed_info["chapter_code"]
    
    # Look up subject name and textbook
    subject_info = textbooks_df[
        (textbooks_df['grade'] == int(grade)) & 
        (textbooks_df['subjectcode'] == subject_code)
    ]
    
    if subject_info.empty:
        print(f"Warning: No subject info found for grade {grade}, subject code {subject_code}")
        subject_name = subject_code
        textbook_name = "Unknown"
    else:
        subject_name = subject_info['subjectname'].iloc[0]
        textbook_name = subject_info['textbook'].iloc[0]
    
    # Format chapter title
    chapter_title = format_chapter_title(chapter_code, special_chapters_df, grade, subject_code)
    
    # Load the markdown file
    loader = UnstructuredMarkdownLoader(filepath)
    documents = loader.load()
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    chunks = text_splitter.split_documents(documents)
    
    # Add metadata to each chunk
    for i, chunk in enumerate(chunks):
        chunk.metadata.update({
            "grade": grade,
            "subject_code": subject_code,
            "chapter_code": chapter_code,
            "subject_name": subject_name,
            "textbook_name": textbook_name,
            "chapter_title": chapter_title,
            "split_number": i + 1,
            "total_splits": len(chunks),
            "source": filepath
        })
    
    # Clean up variables that are no longer needed
    del documents
    gc.collect()
    
    return chunks

# Process markdown files in batches
def process_files_in_batches(file_paths, batch_size, textbooks_df, special_chapters_df):
    all_documents = []
    total_documents_count = 0
    
    for i in range(0, len(file_paths), batch_size):
        batch = file_paths[i:i + batch_size]
        batch_documents = []
        
        print(f"Processing batch {i//batch_size + 1}/{(len(file_paths) + batch_size - 1)//batch_size}")
        
        for file_path in batch:
            chunks = process_markdown_file(file_path, textbooks_df, special_chapters_df)
            batch_documents.extend(chunks)
            print(f"Processed {file_path}: {len(chunks)} chunks")
        
        # Store this batch in the vector database
        if batch_documents:
            vector_store.add_documents(batch_documents)
            print(f"Batch {i//batch_size + 1} with {len(batch_documents)} chunks stored in database")
            total_documents_count += len(batch_documents)
        
        # Clear batch from memory
        del batch_documents
        gc.collect()
        
    return total_documents_count

# Main function to process all markdown files
def process_all_markdown_files(base_dir: str, batch_size=50) -> int:
    textbooks_df, special_chapters_df = load_csv_data()
    
    # Find all markdown files in the specified directory and subdirectories
    pattern = os.path.join(base_dir, "**", "*.md")
    markdown_files = glob.glob(pattern, recursive=True)
    
    print(f"Found {len(markdown_files)} markdown files to process.")
    
    # Process files in batches
    total_documents = process_files_in_batches(
        markdown_files, batch_size, textbooks_df, special_chapters_df
    )
    
    # Clean up after processing all files
    del textbooks_df, special_chapters_df
    gc.collect()
    
    return total_documents

if __name__ == "__main__":
    # Set the base directory where your folders are located
    base_directory = "../marker-output"  # Change this to your actual directory
    batch_size = 50  # Adjust based on your memory constraints
    
    # Process all markdown files and get document chunks with metadata
    total_chunks = process_all_markdown_files(base_directory, batch_size)
    
    print(f"Total document chunks processed and stored: {total_chunks}")
    
    # Final cleanup
    gc.collect()
