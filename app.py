import streamlit as st
from openai import OpenAI
import time

title="Assystente"
st.set_page_config(page_title=title, page_icon="duck.png")
col1, col2 = st.columns([1, 8])
with col1:
    st.image("duck.png", width=50)
with col2:
    st.markdown(title)

def login():
    st.sidebar.title("Guru Login")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if password == st.secrets["password"]:
            st.session_state["authenticated"] = True
        else:
            st.sidebar.error("Invalid credentials!")

if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    login()
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

ASSISTANT_ID = "asst_BzeO7NF2XnErzF2BLRsuBceB"

if "thread_id" not in st.session_state:
    # Erstellt einen neuen Thread
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

if prompt := st.chat_input("Wie kann ich helfen?"):
    # Nachricht an Thread anhängen
    client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=prompt,
    )

    # Ausführung starten
    run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=ASSISTANT_ID,
    )

    # Warten, bis die Ausführung abgeschlossen ist
    with st.spinner("Ich denke..."):
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id,
            )
            if run_status.status == "completed":
                break
            elif run_status.status in ["failed", "expired"]:
                st.error("Assistant failed to respond.")
                st.stop()
            time.sleep(1)

    # Antworten anzeigen
    messages = client.beta.threads.messages.list(
        thread_id=st.session_state.thread_id
    )

    for msg in reversed(messages.data):
        role = msg.role
        content = msg.content[0].text.value
        with st.chat_message(role):
            st.markdown(content)

