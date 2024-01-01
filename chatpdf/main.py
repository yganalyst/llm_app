from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import streamlit as st
import os, tempfile


# 제목
st.title("Chat PDF")
st.write("---")

# 파일 업로드
uploaded_file = st.file_uploader("Choose a file")
st.write("---")

def pdf_to_document(uploaded_file):
    temp_dir = tempfile.TemporaryDirectory()
    temp_filepath = os.path.join(temp_dir.name, uploaded_file.name)
    with open(temp_filepath, "wb") as f:
        f.write(uploaded_file.getvalue())
    loader = PyPDFLoader(temp_filepath)
    pages = loader.load_and_split()
    return pages

# 업로드 후 동작
if uploaded_file is not None:
    pages = pdf_to_document(uploaded_file)

    ## Spliter
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=100,
        chunk_overlap=30,
        length_function=len,
        is_separator_regex=False,
    )
    texts = text_splitter.split_documents(pages)

    ## Embedding
    embeddings_model = OpenAIEmbeddings()

    ## load it into ChromaDB
    db = Chroma.from_documents(texts, embeddings_model)

    ## Create Query
    st.header("PDF에게 질문해보세요!")
    question = st.text_input("질문을 입력하세요")

    if st.button('질문하기'):
        with st.spinner('답변을 생성 중입니다...'):
            llm = ChatOpenAI(
                temperature=0,
                # max_tokens=300    
            )
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm, 
                retriever=db.as_retriever()
            )
            result = qa_chain({"query":question})
            st.write(result["result"])