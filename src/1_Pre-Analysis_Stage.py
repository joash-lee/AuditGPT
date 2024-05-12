from openai import OpenAI
from prompts import pre_analysis_prompt as prompt0
from prompts import pre_analysis_primer as prompt1
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title(" :one: Audit Prompt Generator")
st.markdown(":male-cook: Welcome to AuditGPT! This is Step 1 we will help you craft a binary or open-ended prompt to suit your needs. Make sure to download the prompt. Then move on to Step 2!")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "user", "content": prompt0}]
    st.session_state.messages.append({"role": "assistant", "content": prompt1})

for idx, msg in enumerate(st.session_state.messages):
    if idx != 0:  # Skip the first message
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

if st.button("End Session to Download Prompt"):
    st.download_button('Download Text Prompt', msg['content'])
    st.session_state.pop("messages", None)