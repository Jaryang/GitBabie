# GitBabie
Welcome to GitBabie, your AI-powered companion designed to help you effortlessly navigate and understand GitHub repositories like never before. Whether you're diving into a new project, seeking specific details, or simply exploring the vast world of GitHub, GitBabie is here to assist you every step of the way.

GitBabie is built with the goal of making GitHub more accessible and less daunting, especially for those who are unfamiliar with the repositories they are exploring. By engaging in a friendly chat, you can uncover the insights and information hidden within any GitHub repository. From understanding code structure and finding documentation to discovering the most significant contributions and beyond, GitBabie is your go-to guide.

**Key Features:**

- Interactive Exploration: Engage in a conversation with GitBabie to learn about repository contents, structure, and more.

- Smart Insights: Get concise summaries, key highlights, and relevant details about the repo you're interested in.
  
- Ease of Use: Designed for both beginners and experienced developers, GitBabie makes navigating GitHub repositories simpler and more intuitive.

## Instructions:
This project is based on ChatGPT 3.5 turbo using OpenAI API, and incorporates the technique of "Retrival Augmentaion Generation (RAG)" for prompt engineering and augmentaion.

### 1. Data Preprocessing

#### 1.2 Repo Extraction
Corresponding code file: extract_repo.py

This part is used to automatically clone a given Github repository to the local for further analysis. As a foundamental block of the app, a data chaching strategy is applied in this part using the Streamlit decorator "@st.cache_data" to ease the data loading process.

#### 1.3 Repo parsing
Corresponding code file: parse_repo.py

Since each github repository might contain different types of files, it's important to diversify the parsing strategies. This part of code is designed to address this issue by mainly focusing on files that are in text-based format, picture format, PDF format, and notebook format. 

Specifically, the helper function "parse_others" serves to parse files with formats that can be directly read as plain text. "parse_pics" is based off of the "ImageCaptionLoader" from Langchain which utilizes the pre-trained "[Salesforce BLIP image captioning model](https://huggingface.co/Salesforce/blip-image-captioning-base)" to caption relevant images and only the captions will be stored in the corpus. "parse_pdf" uses the pyPDF Loader from Langchain to process the PDF files. "parse_notebooks" employs the NotebookLoader from Langchain to process the notebook file.

"load_files" is created to navigate through the cloned project and parse relevant files, from which each file will be transformed as a langchain Document object that can be chunked.

#### 1.4 Document Embeddings
Corresponding code file: query_utils.py

The selected embedding model is OpenAIEmbedding with FAISS as the similarity searching approach. Resultant embeddings will be stored as a file named "llm_faiss_index".

### 2. LLM Building

#### 2.1 Prompt Initiation & chain building
Corresponding code file: pages/2_chat_with_me.py

Base prompt for the model is devised according to the [COSTAR framework](https://vreamer.medium.com/how-i-revamped-all-my-prompts-using-the-co-star-framework-0e1c19c37108). On top of this, to further address the AI responsibility, some ethical principles are also incorporated into the initial prompt. The "Chain" chosen here is "load_qa_chain" from Langchain.

```
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

    Helpful Answer:
```

#### 2.2 Memory Storage
Corresponding code file: pages/2_chat_with_me.py

To ensure the chatbot is interactive based on chat histories, the "chat elements" from Streamlit are utilized to save the messages in the session state.


### 3. How to run the APP?

#### 3.1 Modules needed for the APP
```
OpenAI
langchain_openai
streamlit
langchain
langchain_community
langchain_text_splitters
git
```

#### 3.2 Virtual Environment
It's recommended to run this app in the virtual environment. For the basic setup of virtual environment, please see: 

[Python Virtual Environments: A Primer](https://realpython.com/python-virtual-environments-a-primer/)

#### 3.3 Project Structure
The APP itself is only directly related to "Hello.py", and the "Pages" file. It's a multipage streamlit app, where the main page is controlled by Hello.py; the login page is controlled by 1_login_page.py; the chatting page is controlled by 2_chat_with_me.py. To run the app in the virtual environment, just do:

```
venv/bin/python -m streamlit run github_repo_chatbot/Hello.py
```

#### 3.4 Start Your Chat
After the running the app, a new window is going to pop out at your browser. Just follow the instruction specified at the cover page and enjoy your chat.

#### 3.5 Demo Pictures

**Welcome page**
<img width="1440" alt="Screen Shot 2024-03-06 at 5 07 10 PM" src="https://github.com/Jaryang/GitBabie/assets/111720298/0d1d8f6a-10db-4244-973d-8ce89b979b54">

**Login page**
![IMG_8742](https://github.com/Jaryang/GitBabie/assets/111720298/7531f162-9adc-4ac6-a454-13913147ff74)

**Chatting page**
<img width="1440" alt="Screen Shot 2024-03-06 at 5 08 09 PM" src="https://github.com/Jaryang/GitBabie/assets/111720298/95b44b10-a20d-4dde-b941-68867f327ca7">

<img width="1440" alt="Screen Shot 2024-03-06 at 5 09 15 PM" src="https://github.com/Jaryang/GitBabie/assets/111720298/99268f29-e74a-46c0-8e32-9d2da8df68b2">




