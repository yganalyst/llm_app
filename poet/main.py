# from dotenv import load_dotenv
# load_dotenv()
from langchain.chat_models import ChatOpenAI
import streamlit as st

chat_model = ChatOpenAI()

st.title('인공지능 시인')

title = st.text_input('시의 주제를 제시해주세요.')

if st.button('요청하기'):
    with st.spinner('시를 작성 중입니다...'):
        result = chat_model.predict(title + "에 대한 시를 작성해줘")
        st.write(result)