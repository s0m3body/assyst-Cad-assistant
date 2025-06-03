import streamlit as st
import openai
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Assyst Cad assistant", page_icon="🤖")
st.title("🤖 Assyst Cad assistant")

ASSISTANT_ID = "asst_BzeO7NF2XnErzF2BLRsuBceB"

if "thread_id" not in st.session_state:
    # Erstellt einen neuen Thread
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

if prompt := st.chat_input("Wie kann ich dir helfen?"):
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
    with st.spinner("Assistant denkt..."):
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id,
            )
            if run_status.status == "completed":
                break
            time.sleep(1)

    # Antworten anzeigen
    messages = client.beta.threads.messages.list(
        thread_id=st.session_state.thread_id
    )

    for msg in reversed(messages.data):
        if msg.role == "assistant":
            with st.chat_message("assistant"):
                st.markdown(msg.content[0].text.value)
        elif msg.role == "user":
            with st.chat_message("user"):
                st.markdown(msg.content[0].text.value)
