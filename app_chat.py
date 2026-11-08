import streamlit as st
from openai import OpenAI

# 1. Configuración visual de la página web
st.set_page_config(page_title="Mi Primer Agente Web", page_icon="🤖")
st.title("🤖 Chatbot con Memoria DON RODO (Groq)")

# 2. Inicializamos el cliente (Recuerda poner tu API Key)
client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"], 
    base_url="https://api.groq.com/openai/v1"
)

# 3. LA BÓVEDA DE MEMORIA: Verificamos si ya existe un historial
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {"role": "system", "content": "Eres un asistente útil y amigable. Si el usuario dice su nombre, recuérdalo."}
    ]

# 4. DIBUJAR EL CHAT: Mostramos los mensajes guardados en la memoria
for msg in st.session_state.mensajes:
    if msg["role"] != "system": # Ocultamos las instrucciones secretas al usuario
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# 5. CAJA DE TEXTO: Donde el usuario escribe
texto_usuario = st.chat_input("Escribe tu mensaje aquí...")

if texto_usuario:
    # A) Dibujamos el mensaje del usuario en la pantalla y lo guardamos
    with st.chat_message("user"):
        st.write(texto_usuario)
    st.session_state.mensajes.append({"role": "user", "content": texto_usuario})
    
    # B) Llamamos al Agente mostrando un indicador de "pensando"
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            respuesta = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=st.session_state.mensajes,
                temperature=0.7
            )
            texto_ia = respuesta.choices[0].message.content
            
            # Dibujamos la respuesta
            st.write(texto_ia)
            
    # C) Guardamos la respuesta en la memoria
    st.session_state.mensajes.append({"role": "assistant", "content": texto_ia})