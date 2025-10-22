import streamlit as st
from textblob import TextBlob
from googletrans import Translator

# Configuración de la página
st.set_page_config(
    page_title="Sentiment Analyzer Pro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar estilos CSS personalizados
st.markdown("""
<style>
    .main-title {
        font-size: 3.2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 800;
        padding: 1rem;
    }
    .sub-title {
        font-size: 1.4rem;
        color: #4A5568;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    .section-header {
        font-size: 1.6rem;
        color: #2D3748;
        margin: 2rem 0 1rem 0;
        font-weight: 700;
        border-left: 5px solid #667eea;
        padding-left: 15px;
        background: linear-gradient(90deg, #F7FAFC, transparent);
        padding: 1rem 1.5rem;
        border-radius: 10px;
    }
    .sentiment-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .metric-box {
        background: white;
        color: #2D3748;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .correction-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .original-text {
        background: #EDF2F7;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #E53E3E;
    }
    .corrected-text {
        background: #C6F6D5;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #38A169;
    }
    .emoji-size {
        font-size: 2rem;
        margin-right: 10px;
    }
    .sidebar-content {
        background: linear-gradient(180deg, #F7FAFC 0%, #EDF2F7 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #E2E8F0;
        padding: 1rem;
        font-size: 1rem;
    }
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    .divider {
        border-top: 3px solid #E2E8F0;
        margin: 2rem 0;
    }
    .feature-icon {
        font-size: 1.5rem;
        margin-right: 10px;
    }
    .positive {
        color: #38A169;
        font-weight: 600;
    }
    .negative {
        color: #E53E3E;
        font-weight: 600;
    }
    .neutral {
        color: #D69E2E;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

translator = Translator()

# Header principal
st.markdown('<h1 class="main-title">🧠 Sentiment Analyzer Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Analiza sentimientos y corrige texto en inglés con inteligencia artificial</p>', unsafe_allow_html=True)

# Layout principal
col1, col2 = st.columns([2, 1])

with col1:
    # Sección de Análisis de Sentimientos
    st.markdown('<div class="section-header">📊 Análisis de Sentimientos</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;'>
            <h3 style='margin:0; color:white;'>✨ Escribe tu texto para analizar</h3>
            <p style='margin:0; opacity:0.9;'>El sistema detectará automáticamente el sentimiento y lo traducirá para análisis preciso</p>
        </div>
        """, unsafe_allow_html=True)
        
        text1 = st.text_area(
            'Escribe tu texto aquí:',
            placeholder='Ej: "Estoy muy feliz con los resultados obtenidos hoy..."',
            height=120,
            key='sentiment_input'
        )
        
        if text1:
            with st.spinner('🔍 Analizando sentimiento...'):
                # Traducción y análisis
                translation = translator.translate(text1, src="es", dest="en")
                trans_text = translation.text
                blob = TextBlob(trans_text)
                
                # Métricas
                polarity = round(blob.sentiment.polarity, 2)
                subjectivity = round(blob.sentiment.subjectivity, 2)
                
                # Tarjeta de resultados
                st.markdown('<div class="sentiment-card">', unsafe_allow_html=True)
                
                col_met1, col_met2 = st.columns(2)
                with col_met1:
                    st.markdown(f"""
                    <div class="metric-box">
                        <h3 style='margin:0; color:#2D3748;'>📈 Polaridad</h3>
                        <p style='font-size: 2rem; font-weight: bold; margin:0; color:#667eea;'>{polarity}</p>
                        <p style='margin:0; color:#718096;'>Rango: -1 (Negativo) a 1 (Positivo)</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_met2:
                    st.markdown(f"""
                    <div class="metric-box">
                        <h3 style='margin:0; color:#2D3748;'>🎯 Subjetividad</h3>
                        <p style='font-size: 2rem; font-weight: bold; margin:0; color:#764ba2;'>{subjectivity}</p>
                        <p style='margin:0; color:#718096;'>Rango: 0 (Objetivo) a 1 (Subjetivo)</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Determinación del sentimiento
                st.markdown('</div>', unsafe_allow_html=True)
                
                if polarity >= 0.5:
                    st.markdown(f"""
                    <div style='background: #C6F6D5; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 6px solid #38A169;'>
                        <h3 style='margin:0; color:#22543D;'>😊 Sentimiento Positivo</h3>
                        <p style='margin:0; color:#22543D;'>El texto expresa emociones positivas y optimismo</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif polarity <= -0.5:
                    st.markdown(f"""
                    <div style='background: #FED7D7; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 6px solid #E53E3E;'>
                        <h3 style='margin:0; color:#742A2A;'>😔 Sentimiento Negativo</h3>
                        <p style='margin:0; color:#742A2A;'>El texto expresa emociones negativas o pesimismo</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='background: #FEFCBF; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 6px solid #D69E2E;'>
                        <h3 style='margin:0; color:#744210;'>😐 Sentimiento Neutral</h3>
                        <p style='margin:0; color:#744210;'>El texto mantiene un tono neutral y objetivo</p>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Sección de Corrección en Inglés
    st.markdown('<div class="section-header">✏️ Corrección de Texto en Inglés</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;'>
            <h3 style='margin:0; color:white;'>🔧 Corrige tu texto en inglés</h3>
            <p style='margin:0; opacity:0.9;'>Escribe texto en inglés y el sistema corregirá automáticamente los errores ortográficos</p>
        </div>
        """, unsafe_allow_html=True)
        
        text2 = st.text_area(
            'Escribe texto en inglés:',
            placeholder='Ej: "I am very hapy with the resuls..."',
            height=120,
            key='correction_input'
        )
        
        if text2:
            with st.spinner('🔧 Corrigiendo texto...'):
                blob2 = TextBlob(text2)
                corrected_text = str(blob2.correct())
                
                # Mostrar comparación
                col_orig, col_corr = st.columns(2)
                
                with col_orig:
                    st.markdown('<div class="original-text">', unsafe_allow_html=True)
                    st.markdown('**📝 Texto Original:**')
                    st.info(text2)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col_corr:
                    st.markdown('<div class="corrected-text">', unsafe_allow_html=True)
                    st.markdown('**✅ Texto Corregido:**')
                    st.success(corrected_text)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Mostrar cambios específicos si hay diferencias
                if text2 != corrected_text:
                    st.markdown("""
                    <div style='background: #E6FFFA; padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #319795;'>
                        <h4 style='margin:0; color:#234E52;'>🔄 Cambios Realizados:</h4>
                        <p style='margin:0; color:#234E52;'>El sistema ha detectado y corregido errores ortográficos en tu texto.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style='background: #F0FFF4; padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #38A169;'>
                        <h4 style='margin:0; color:#22543D;'>✅ Texto Correcto</h4>
                        <p style='margin:0; color:#22543D;'>¡Excelente! Tu texto en inglés no contiene errores ortográficos detectables.</p>
                    </div>
                    """, unsafe_allow_html=True)

with col2:
    # Sidebar informativo
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown('## 📚 Guía de Análisis')
    
    st.markdown('### 📈 Polaridad')
    st.markdown("""
    <div style='background: white; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;'>
        <p><strong>Valor:</strong> -1 a 1</p>
        <p><strong>Positivo:</strong> > 0.5 😊</p>
        <p><strong>Neutral:</strong> -0.5 a 0.5 😐</p>
        <p><strong>Negativo:</strong> < -0.5 😔</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('### 🎯 Subjetividad')
    st.markdown("""
    <div style='background: white; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;'>
        <p><strong>Valor:</strong> 0 a 1</p>
        <p><strong>Objetivo:</strong> < 0.3 📊</p>
        <p><strong>Neutral:</strong> 0.3 a 0.7 ⚖️</p>
        <p><strong>Subjetivo:</strong> > 0.7 💭</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('### 💡 Consejos')
    st.markdown("""
    <div style='background: white; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;'>
        <p>• Escribe textos completos para mejor análisis</p>
        <p>• Incluye contexto emocional</p>
        <p>• Evita textos muy cortos</p>
        <p>• Usa puntuación adecuada</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('### 🛠️ Corrección')
    st.markdown("""
    <div style='background: white; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;'>
        <p>• Corrige errores ortográficos</p>
        <p>• Solo funciona en inglés</p>
        <p>• Mejora la claridad del texto</p>
        <p>• Perfecto para emails y documentos</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center; color: #718096; padding: 2rem; background: #F7FAFC; border-radius: 10px;'>
        <h3 style='color: #2D3748;'>🧠 Sentiment Analyzer Pro</h3>
        <p>Analiza sentimientos y corrige texto con tecnología avanzada de procesamiento de lenguaje natural</p>
        <p><strong>Tecnologías:</strong> TextBlob • Googletrans • Streamlit</p>
    </div>
    """, 
    unsafe_allow_html=True
)
