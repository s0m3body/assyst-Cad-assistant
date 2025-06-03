import streamlit as st
from openai import OpenAI
import time

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

ASSISTANT_ID = "asst_BzeO7NF2XnErzF2BLRsuBceB"

st.set_page_config(page_title="Assyst Cad Assistent", page_icon="🤖")
st.title("🤖 Assyst Cad assistant")

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

