import streamlit as st
from textblob import TextBlob
from googletrans import Translator
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

translator = Translator()

def correct_spanish_text(text):
    """Corrige texto en español usando un enfoque combinado"""
    if not text.strip():
        return text
    
    # Diccionario de correcciones comunes en español
    common_corrections = {
        'hojos': 'ojos', 'muncho': 'mucho', 'haiga': 'haya', 'asercarse': 'acercarse',
        'cocreta': 'croqueta', 'dotor': 'doctor', 'estubes': 'estuviste', 'haver': 'haber',
        'hiba': 'iba', 'ansina': 'así', 'entonses': 'entonces', 'dijistes': 'dijiste',
        'vinistes': 'viniste', 'truje': 'traje', 'naiden': 'nadie', 'mesmo': 'mismo',
        'vide': 'vi', 'pacencia': 'paciencia', 'cocinar': 'cocinar', 'recebir': 'recibir',
        'satisfacer': 'satisfacer', 'yeba': 'lleve', 'callo': 'calló', 'valla': 'vaya',
        'aya': 'haya', 'echo': 'hecho', 'ha': 'ha', 'hechar': 'echar', 'hico': 'hizo',
        'hubieron': 'hubo', 'inflación': 'inflación', 'jente': 'gente', 'mirar': 'mirar',
        'pongo': 'pongo', 'practicar': 'practicar', 'preveer': 'prever', 'sabía': 'sabía',
        'tener': 'tener', 'vien': 'bien', 'vueno': 'bueno', 'zeda': 'ceda'
    }
    
    # Aplicar correcciones palabra por palabra
    words = text.split()
    corrected_words = []
    
    for word in words:
        # Limpiar la palabra de signos de puntuación
        clean_word = re.sub(r'[^\w]', '', word.lower())
        
        # Si la palabra está en nuestro diccionario de correcciones, corregirla
        if clean_word in common_corrections:
            corrected_word = common_corrections[clean_word]
            # Mantener la capitalización original si la palabra empezaba con mayúscula
            if word[0].isupper():
                corrected_word = corrected_word.capitalize()
            corrected_words.append(corrected_word)
        else:
            corrected_words.append(word)
    
    return ' '.join(corrected_words)

def correct_text(text):
    """Corrige el texto automáticamente detectando el idioma"""
    if not text.strip():
        return text
    
    try:
        # Detectar idioma
        detected = translator.detect(text)
        lang = detected.lang
        
        if lang == 'es':
            # Usar nuestro corrector personalizado para español
            return correct_spanish_text(text)
        else:
            # Usar TextBlob para inglés
            blob = TextBlob(text)
            return str(blob.correct())
    except:
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

# Variables para almacenar resultados
polarity = 0
subjectivity = 0
sentiment_text = ""
corrected_text = ""

if text_input:
    # Primero corregir el texto
    corrected_text = correct_text(text_input)
    
    # Análisis de sentimiento con el texto corregido
    translation = translator.translate(corrected_text, src="es", dest="en")
    trans_text = translation.text
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

# Mostrar resultados del análisis si hay texto
if text_input:
    # Mostrar métricas
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
    if text_input:
        st.markdown(f'<div class="sentiment-result {sentiment_class}">{sentiment_text}</div>', unsafe_allow_html=True)

# Línea divisoria
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Sección de Corrección Automática
st.markdown('<div class="section-title">✏️ Corrección Automática</div>', unsafe_allow_html=True)

# Mostrar corrección automática del texto analizado
if text_input:
    st.markdown("**El texto se ha corregido automáticamente:**")
    
    col_orig, col_correct = st.columns(2)
    
    with col_orig:
        st.markdown('<div class="correction-title">Texto original:</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="correction-box">{text_input}</div>', unsafe_allow_html=True)
    
    with col_correct:
        st.markdown('<div class="correction-title">Texto corregido:</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="correction-box">{corrected_text}</div>', unsafe_allow_html=True)
    
    # Mostrar mensaje de estado
    if text_input.lower() != corrected_text.lower():
        st.success("✅ Se han corregido errores en el texto")
        st.info("💡 **Ejemplos de corrección:** 'Hojos' → 'Ojos', 'sadaa' → 'sad'")
    else:
        st.info("🎉 El texto ya está correcto")
else:
    st.info("✍️ Escribe texto arriba para ver la corrección automática aquí")

# Información en sidebar
with st.sidebar:
    st.markdown("### ℹ️ Acerca del Análisis")
    
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("**Polaridad:** Mide si el texto es positivo, negativo o neutral")
    st.markdown("**Subjetividad:** Indica si el texto es objetivo (hechos) o subjetivo (opiniones)")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("### 💡 Corrección Automática")
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("• **Funciona en español e inglés**")
    st.markdown("• **Corrección instantánea**")
    st.markdown("• **Ejemplos en español:**")
    st.markdown("  - 'Hojos' → 'Ojos'")
    st.markdown("  - 'muncho' → 'mucho'")
    st.markdown("  - 'haiga' → 'haya'")
    st.markdown("• **Ejemplos en inglés:**")
    st.markdown("  - 'sadaa' → 'sad'")
    st.markdown("  - 'hapy' → 'happy'")
    st.markdown("</div>", unsafe_allow_html=True)

# Footer simple
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: #888; font-size: 0.9rem;'>"
    "Analizador de Sentimientos • Corrección automática en español e inglés"
    "</div>",
    unsafe_allow_html=True
)
