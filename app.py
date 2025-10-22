import streamlit as st
from textblob import TextBlob
from googletrans import Translator

# Configuración de la página
st.set_page_config(
    page_title="Analizador de Sentimientos",
    page_icon="💕",
    layout="centered"
)

# Aplicar estilos CSS minimalistas
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        color: #EC407A;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    .section-title {
        font-size: 1.5rem;
        color: #EC407A;
        margin: 2rem 0 1rem 0;
        font-weight: 600;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #F8BBD0;
    }
    .metric-card {
        background-color: #FCE4EC;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #EC407A;
    }
    .sentiment-result {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
    }
    .positive {
        background-color: #E8F5E8;
        color: #2E7D32;
        border: 1px solid #A5D6A7;
    }
    .negative {
        background-color: #FFEBEE;
        color: #C62828;
        border: 1px solid #EF9A9A;
    }
    .neutral {
        background-color: #FFF8E1;
        color: #F57F17;
        border: 1px solid #FFE082;
    }
    .correction-box {
        background-color: #F3E5F5;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 1px solid #E1BEE7;
    }
    .stTextArea textarea {
        border-radius: 8px;
        border: 1px solid #E1BEE7;
    }
    .info-box {
        background-color: #F3E5F5;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

translator = Translator()

# Título principal
st.markdown('<h1 class="main-title">💕 Analizador de Sentimientos</h1>', unsafe_allow_html=True)

# Sección de Análisis de Sentimientos
st.markdown('<div class="section-title">📝 Análisis de Texto</div>', unsafe_allow_html=True)

text_input = st.text_area(
    "Escribe el texto que quieres analizar:",
    placeholder="Ej: 'Me siento muy contento con los resultados...'",
    height=100
)

if text_input:
    # Análisis de sentimiento
    translation = translator.translate(text_input, src="es", dest="en")
    trans_text = translation.text
    blob = TextBlob(trans_text)
    
    polarity = round(blob.sentiment.polarity, 2)
    subjectivity = round(blob.sentiment.subjectivity, 2)
    
    # Mostrar métricas
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <h4>📊 Polaridad</h4>
            <h3>{polarity}</h3>
            <small>Sentimiento: -1 (negativo) a 1 (positivo)</small>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <h4>🎯 Subjetividad</h4>
            <h3>{subjectivity}</h3>
            <small>0 (objetivo) a 1 (subjetivo)</small>
        </div>
        ''', unsafe_allow_html=True)
    
    # Resultado del sentimiento
    if polarity >= 0.5:
        st.markdown('<div class="sentiment-result positive">😊 Sentimiento Positivo</div>', unsafe_allow_html=True)
    elif polarity <= -0.5:
        st.markdown('<div class="sentiment-result negative">😔 Sentimiento Negativo</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sentiment-result neutral">😐 Sentimiento Neutral</div>', unsafe_allow_html=True)

# Línea divisoria
st.markdown("---")

# Sección de Corrección en Inglés
st.markdown('<div class="section-title">✏️ Corrección de Inglés</div>', unsafe_allow_html=True)

english_input = st.text_area(
    "Escribe texto en inglés para corregir:",
    placeholder="Ej: 'I am very hapy with the resuls...'",
    height=100,
    key="english_correction"
)

if english_input:
    blob_english = TextBlob(english_input)
    corrected_text = str(blob_english.correct())
    
    st.markdown("**Texto original:**")
    st.markdown(f'<div class="correction-box">{english_input}</div>', unsafe_allow_html=True)
    
    st.markdown("**Texto corregido:**")
    st.markdown(f'<div class="correction-box">{corrected_text}</div>', unsafe_allow_html=True)
    
    if english_input != corrected_text:
        st.info("✅ Se han corregido errores en el texto")
    else:
        st.success("🎉 El texto ya está correcto")

# Información en sidebar
with st.sidebar:
    st.markdown("### ℹ️ Acerca del Análisis")
    
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("**Polaridad:** Mide si el texto es positivo, negativo o neutral")
    st.markdown("**Subjetividad:** Indica si el texto es objetivo (hechos) o subjetivo (opiniones)")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("### 💡 Consejos")
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("• Escribe textos completos para mejor análisis")
    st.markdown("• La corrección funciona solo en inglés")
    st.markdown("• Los textos más largos dan resultados más precisos")
    st.markdown("</div>", unsafe_allow_html=True)

# Footer simple
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; font-size: 0.9rem;'>"
    "Analizador de Sentimientos • Desarrollado con TextBlob y Streamlit"
    "</div>",
    unsafe_allow_html=True
)
