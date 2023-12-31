# from dotenv import load_dotenv
# load_dotenv()
# from langchain.llms import CTransformers
from langchain.chat_models import ChatOpenAI
import streamlit as st

chat_model = ChatOpenAI(max_tokens=200)
## Offline model: LLaMA
# chat_model = CTransformers(
#     model="llama-7b.ggmlv3.q2_K.bin",
#     model_type="llama"
# )

st.title("Yg's 인공지능 시인")

content = st.text_input('시의 주제를 제시해주세요.')

if st.button('요청하기'):
    with st.spinner('시를 작성 중입니다...'):
        result = chat_model.predict(content + "에 대한 시를 작성해줘")
        # result = chat_model.predict("write a poem about "+ content + ": ")
        st.write(result)