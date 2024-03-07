from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferWindowMemory
from query_utils import get_answer
from extract_repo import get_repo
from parse_repo import load_files
import streamlit as st
import os


st.set_page_config(
    page_title="Hello there,",
    page_icon="👋",
)

st.write("# Welcome to GitBabie! 👋")

st.sidebar.success("Please select above.")

st.markdown(
    """
    Welcome to GitBabie, your AI-powered companion designed to help you effortlessly 
    navigate and understand GitHub repositories like never before. 
    Whether you're diving into a new project, seeking specific details, or simply 
    exploring the vast world of GitHub, GitBabie is here to assist you every step of the way.

    ### 👈 Please follow the instruction below to use the app:
    #### 1. Login in
    Before starting the chat, you need to type in your OpenAI API Key and interested
    Github repo link in the **login page**. Don't worry, GitBabie complies with the
    user privacy rules and will not share your information to a third party. Besides,
    GitBabie will clear your data when you finish the chat.
    #### 2. Start to chat
    When you finish typing in your credentials, just press the "enter" key on your
    keyboard. Then, go to the **chat with me** page and start your chat 🤳
"""
)