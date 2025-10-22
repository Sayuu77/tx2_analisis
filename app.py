import streamlit as st
from textblob import TextBlob
from streamlit_lottie import st_lottie
import requests
import time

# Configuración de la página
st.set_page_config(
    page_title="English Sentiment Analyzer",
    page_icon="💕",
    layout="centered"
)

# --- CSS ---
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

# Función para cargar animaciones Lottie desde URL
def load_lottie_url(url: str):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

# URLs de animaciones Lottie actualizadas - una realmente triste
lottie_animations = {
    "positive": "https://assets2.lottiefiles.com/packages/lf20_touohxv0.json",  # Feliz
    "negative": "https://assets1.lottiefiles.com/packages/lf20_1d2yfchc.json",  # Persona llorando - muy triste
    "neutral": "https://assets2.lottiefiles.com/packages/lf20_u4yrau.json"     # Neutral
}

# Función para corrección de texto
def correct_english_text(text):
    if not text.strip():
        return text
    try:
        blob = TextBlob(text)
        return str(blob.correct())
    except:
        return text

# --- Título principal ---
st.markdown('<h1 class="main-title">💕 Mood Analyzer</h1>', unsafe_allow_html=True)

# Sección de análisis de sentimientos
st.markdown('<div class="section-title">Text Analysis</div>', unsafe_allow_html=True)

text_input = st.text_area(
    "Enter the text you want to analyze:",
    placeholder="Example: 'I am feeling very happy with the results...'",
    height=100,
    key="sentiment_input"
)

polarity = 0
subjectivity = 0
sentiment_text = ""
sentiment_class = ""
corrected_text = ""

if text_input:
    with st.spinner('🔧 Correcting text...'):
        corrected_text = correct_english_text(text_input)
    
    blob = TextBlob(corrected_text)
    polarity = round(blob.sentiment.polarity, 2)
    subjectivity = round(blob.sentiment.subjectivity, 2)
    
    if polarity >= 0.1:
        sentiment_text = "😊 Positive Sentiment"
        sentiment_class = "positive"
        lottie_key = "positive"
    elif polarity <= -0.1:
        sentiment_text = "😢 Negative Sentiment"
        sentiment_class = "negative"
        lottie_key = "negative"
    else:
        sentiment_text = "😐 Neutral Sentiment"
        sentiment_class = "neutral"
        lottie_key = "neutral"
    
    # Mostrar animación Lottie
    lottie_json = load_lottie_url(lottie_animations[lottie_key])
    if lottie_json:
        st_lottie(
            lottie_json,
            height=300,
            width=300,
            key=f"lottie_{lottie_key}_{time.time()}"
        )
    else:
        st.warning(f"⚠️ Could not load animation for {lottie_key} sentiment")

# Mostrar resultados del análisis
if text_input:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Polarity</div>
            <div class="metric-value">{polarity}</div>
            <small style="color: #880E4F;">-1 (negative) to 1 (positive)</small>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Subjectivity</div>
            <div class="metric-value">{subjectivity}</div>
            <small style="color: #880E4F;">0 (objective) to 1 (subjective)</small>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown(f'<div class="sentiment-result {sentiment_class}">{sentiment_text}</div>', unsafe_allow_html=True)

# Línea divisoria
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Sección de Corrección Automática
st.markdown('<div class="section-title">Automatic Correction</div>', unsafe_allow_html=True)

if text_input:
    st.markdown("**Text has been automatically corrected:**")
    
    col_orig, col_correct = st.columns(2)
    
    with col_orig:
        st.markdown('<div class="correction-title">Original text:</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="correction-box">{text_input}</div>', unsafe_allow_html=True)
    
    with col_correct:
        st.markdown('<div class="correction-title">Corrected text:</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="correction-box">{corrected_text}</div>', unsafe_allow_html=True)
    
    # Mostrar estado de la corrección
    if text_input.lower() != corrected_text.lower():
        st.success("✅ Errors have been corrected in the text")
    else:
        st.info("🎉 The text is already correct")
else:
    st.info("✍️ Enter text above to see automatic correction here")

# Sidebar informativo
with st.sidebar:
    st.markdown("### ℹ️ About Analysis")
    st.markdown("**Polarity:** Measures if the text is positive, negative or neutral")
    st.markdown("**Subjectivity:** Indicates if the text is objective (facts) or subjective (opinions)")
    
    st.markdown("### 💡 How It Works")
    st.markdown("""
    • **English text only**  
    • **Automatic spelling correction**  
    • **Real-time processing**  
    • **Sentiment analysis**  
    """)

# Footer
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: #888; font-size: 0.9rem;'>"
    "English Sentiment Analyzer • Automatic text correction"
    "</div>",
    unsafe_allow_html=True
)
