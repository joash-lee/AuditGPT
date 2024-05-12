from openai import OpenAI
from prompts import learning_prompt as prompt0
from prompts import learning_primer as prompt1
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

uploaded_file = st.file_uploader("Upload the final audit report file", type=("json"))


st.title(":four: Solidity AI Expert")
st.markdown(":teacher: Welcome to AuditGPT! This is Step 4! The chatbot is trained to handle your audit report and explain the vulnerabilities to you. Feel free to ask it for vulnerabilities, code fixes etc")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "user", "content": prompt0}]
    st.session_state.messages.append({"role": "assistant", "content": prompt1})

if uploaded_file is None:
    st.info("Please upload the smart contract file to continue.")
    st.stop()

for idx, msg in enumerate(st.session_state.messages):
    if idx != 0:  # Skip the first message
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    if "file_appended" not in st.session_state:
        if uploaded_file is not None:
            file_content = uploaded_file.getvalue().decode("utf-8")
            prompt += "\n\n" + file_content
        st.session_state["file_appended"] = True
    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

if st.button("End Session. You have finished an entire Audit :smile:"):
    st.session_state.pop("messages", None)