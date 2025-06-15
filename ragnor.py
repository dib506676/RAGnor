import streamlit as st
from PyPDF2 import PdfReader

# importing tempfile for fake path of pdf
import tempfile
import json

# pdf loader by langchain -----> convert pdf into text
from langchain_community.document_loaders import PyPDFLoader

# importing openAi for chat
from openai import OpenAI

from langchain_text_splitters import RecursiveCharacterTextSplitter
import google.generativeai as genai

from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import os

st.set_page_config(page_title="RAGnor", layout="wide")

def get_text_chunks(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    # chunking
    chunks = text_splitter.split_documents(documents=docs)
    return chunks


def get_vector_store(text_chunks, api_key):
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=api_key
    )
    vector_store = FAISS.from_documents(text_chunks, embedding=embeddings)
    vector_store.save_local("RAGnor")

def get_conversation_with_llm(api_key):
    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    return client

def user_input(user_question, api_key):
    #creating vector embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=api_key
    )

    #storing the vector embdding locally with collection name RAGnor
    new_db = FAISS.load_local(
        "RAGnor", embeddings, allow_dangerous_deserialization=True
    )

    search_result = new_db.similarity_search(user_question)
    context = "\n\n\n".join(
        [
            f"page content : {result.page_content}\n page number : {result.metadata.get('page_label', 'N/A')}"
            for result in search_result
        ]
    )
    client = get_conversation_with_llm(api_key)
    SYSTEM_PROMPT = f"""You are a helpfull AI Assistant who asnweres user query based on the available context retrieved from a PDF file along with page_contents and page number.
    You have to evaluate more ans answer simple english and easy to understand by user.

    Context:
        {context}
    """
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_question},
        ],
    )
    reply = response.choices[0].message.content
    return reply

st.markdown(
    """
    <div style="display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px;">
        <span style="font-size: 58px; font-weight: bold;">RAGnor</span>
        <span style="font-size: 20px; color: gray;">Get instant insight from your document</span>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("""
#### Follow these simple steps to get input :
1. **Enter your API Key** : obtain api_key from https://markersuite.google.com/app/apikey.            
2. **Upload Your Document** : open sidebar and upload pdf (the system accept single pdf at once).
3. **Ask a Question** : ask any question related to the content of your uploaded document.
""")
api_key = st.text_input(
    "enter your google api key : ", type="password", key="api_key_input"
)

user_question = st.text_input("ask a question from pdf file", key="user_question")

if user_question and api_key:
    reply = user_input(user_question, api_key)
    reply_dict = json.loads(reply)
    st.write(f"Ai reply : {reply_dict['answer']}")
    page_number = reply_dict.get('page_number')
    if page_number:
        st.write(f"For more context go to page no. {page_number} of given PDF")
    else:
        st.write("Page number information is not available.")

with st.sidebar:
    st.title("menu : ")
    file = st.file_uploader(
        "upload you docs",
        type="pdf",
    )
    if st.button("upload", key="upload_button") and api_key:
        with st.spinner("processing..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(file.getvalue())
                tmp_file_path = tmp_file.name
            loader = PyPDFLoader(tmp_file_path)
            docs = loader.load()
            text_chunks = get_text_chunks(docs)
            get_vector_store(text_chunks, api_key)
            st.success("upload successfull !")
