import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator
import re

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

def detect_language(text):
    """Detecta el idioma del texto de forma simple"""
    # Caracteres comunes en español
    spanish_chars = set('áéíóúñÁÉÍÓÚÑ')
    if any(char in text for char in spanish_chars):
        return 'es'
    
    # Palabras comunes en español
    spanish_words = ['el', 'la', 'los', 'las', 'de', 'que', 'y', 'en', 'un', 'una', 'es', 'son']
    words = text.lower().split()
    spanish_count = sum(1 for word in words if word in spanish_words)
    
    if spanish_count > len(words) * 0.3:  # Si más del 30% son palabras españolas
        return 'es'
    else:
        return 'en'

def correct_text_automatically(text):
    """Corrige texto automáticamente para cualquier palabra"""
    if not text.strip():
        return text
    
    try:
        # Detectar idioma
        lang = detect_language(text)
        
        if lang == 'es':
            # Para español: usar traducción bidireccional
            try:
                # Traducir a inglés
                translated_en = GoogleTranslator(source='es', target='en').translate(text)
                # Corregir en inglés (TextBlob funciona mejor en inglés)
                blob_en = TextBlob(translated_en)
                corrected_en = str(blob_en.correct())
                # Traducir de vuelta a español
                corrected_es = GoogleTranslator(source='en', target='es').translate(corrected_en)
                return corrected_es
            except Exception as e:
                # Fallback: corrección directa
                blob = TextBlob(text)
                return str(blob.correct())
        else:
            # Para inglés: corrección directa
            blob = TextBlob(text)
            return str(blob.correct())
            
    except Exception as e:
        # Si falla todo, devolver texto original
        return text

# Título principal
st.markdown('<h1 class="main-title">💕 Analizador de Sentimientos</h1>', unsafe_allow_html=True)

# Sección de Análisis de Sentimientos
st.markdown('<div class="section-title">📝 Análisis de Texto</div>', unsafe_allow_html=True)

text_input = st.text_area(
    "Escribe el texto que quieres analizar:",
    placeholder="Escribe cualquier texto en español o inglés...",
    height=100,
    key="sentiment_input"
)

# Variables para almacenar resultados
polarity = 0
subjectivity = 0
sentiment_text = ""
corrected_text = ""

if text_input:
    # Corregir texto automáticamente
    with st.spinner('🔧 Corrigiendo texto...'):
        corrected_text = correct_text_automatically(text_input)
    
    # Análisis de sentimiento
    try:
        # Traducir a inglés para análisis (TextBlob funciona mejor en inglés)
        if detect_language(corrected_text) == 'es':
            trans_text = GoogleTranslator(source='es', target='en').translate(corrected_text)
        else:
            trans_text = corrected_text
    except:
        trans_text = corrected_text

    # Análisis de sentimiento
    blob = TextBlob(trans_text)
    polarity = round(blob.sentiment.polarity, 2)
    subjectivity = round(blob.sentiment.subjectivity, 2)
    
    # Determinar sentimiento
    if polarity >= 0.5:
        sentiment_text = "😊 Sentimiento Positivo"
        sentiment_class = "positive"
    elif polarity <= -0.5:
        sentiment_text = "😔 Sentimiento Negativo"
        sentiment_class = "negative"
    else:
        sentiment_text = "😐 Sentimiento Neutral"
        sentiment_class = "neutral"

# Mostrar resultados del análisis
if text_input:
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
    
    st.markdown(f'<div class="sentiment-result {sentiment_class}">{sentiment_text}</div>', unsafe_allow_html=True)

# Línea divisoria
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Sección de Corrección Automática
st.markdown('<div class="section-title">✏️ Corrección Automática</div>', unsafe_allow_html=True)

if text_input:
    st.markdown("**El texto se ha corregido automáticamente:**")
    
    col_orig, col_correct = st.columns(2)
    
    with col_orig:
        st.markdown('<div class="correction-title">Texto original:</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="correction-box">{text_input}</div>', unsafe_allow_html=True)
    
    with col_correct:
        st.markdown('<div class="correction-title">Texto corregido:</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="correction-box">{corrected_text}</div>', unsafe_allow_html=True)
    
    # Mostrar estado de la corrección
    if text_input.lower() != corrected_text.lower():
        st.success("✅ Se han corregido errores en el texto")
    else:
        st.info("🎉 El texto ya está correcto")
else:
    st.info("✍️ Escribe texto arriba para ver la corrección automática aquí")

# Sidebar informativo
with st.sidebar:
    st.markdown("### ℹ️ Acerca del Análisis")
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("**Polaridad:** Mide si el texto es positivo, negativo o neutral")
    st.markdown("**Subjetividad:** Indica si el texto es objetivo (hechos) o subjetivo (opiniones)")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("### 💡 Cómo Funciona")
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    • **Detección automática** de idioma
    • **Corrección inteligente** para cualquier palabra
    • **Funciona en español e inglés**
    • **Procesamiento en tiempo real**
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: #888; font-size: 0.9rem;'>"
    "Analizador de Sentimientos • Corrección automática universal"
    "</div>",
    unsafe_allow_html=True
)
