import streamlit as st
from openai import OpenAI
import time
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode()
        return f"data:image/png;base64,{b64_string}"

# Prepare
duck_base64 = get_base64_image("duck.png")

title="Assystente"
st.set_page_config(page_title=title, page_icon="duck.png")
st.markdown(f"""
    <div style="display: flex; align-items: center;">
        <img src="{duck_base64}" width="120" style="margin-right: 15px;">
        <h1 style="font-size: 48px; margin: 0;">{title}</h1>
    </div>
""", unsafe_allow_html=True)

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

