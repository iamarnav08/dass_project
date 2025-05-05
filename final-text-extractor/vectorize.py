import os
import re
import glob
import json
from typing import List
import pandas as pd

from langchain_ollama import OllamaEmbeddings

import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_core.documents import Document

def process_markdown_file(filepath: str, textbooks_df, special_chapters_df) -> List[Document]:

    # Get folder name from file path
    folder_name = os.path.basename(os.path.dirname(filepath))
    
    # Parse folder name to extract subject code, grade, and chapter code
    parts = folder_name.split('_')
    
    if len(parts) < 3:
        print(f"Warning: Folder name '{folder_name}' doesn't match expected format.")
        parsed_info = None
    
    subject_code = parts[0]
    grade = parts[1]
    chapter_code = '_'.join(parts[2:]) if len(parts) > 3 else parts[2]

    parsed_info = {
        "grade": grade,
        "subject_code": subject_code,
        "chapter_code": chapter_code
    }

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
    # Check if this is a special chapter
    chapter_title = chapter_code
    
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
            chapter_title = f"{chapter_type} {number}"
    
    # If it's just a number or didn't match any special chapter
    if chapter_code.isdigit():
        chapter_title = f"chapter {chapter_code}"
    
    # Load the markdown file
    loader = TextLoader(filepath)
    documents = loader.load()

    meta_filepath = os.path.join(os.path.dirname(filepath), os.path.basename(filepath).replace('.md', '_meta.json'))
    section_titles = []

    if os.path.exists(meta_filepath):
        with open(meta_filepath, 'r') as f:
            metadata = json.load(f)

            for section in metadata.get('table_of_contents', []):
                title = section.get('title', '')
                section_titles.append(title)

    headers_to_split_on = [("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3"), ("####", "Header 4")]

    text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)
    chunks = text_splitter.split_text(documents[0].page_content)
    print(len(chunks), len(section_titles))
    
    # Add metadata to each chunk
    for i, chunk in enumerate(chunks):
        section_title = section_titles[i] if i < len(section_titles) else ""

        chunk.metadata.update({
            "grade": grade,
            "subject_code": subject_code,
            "chapter_code": chapter_code,
            "subject_name": subject_name,
            "textbook_name": textbook_name,
            "chapter_title": chapter_title,
            "section_title": section_title,
            "split_number": i + 1,
            "total_splits": len(chunks),
            "source": filepath
        })
    
    if len(chunks) != len(section_titles):
        print(f"Warning: Number of chunks ({len(chunks)}) doesn't match number of section titles ({len(section_titles)}) for {filepath}")

    return chunks

if __name__ == "__main__":
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))
    vector_store = FAISS(embedding_function=embeddings, index=index, docstore=InMemoryDocstore(), index_to_docstore_id={})
    
    textbooks_df = pd.read_csv("textbooks.csv")
    special_chapters_df = pd.read_csv("special_chapters.csv")

    markdown_files = glob.glob(os.path.join("../extracted_text", "**/*.md"), recursive=True)
    print(f"Found {len(markdown_files)} markdown files to process")
    i = 0
    for file_path in markdown_files:
            print(f"Processing file: {file_path}")
            try:
                chunks = process_markdown_file(file_path, textbooks_df, special_chapters_df)
                vector_store.add_documents(chunks)
                vector_store.save_local("faiss-index")
                print(f"Successfully processed {file_path}, File: {i}")
                i += 1
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                with open("errors.txt", "a") as f:
                    f.write(f"Error processing {file_path}: {str(e)}\n")
        
    print("Finished processing all markdown files")
