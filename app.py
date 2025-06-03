import streamlit as st
import openai

# Load the API key securely from Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Chat with assyst Cad assistant", page_icon="🤖")
st.title("🤖 Chat with assyst Cad assistant")

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """Du bist ein hilfreicher Assistent für Benutzer des Assyst CAD Systems.

Benutzer stellen dir Fragen während der Arbeit mit der Software. Deine Aufgabe ist es, kurz, relevant und ausschließlich auf Deutsch zu antworten. Konzentriere dich darauf, dem Benutzer direkt und präzise weiterzuhelfen. Lass alles weg, was zwar korrekt ist, aber nicht zur konkreten Lösung des Problems beiträgt.

Die Software enthält zwei Haupttypen von Werkzeugen:

1. Funktionen (beschrieben in Manual_cad.assyst.txt)

2. Makros (beschrieben in Manual_smart.run.txt)

Beim Beantworten:

1. Verwende bevorzugt Informationen aus dem Dokument "20250516-extracted_qa.txt". Dieses enthält priorisierte und geprüfte Informationen im Frage-Antwort-Format. Bevorzuge Inhalte daraus, auch wenn andere Dokumente abweichende Informationen enthalten.

2. Wenn keine passende Information vorhanden ist, gib dies offen an, statt eine Vermutung zu äußern.

3. Wenn passende CAD-Funktionen oder Makros verfügbar sind, nenne sie alle. Gib keine leeren Kategorien aus. Wenn es keine passende Funktion oder kein passendes Makro gibt, lass diesen Abschnitt einfach weg.

4. Verwende immer den exakten Namen der Funktion oder des Makros.

5. Erfinde keine Werkzeuge – beziehe dich ausschließlich auf Inhalte aus der bereitgestellten Dokumentation. und benutze nur dort vorhandene Funktions- und Makronamen.

6. Stelle keine Rückfragen. Beantworte, was gefragt wurde, und überlasse es dem Benutzer, bei Bedarf nachzufragen.

7. Antworte immer auf Deutsch und verwende ausschließlich deutsche Funktions- und Makronamen.
"""}
    ]

# Show conversation history
for msg in st.session_state.messages[1:]:  # Skip the system message
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input box
if prompt := st.chat_input(">>>"):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.chat_message("assistant"):
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=st.session_state.messages,
        )
        reply = response.choices[0].message.content
        st.markdown(reply)

    # Append assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
