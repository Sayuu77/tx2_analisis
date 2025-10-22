import streamlit as st
from textblob import TextBlob
from googletrans import Translator
import time

# Configuración de la página
st.set_page_config(
    page_title="Analizador de Sentimientos",
    page_icon="💕",
    layout="centered"
)

# Aplicar estilos CSS mejorados
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        color: #E91E63;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    .section-title {
        font-size: 1.5rem;
        color: #E91E63;
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
        border-left: 4px solid #E91E63;
    }
    .metric-value {
        color: #E91E63;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .metric-label {
        color: #880E4F;
        font-weight: 500;
    }
    .sentiment-result {
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .positive {
        background-color: #E8F5E8;
        color: #2E7D32;
        border: 2px solid #A5D6A7;
    }
    .negative {
        background-color: #FFEBEE;
        color: #C62828;
        border: 2px solid #EF9A9A;
    }
    .neutral {
        background-color: #FFF8E1;
        color: #F57F17;
        border: 2px solid #FFE082;
    }
    .correction-box {
        background-color: #F3E5F5;
        padding: 1.2rem;
        border-radius: 8px;
        margin: 0.8rem 0;
        border: 2px solid #E1BEE7;
        color: #4A148C;
        font-size: 1rem;
    }
    .correction-title {
        color: #7B1FA2;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .stTextArea textarea {
        border-radius: 8px;
        border: 2px solid #E1BEE7;
        font-size: 1rem;
    }
    .info-box {
        background-color: #F3E5F5;
        padding: 1.2rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 0.9rem;
        color: #4A148C;
        border: 1px solid #E1BEE7;
    }
    .divider {
        margin: 2rem 0;
        border-top: 2px solid #F8BBD0;
    }
</style>
""", unsafe_allow_html=True)

translator = Translator()

def correct_text(text):
    """Corrige el texto automáticamente en español o inglés"""
    if not text.strip():
        return text
    
    try:
        # Detectar idioma
        detected = translator.detect(text)
        lang = detected.lang
        
        # Si es español, traducir a inglés, corregir y volver a español
        if lang == 'es':
            # Traducir a inglés
            translated = translator.translate(text, src='es', dest='en')
            # Corregir en inglés
            blob = TextBlob(translated.text)
            corrected_en = str(blob.correct())
            # Volver a español
            corrected_es = translator.translate(corrected_en, src='en', dest='es')
            return corrected_es.text
        else:
            # Corregir directamente en inglés
            blob = TextBlob(text)
            return str(blob.correct())
    except:
        # En caso de error, devolver texto original
        return text

# Título principal
st.markdown('<h1 class="main-title">💕 Analizador de Sentimientos</h1>', unsafe_allow_html=True)

# Sección de Análisis de Sentimientos
st.markdown('<div class="section-title">📝 Análisis de Texto</div>', unsafe_allow_html=True)

text_input = st.text_area(
    "Escribe el texto que quieres analizar:",
    placeholder="Ej: 'Me siento muy contento con los resultados...'",
    height=100,
    key="sentiment_input"
)

if text_input:
    # Análisis de sentimiento
    translation = translator.translate(text_input, src="es", dest="en")
    trans_text = translation.text
    blob = TextBlob(trans_text)
    
    polarity = round(blob.sentiment.polarity, 2)
    subjectivity = round(blob.sentiment.subjectivity, 2)
    
    # Mostrar métricas con mejor contraste
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">📊 Polaridad</div>
            <div class="metric-value">{polarity}</div>
            <small style="color: #880E4F;">-1 (negativo) a 1 (positivo)</small>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">🎯 Subjetividad</div>
            <div class="metric-value">{subjectivity}</div>
            <small style="color: #880E4F;">0 (objetivo) a 1 (subjetivo)</small>
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
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Sección de Corrección Instantánea
st.markdown('<div class="section-title">✏️ Corrección Instantánea</div>', unsafe_allow_html=True)

st.markdown("Escribe en español o inglés y se corregirá automáticamente:")

# Usar session_state para mantener el texto corregido
if 'corrected_text' not in st.session_state:
    st.session_state.corrected_text = ""

correction_input = st.text_area(
    "Texto a corregir:",
    placeholder="Ej: 'Hojos' se corregirá a 'Ojos' o 'I am sadaa' a 'I am sad'",
    height=100,
    key="correction_input"
)

# Corrección instantánea
if correction_input:
    with st.spinner('Corrigiendo...'):
        # Pequeña pausa para que se vea el spinner
        time.sleep(0.5)
        corrected = correct_text(correction_input)
        st.session_state.corrected_text = corrected

# Mostrar resultado de corrección si existe
if st.session_state.corrected_text and correction_input:
    col_orig, col_correct = st.columns(2)
    
    with col_orig:
        st.markdown('<div class="correction-title">Texto original:</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="correction-box">{correction_input}</div>', unsafe_allow_html=True)
    
    with col_correct:
        st.markdown('<div class="correction-title">Texto corregido:</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="correction-box">{st.session_state.corrected_text}</div>', unsafe_allow_html=True)
    
    # Mostrar mensaje de estado
    if correction_input != st.session_state.corrected_text:
        st.success("✅ Se han corregido errores en el texto")
    else:
        st.info("🎉 El texto ya está correcto")

# Información en sidebar
with st.sidebar:
    st.markdown("### ℹ️ Acerca del Análisis")
    
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("**Polaridad:** Mide si el texto es positivo, negativo o neutral")
    st.markdown("**Subjetividad:** Indica si el texto es objetivo (hechos) o subjetivo (opiniones)")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("### 💡 Corrección Automática")
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("• Funciona en español e inglés")
    st.markdown("• Corrección instantánea")
    st.markdown("• Detecta automáticamente el idioma")
    st.markdown("• Ejemplo: 'Hojos' → 'Ojos'")
    st.markdown("• Ejemplo: 'sadaa' → 'sad'")
    st.markdown("</div>", unsafe_allow_html=True)

# Footer simple
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: #888; font-size: 0.9rem;'>"
    "Analizador de Sentimientos • Corrección automática en español e inglés"
    "</div>",
    unsafe_allow_html=True
)
