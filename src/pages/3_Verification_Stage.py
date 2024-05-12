from openai import OpenAI
from prompts import adversarial_prompt as prompt0
from prompts import adversarial_primer as prompt1
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

uploaded_file = st.file_uploader("Upload the audit report file in JSON", type=("json"))


st.title(":three: Checking and Scoring Vulnerabilities")
st.markdown(":judge: Welcome to AuditGPT! This is Step 3, upload your audit report. The critique will double check the vulnerabilities and score them. You may give feedback on scoring before finalising the results")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "user", "content": prompt0}]
    #st.session_state.messages.append({"role": "assistant", "content": prompt1})

if uploaded_file is None:
    st.info("Please upload the audit report to continue.")
    st.stop()

for idx, msg in enumerate(st.session_state.messages):
    if idx != 0:  # Skip the first message
        st.chat_message(msg["role"]).write(msg["content"])

if st.button("Generate"):
    client = OpenAI(api_key=openai_api_key)
    file_input = uploaded_file.getvalue().decode("utf-8")
    st.session_state.messages.append({"role": "user", "content": file_input})
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    st.session_state["generation_complete"] = True

if st.session_state.get("generation_complete", False):
    if prompt := st.chat_input():
        client = OpenAI(api_key=openai_api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

if st.button("End Session to Download Final Vulnerability Report"):
    st.download_button(
        label='Click to download',
        data=msg['content'],
        file_name='data.json',
        mime='application/json'
    )
    st.session_state.pop("messages", None)