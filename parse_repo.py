# load and parse relevant files
import os
from langchain_community.document_loaders import ImageCaptionLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import NotebookLoader
from params import TEXT_FORMATS, PICTURE_FORMATS
from langchain_text_splitters import RecursiveCharacterTextSplitter
import streamlit as st
from query_utils import embed_docs


def parse_others(path):
    """Used to parse all the text-based files that are not specified in the code"""

    with open(path, 'r') as code_file:
        codes = code_file.read()
    
    return [codes]


def parse_pics(path):
    """Used to parse pictures as corresponding captions"""

    loader = ImageCaptionLoader(images=[path])
    data = loader.load()

    return [data[0].page_content]


def parse_pdf(path):
    """Used to parse pdf files"""

    loader = PyPDFLoader(path, extract_images=True)
    data = loader.load()
    pdf_text = ""
    
    for doc in data:
        pdf_text += doc.page_content
    
    return [pdf_text]


def parse_notebook(path):
    """Used to parse notebook files"""

    loader = NotebookLoader(
        path,
        include_outputs=True,
        max_output_length=20,
        remove_newline=True,
    )
    data = loader.load()

    return [data[0].page_content]


def organize_files_by_directory(repo_path):
    """Generate a dictionary depicting the structure of the given repo"""

    organized_files = {"other_files": []}
    
    for root, dirs, files in os.walk(repo_path):

        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, repo_path)

            if root == repo_path:
                # File is in the root directory, add to 'other_files'
                organized_files["other_files"].append(file_path)

            else:
                # File is in a subdirectory, organize by directory
                subdir_name = os.path.relpath(root, repo_path)
                # Handle nested directories by considering only the first level
                subdir_name = subdir_name.split(os.sep)[0]
                if subdir_name not in organized_files:
                    organized_files[subdir_name] = []
                organized_files[subdir_name].append(file_path)
    

    return organized_files


@st.cache_resource
def load_files(root_path, openai_key):
    """Used to iterate through the repos to load files together"""
    
    repo_structure = organize_files_by_directory(root_path)
    docs = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len
    )
    
    for dir, files in repo_structure.items():

        for file in files:

            if file.endswith(tuple(PICTURE_FORMATS)):
                # load picture files
                text = parse_pics(file)
                if len(text) == 0:
                    continue
                text = text_splitter.create_documents(texts=text,
                                                      metadatas=[{'source': file}])
                docs.extend(text)
            
            elif file.endswith(".pdf"):
                # load pdf files
                text = parse_pdf(file)
                if len(text) == 0:
                    continue
                text = text_splitter.create_documents(texts=text,
                                                      metadatas=[{'source': file}])
                docs.extend(text)
            
            elif file.endswith(".ipynb"):
                # load notebook files
                text = parse_notebook(file)
                if len(text) == 0:
                    continue
                text = text_splitter.create_documents(texts=text,
                                                      metadatas=[{'source': file}])
                docs.extend(text)
            
            elif file.endswith(tuple(TEXT_FORMATS)):
                text = parse_others(file)
                if len(text) == 0:
                    continue
                text = text_splitter.create_documents(texts=text,
                                                      metadatas=[{'source': file}])
                docs.extend(text)


    return embed_docs(docs, openai_key)
