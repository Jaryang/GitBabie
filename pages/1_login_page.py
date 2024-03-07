import streamlit as st

if "OPENAI_API_KEY" not in st.session_state or "TARGET_GITHUB_REPO" not in st.session_state:
        # Display inputs for API key and repo link
        OPENAI_API_KEY = st.text_input("Your OpenAI API Key:")
        TARGET_GITHUB_REPO = st.text_input("Target Github Repo Link:")

        # Update session state when inputs are provided
        if OPENAI_API_KEY and TARGET_GITHUB_REPO:
            st.session_state["OPENAI_API_KEY"] = OPENAI_API_KEY
            st.session_state["TARGET_GITHUB_REPO"] = TARGET_GITHUB_REPO