import streamlit as st
from openai import OpenAI
import time
import base64

_dollar_pattern = re.compile(r'(?<!\\)\$')

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode()
        return f"data:image/png;base64,{b64_string}"

# common
title="Assystente"
duck_base64 = get_base64_image("duck.png")
st.set_page_config(page_title=title, page_icon="duck.png")

def login_page():
    with st.form("login_form"):
        st.markdown("""
            <style>
                div[data-testid="stForm"] {
                    max-width: none !important;
                    width: fit-content !important;
                    margin: auto;
                }
                div[data-testid="stForm"] h1 {
                    white-space: nowrap;
                }
                div[data-testid="stForm"] div {
                    white-space: nowrap;
                }
            </style>
        """, unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>Die KI wird den Menschen nicht ersetzen.</h1>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: right;margin-bottom: 10%;'><b>...sie wird jene ersetzen, die sich weigern, sie zu nutzen...</b></div>", unsafe_allow_html=True)
        password = st.text_input("Guru Kennwort:", type="password")
        submitted = st.form_submit_button("Ich bin's")
        if submitted:
            if password == st.secrets["password"]:
                st.session_state["authenticated"] = True
                st.rerun()  # restart app with new state
            else:
                st.error("Invalid credentials!")


def assystente_app():
    st.markdown(f"""
        <div style="display: flex; align-items: center;">
            <img src="{duck_base64}" width="120" style="margin-right: 15px;">
            <h1 style="font-size: 48px; margin: 0;">{title}</h1>
        </div>
    """, unsafe_allow_html=True)

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    #ASSISTANT_ID = "asst_BzeO7NF2XnErzF2BLRsuBceB" # 20250527
    #ASSISTANT_ID = "asst_eYS26BK1AXnbRTOECdN1Bvax" # 20250619
    #ASSISTANT_ID = "asst_eYS26BK1AXnbRTOECdN1Bvax" # 20250619
    ASSISTANT_ID = "asst_p7YLYouRF69uaeNyaa5drVaP" # 20250711

    if "thread_id" not in st.session_state:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id

    if prompt := st.chat_input("Wie kann ich helfen?"):
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt,
        )

        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=ASSISTANT_ID,
        )

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

        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        for msg in reversed(messages.data):
            role = msg.role
            content = msg.content[0].text.value
            with st.chat_message(role):
                st.text(content)


# main control
if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    login_page()
else:
    assystente_app()
