# testing for chatbot
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains.question_answering import load_qa_chain
from query_utils import get_answer
from extract_repo import get_repo
from parse_repo import load_files
import streamlit as st
import os


# information input
def main():

        # Update session state when inputs are provided
        if ("OPENAI_API_KEY" in st.session_state.keys()) and ("TARGET_GITHUB_REPO" in st.session_state.keys()):
            load_and_initialize()


def load_and_initialize():

    TARGET_GITHUB_REPO = st.session_state["TARGET_GITHUB_REPO"]
    OPENAI_API_KEY = st.session_state["OPENAI_API_KEY"]

    if (TARGET_GITHUB_REPO == None) or (TARGET_GITHUB_REPO == None):
        return "Information is not complete"
    
    # github repo loading
    data_dir = os.getcwd() + '/repo_data'
    data_load_state = st.text('Cloning repo...')
    get_repo(TARGET_GITHUB_REPO, data_dir)
    st.write(data_dir)
    data_load_state.text('Cloning repo...done!')
    
    #### LLM budilding ####
    # 1. prompt initiation
    prompt_template = """
    You are a helpful assistant that serves the users to understand and navigate through
    a github repository. Your task is to answer their question based on your knowledge and 
    relevant context that is given to you. Your style should be like an actual human
    assistant, with a relaxing, colloquial but professional tone . Your audience are people
    who are unfamiliar with the repo. However, If you don't know the answer, just say that 
    you don't know, don't try to make up an answer. On top of that, you should ensure that your
    response complies with the AI responsibility principles that are given.

    Context: {context}
    ---------
    AI responsibility principles: You are committed to operating within ethical guidelines 
    and respecting user privacy and data security. Don't include the principles in your
    response.
    ---------
    Question: {question}

    Helpful Answer:"""

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    # 2. load embeddings
    data_load_state_2 = st.text('Loading data...')
    docembeddings = load_files(data_dir, OPENAI_API_KEY)
    data_load_state_2.text('Loading data...done!')

    # 3. model building
    conversation = load_qa_chain(
        llm=OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY),
        prompt=PROMPT,
        verbose=True
        )
    
    # 4. Handle the memory
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        response = get_answer(prompt, conversation, docembeddings, OPENAI_API_KEY)
        answer = response["Answer"]
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": response["Answer"]})


if __name__ == "__main__":
    main()