# functions used to interact with LLM
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os


def embed_docs(documents, openai_key):
    """
    Transform all the documents into embeddings and save the results locally
    Params:
        documents: a list of Langchain documents
        openai_key: your openai api key
    """

    if not os.path.exists(os.getcwd() + "/llm_faiss_index"):
        docembeddings = FAISS.from_documents(documents, 
                                             OpenAIEmbeddings(openai_api_key=openai_key))
        docembeddings.save_local("llm_faiss_index")

    docembeddings = FAISS.load_local("llm_faiss_index", 
                                     OpenAIEmbeddings(openai_api_key=openai_key))
    
    return docembeddings


def get_answer(query, chain, docembeddings, openai_key):
    """
    Search and augment the query from embeddings and ouput an answer to the query.
    Params:
        query: a string query
        chain: a Langchain chain pipeline
        openai_key: your openai api key
    """
    # set the K-nearest neighbors to be 3 since there might be different
    # intercorrelated files under the repo
    relevant_chunks = docembeddings.similarity_search_with_score(query, k=3)
    chunk_docs = [chunk[0] for chunk in relevant_chunks]
    results = chain({"input_documents": chunk_docs, 
                     "question": query})
    text_reference = set()

    for _, doc in enumerate(results["input_documents"]):
        text_reference.update(doc.metadata['source'])

    text_reference = '\n'.join(text_reference)
    output={"Answer": results["output_text"], "Reference": text_reference}

    return output