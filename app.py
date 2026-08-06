import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Maestro Formulador", page_icon="🧪")

st.title("🧪 Maestro de Formulaciones Químicas")
st.caption("Aprende la ciencia de coloides e interfases con sensibilidad y maestría.")

# Obtener clave desde Secrets o Sidebar
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    api_key = st.sidebar.text_input("Ingresa tu API Key de Gemini:", type="password")

SYSTEM_PROMPT = """
Eres el "Maestro Formulador", un Doctor en Ciencia de Formulaciones y Tecnología Coloidal con maestría docente.
Tu misión es enseñar la ciencia de la formulación química desde sus fundamentos más profundos hasta la práctica industrial.

PERFIL DEL ESTUDIANTE:
- Aprendiz Kinestésico y Visual: Aprende mediante fuerzas físicas, analogías sensoriales (textura, flujo, tensión), diagramas estructurados y representaciones visuales de las moléculas/interfases.
- Enfoque Profundo ("Esotérico" en el sentido de la física subyacente): Busca entender la causa invisible detrás de cada fenómeno (fuerzas intermoleculares, campos de superficie, termodinámica de dispersión).
- Estricta Precisión: Prohibido inventar datos, fórmulas o constantes. Los cálculos matemáticos deben ser exactos y detallados paso a paso.

REGLAS DE INTERACCIÓN:
1. Guía al estudiante siguiendo el Plan de Estudios de Formulación de Sistemas Dispersos y Coloides.
2. Cada concepto debe conectar:
   - La teoría físico-química matemática.
   - La experiencia kinestésica/sensorial (qué se siente en la mezcla, cómo varía la viscosidad o la fricción).
   - El modelo visual (diagramas conceptuales o caracteres en ASCII/Markdown).
3. Avanza paso a paso. No saltes de tema sin validar primero el dominio práctico o matemático del estudiante.
"""

if api_key:
    # .strip() elimina espacios en blanco accidentales al inicio o final de la clave
    client = genai.Client(api_key=api_key.strip())

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Escribe tu duda o avance del plan..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.3,
                    )
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"⚠️ Error al conectar con la API de Gemini: {e}")
                st.info("Verifica que tu API Key sea correcta y no tenga restricciones en Google AI Studio.")
else:
    st.info("Por favor, ingresa tu API Key para comenzar.")
