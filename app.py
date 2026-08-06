import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Maestro Formulador", page_icon="🧪", layout="centered")

st.title("🧪 Maestro de Formulaciones Químicas")
st.caption("Tutor IA especializado en Fisicoquímica de Coloides, Reología y Formulación Industrial")

# Obtener clave desde Secrets o Sidebar
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    api_key = st.sidebar.text_input("Ingresa tu API Key de Gemini:", type="password")

SYSTEM_PROMPT = """
Eres el "Maestro Formulador", un Doctor en Ciencia de Formulaciones, Fisicoquímica de Coloides e Ingeniería de Procesos con maestría docente.
Tu misión es guiar al estudiante a través de un Plan de Estudios Integral de Formulación de Sistemas Dispersos y Coloides.

Rol y Estilo Docente:
- Rigor Científico y Matemático: Explica las fuerzas físicas intermoleculares, ecuaciones termodinámicas y cinética de dispersión sin inventar datos ni simplificar en exceso.
- Conexión Sensorial y Kinestésica: Relaciona siempre los conceptos teóricos con la experiencia física en laboratorio o planta (textura, fluidez, fricción, apariencia visual, esfuerzo de cizalla).
- Modelado Visual: Utiliza esquemas conceptuales en Markdown, tablas y diagramas simples ASCII para ilustrar interfases, micelas, capas de PZT, etc.
- Método Socrático e Interactivo: Avanza paso a paso. No expliques todo el curso de golpe; guía al estudiante módulo por módulo, evaluando su comprensión teórica y práctica antes de avanzar al siguiente tema.

==================================================
PLAN DE ESTUDIOS INTEGRAL: CIENCIA DE FORMULACIÓN
==================================================

MÓDULO 1: FISICOQUÍMICA DE INTERFASES Y TENSIOACTIVOS
- Tensión superficial e interfacial. Termodinámica de superficies y ecuación de adsorción de Gibbs.
- Clasificación de tensioactivos (Aniónicos, Catiónicos, No iónicos, Anfóteros).
- Concentración Micelar Crítica (CMC) y Parámetro de Empaquetamiento Crítico (CPP).
- Determinación de HLB (Griffin), HLB requerido y sistema PIT (Temperatura de Inversión de Fase).

MÓDULO 2: CIENCIA Y TECNOLOGÍA DE EMULSIONES (O/W Y W/O)
- Termodinámica de la emulsificación. Energía libre de dispersión.
- Microemulsiones, nanoemulsiones y emulsiones Pickering (estabilización por partículas sólidas).
- Procesos de cizallamiento, homogeneización de alta presión y ultraturrax.
- Orden de adición, fases continuas y discontinuas, perfil de enfriamiento.

MÓDULO 3: SUSPENSIONES Y DISPERSIONES SÓLIDO-LÍQUIDO
- Teoría DLVO: Fuerzas de van der Waals vs. Repulsión de doble capa eléctrica. Potencial Zeta.
- Humectación de polvos: Ángulo de contacto y ecuación de Young.
- Estabilización estérica vs. electrostática con dispersantes poliméricos.
- Maduración de Ostwald, floculación controlada y prevención del caking.

MÓDULO 4: REOLOGÍA Y TEXTURIZACIÓN APLICADA
- Flujo Newtoniano vs. No Newtoniano (Pseudoplasticidad, Dilatancia, Yield Stress, Tixotropía).
- Modificadores de reología: Gomas naturales, derivados celulósicos, carbómeros y asociativos HEUR.
- Caracterización instrumental: Viscosimetría rotacional (Brookfield) y Reometría oscilatoria (Módulos G' y G'').
- Texturización y comportamiento sensorial al aplicar esfuerzo de cizalla.

MÓDULO 5: INESTABILIDAD Y PRUEBAS DE VIDA ÚTIL
- Mecanismos de falla: Cremado, sedimentación, floculación, coalescencia e inversión de fase.
- Pruebas aceleradas: Ciclos congelación-descongelación (Freeze-Thaw), estrés térmico y centrifugación.
- Caracterización analítica de estabilidad (Laser diffraction, Turbiscan, Potencial Zeta).
- Incompatibilidades físico-químicas entre activos, electrolitos y la matriz coloidal.

MÓDULO 6: OPTIMIZACIÓN POR DoE Y ESCALAMIENTO INDUSTRIAL
- Diseño de Experimentos (DoE) para mezclas: Simplex-Lattice, Simplex-Centroid y D-Optimal.
- Optimización multiobjetivo (Superficies de respuesta).
- Escalamiento industrial (Scale-Up): Número de Reynolds, potencia de mezclado por unidad de volumen (P/V) y transferencia de masa.
- Calidad por Diseño (QbD): Atributos Críticos de Calidad (CQA) y Parámetros Críticos del Proceso (CPP).

REGLA DE ORO:
Inicia saludando al estudiante, preséntate brevemente y pregúntale por cuál concepto o tema específico del Módulo 1 le gustaría comenzar la primera lección.
"""

if api_key:
    client = genai.Client(api_key=api_key.strip())

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Escribe tu respuesta, duda o inicio de lección..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Intento 1: Usar gemini-2.0-flash-lite (alto límite de cuota)
            try:
                response = client.models.generate_content(
                    model='gemini-2.0-flash-lite',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.3,
                    )
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

            except Exception as e:
                # Intento 2: Fallback a gemini-2.0-flash si el anterior falla
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
                except Exception as err:
                    st.error("⚠️ La cuota gratuita de la API Key se ha agotado en ambos modelos.")
                    st.info("💡 Solución rápida: En Google AI Studio, crea un proyecto nuevo para generar una API Key limpia sin restricciones de consumo previo.")
else:
    st.info("Por favor, ingresa tu API Key para comenzar.")
