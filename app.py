import streamlit as st
from textblob import TextBlob

# Configuración de la página
st.set_page_config(
    page_title="Mood Analyzer",
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
    .lottie-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

def correct_english_text(text):
    """Corrige texto en inglés usando TextBlob"""
    if not text.strip():
        return text
    
    try:
        blob = TextBlob(text)
        return str(blob.correct())
    except:
        return text

# HTML para las animaciones Lottie
lottie_html = """
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
"""

# Inyectar el script de Lottie
st.components.v1.html(lottie_html, height=0)

# Título principal
st.markdown('<h1 class="main-title">💕 Mood Analyzer</h1>', unsafe_allow_html=True)

# Sección de Análisis de Sentimientos
st.markdown('<div class="section-title">Text Analysis</div>', unsafe_allow_html=True)

text_input = st.text_area(
    "Enter the text you want to analyze:",
    placeholder="Example: 'I am feeling very happy with the results...'",
    height=100,
    key="sentiment_input"
)

# Variables para almacenar resultados
polarity = 0
subjectivity = 0
sentiment_text = ""
corrected_text = ""
sentiment_type = ""

if text_input:
    # Corregir texto automáticamente
    with st.spinner('🔧 Correcting text...'):
        corrected_text = correct_english_text(text_input)
    
    # Análisis de sentimiento
    blob = TextBlob(corrected_text)
    polarity = round(blob.sentiment.polarity, 2)
    subjectivity = round(blob.sentiment.subjectivity, 2)
    
    # Determinar sentimiento
    if polarity >= 0.5:
        sentiment_text = "😊 Positive Sentiment"
        sentiment_class = "positive"
        sentiment_type = "positive"
        lottie_url = "https://assets1.lottiefiles.com/packages/lf20_vybwn7df.json"
        animation_name = "Happy Animation"
    elif polarity <= -0.5:
        sentiment_text = "😔 Negative Sentiment"
        sentiment_class = "negative"
        sentiment_type = "negative"
        lottie_url = "https://assets1.lottiefiles.com/packages/lf20_1pxqjqps.json"
        animation_name = "Sad Animation"
    else:
        sentiment_text = "😐 Neutral Sentiment"
        sentiment_class = "neutral"
        sentiment_type = "neutral"
        lottie_url = "https://assets1.lottiefiles.com/packages/lf20_gns3tjng.json"
        animation_name = "Neutral Animation"

# Mostrar animación Lottie si hay texto analizado
if text_input and sentiment_type:
    st.markdown(f"### 🎭 {animation_name}")
    
    # Crear el HTML para la animación Lottie
    animation_html = f"""
    <div class="lottie-container">
        <lottie-player 
            src="{lottie_url}"
            background="transparent" 
            speed="1" 
            style="width: 300px; height: 300px;" 
            loop 
            autoplay>
        </lottie-player>
    </div>
    
    <script>
        // Esperar a que se cargue la animación
        setTimeout(() => {{
            const player = document.querySelector('lottie-player');
            if (player) {{
                // Hacer crecer la animación
                player.style.transform = 'scale(1.5)';
                player.style.transition = 'transform 0.5s ease-in-out';
                
                // Después de 2 segundos, volver al tamaño normal
                setTimeout(() => {{
                    player.style.transform = 'scale(1)';
                }}, 2000);
                
                // Después de 4 segundos, desaparecer
                setTimeout(() => {{
                    player.style.opacity = '0';
                    player.style.transition = 'opacity 1s ease-in-out';
                }}, 4000);
            }}
        }}, 1000);
    </script>
    """
    
    # Mostrar la animación
    st.components.v1.html(animation_html, height=350)

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
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("**Polarity:** Measures if the text is positive, negative or neutral")
    st.markdown("**Subjectivity:** Indicates if the text is objective (facts) or subjective (opinions)")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("### 💡 How It Works")
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    • **English text only**
    • **Automatic spelling correction**
    • **Real-time processing**
    • **Sentiment analysis**
    • **Animated mood reactions**
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("### 🎭 Animations")
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("""
    **Positive:** Happy character animation
    **Negative:** Sad character with tears  
    **Neutral:** Thinking character
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: #888; font-size: 0.9rem;'>"
    "Mood Analyzer • Automatic text correction • Animated reactions"
    "</div>",
    unsafe_allow_html=True
)
