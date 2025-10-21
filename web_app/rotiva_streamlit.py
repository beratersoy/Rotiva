import streamlit as st
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from data_scraper.event_manager import EventManager
from rag_pipeline.rag_engine import RAGEngine
from utils.llm_client import OpenAIClient
from utils.sheets_manager import SheetsManager
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Rotiva - AI Etkinlik Asistanı", 
    page_icon="🎭", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# JavaScript to force sidebar open and clear localStorage
st.markdown("""
<script>
// Clear sidebar state from localStorage
if (window.localStorage) {
    Object.keys(localStorage).forEach(key => {
        if (key.includes('sidebar') || key.includes('collapsed')) {
            localStorage.removeItem(key);
        }
    });
}

// Force sidebar to be visible
(function forceSidebar() {
    const sidebar = parent.document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        sidebar.style.transform = 'translateX(0px)';
        sidebar.style.display = 'block';
        sidebar.style.visibility = 'visible';
        sidebar.style.left = '0px';
        sidebar.setAttribute('aria-expanded', 'true');
    }
    // Retry after a short delay if sidebar not found
    setTimeout(forceSidebar, 100);
})();
</script>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ============ HIDE STREAMLIT TOOLBAR ============ */
header[data-testid="stHeader"] {
    background-color: transparent;
    display: none;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* ============ MODERN GRADIENT BACKGROUND ============ */
body { 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-attachment: fixed;
}

/* ============ MODERN CHAT BUBBLES ============ */
.user-bubble {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #ffffff !important; 
    border-radius: 20px 20px 4px 20px;
    padding: 1em 1.4em; 
    max-width: 85%;
    min-width: 200px;
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
    border: none;
    animation: slideInRight 0.3s ease-out;
    font-size: 1rem;
    line-height: 1.6;
    font-weight: 400;
    word-break: keep-all;
    overflow-wrap: normal;
    white-space: normal;
    display: inline-block;
}

.bot-bubble {
    background: rgba(255, 255, 255, 0.98);
    color: #2d3748 !important; 
    border-radius: 20px 20px 20px 4px;
    padding: 1em 1.4em; 
    max-width: 85%;
    min-width: 200px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    animation: slideInLeft 0.3s ease-out;
    font-size: 0.95rem;
    line-height: 1.6;
    word-break: keep-all;
    overflow-wrap: normal;
    white-space: normal;
    display: inline-block;
}

/* ============ FIXED BLACK SIDEBAR (SOLID COLOR) ============ */
[data-testid="stSidebar"] {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    height: 100vh !important;
    width: 21rem !important;
    z-index: 999999 !important;
    background: #000000 !important;
    background-color: #000000 !important;
    background-image: none !important;
    transform: translateX(0) !important;
    transition: none !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
}

/* Force sidebar always visible - all states */
[data-testid="stSidebar"][aria-expanded="false"],
[data-testid="stSidebar"][aria-expanded="true"],
section[data-testid="stSidebar"] {
    transform: translateX(0) !important;
    display: block !important;
    visibility: visible !important;
    left: 0 !important;
    opacity: 1 !important;
}

/* Sidebar collapse button - completely remove */
[data-testid="collapsedControl"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

button[kind="header"] {
    display: none !important;
}

/* Override any Streamlit hiding classes */
.css-1544g2n, .css-163ttbj {
    display: block !important;
    visibility: visible !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: #000000 !important;
    background-color: #000000 !important;
    background-image: none !important;
    min-height: 100vh !important;
    height: auto !important;
}

[data-testid="stSidebar"] > div {
    background: #000000 !important;
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

[data-testid="stSidebar"] .stMarkdown {
    color: #ffffff !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.2) !important;
}

/* Checkbox, metric gibi sidebar elementleri */
[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
}

[data-testid="stSidebar"] [data-testid="stCheckbox"] {
    color: #ffffff !important;
}

/* ============ MODERN HEADER (FIXED, NEXT TO SIDEBAR) ============ */
.header {
    position: fixed;
    top: 0;
    left: 21rem;
    right: 0;
    z-index: 9999;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff; 
    border-radius: 0 0 24px 24px;
    padding: 1.2em 2em 1em 2em; 
    margin-bottom: 1em;
    box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
    text-align: left;
    transition: left 0.3s ease !important;
}

/* Header adjustment when sidebar is collapsed */
[data-testid="stSidebar"][aria-expanded="false"] ~ * .header {
    left: 0 !important;
}

/* Main content area - adjust for sidebar and header */
[data-testid="stAppViewContainer"] {
    margin-left: 21rem !important;
    transition: margin-left 0.3s ease !important;
}

/* When sidebar is collapsed */
[data-testid="stSidebar"][aria-expanded="false"] ~ [data-testid="stAppViewContainer"],
.css-1d391kg {
    margin-left: 0 !important;
}

[data-testid="stAppViewContainer"] > section:first-child {
    padding-top: 90px;
}

.header-title {
    font-size: 1.6em;
    font-weight: 700;
    margin-bottom: 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.header-subtitle {
    font-size: 0.95em;
    opacity: 0.9;
    font-weight: 300;
}

/* ============ MODERN CHAT INPUT ============ */
.stTextInput > div > div > input {
    background: rgba(255, 255, 255, 0.15) !important;
    color: #ffffff !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 16px !important;
    padding: 1em 1.5em !important;
    font-size: 1rem !important;
    backdrop-filter: blur(20px) !important;
    transition: all 0.3s ease !important;
    height: 48px !important;
    min-height: 48px !important;
    max-height: 48px !important;
    overflow: hidden !important;
}

.stTextInput > div > div > input::placeholder {
    color: rgba(255, 255, 255, 0.6) !important;
    font-weight: 400 !important;
}

.stTextInput > div > div > input:focus {
    border-color: rgba(102, 126, 234, 0.8) !important;
    background: rgba(255, 255, 255, 0.2) !important;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3) !important;
    transform: translateY(-2px) !important;
}

/* ============ MODERN SEND BUTTON ============ */
.stForm button[kind="primary"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 0.8em 2em !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
}

.stForm button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
}

/* ============ OFF-WHITE TEXT COLORS (Keep backgrounds) ============ */
.user-bubble {
    color: #f5f5f5 !important;
}

.bot-bubble {
    color: #2d3748 !important;
    white-space: pre-line !important;
}

/* ============ AVATAR STYLES ============ */
.avatar { 
    width: 42px; 
    height: 42px; 
    border-radius: 50%; 
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3em;
    margin-right: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.avatar-bot {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.avatar-user {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
}

/* ============ MESSAGE WRAPPER ============ */
.user-wrap { 
    display: flex; 
    justify-content: flex-end; 
    margin-bottom: 1.2em;
    animation: fadeIn 0.4s ease-in;
    min-height: fit-content;
}

.bot-wrap { 
    display: flex; 
    justify-content: flex-start; 
    margin-bottom: 1.2em;
    animation: fadeIn 0.4s ease-in;
    min-height: fit-content;
}

.msg-row { 
    display: flex; 
    gap: 12px; 
    align-items: flex-start;
    min-height: fit-content;
}

/* ============ TIMESTAMP ============ */
.timestamp { 
    font-size: 0.72rem; 
    color: #9ca3af; 
    margin-top: 6px;
    opacity: 0.7;
}

/* ============ SIDEBAR MODERN ============ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.95) 100%);
    backdrop-filter: blur(10px);
}

[data-testid="stSidebar"] h3 {
    color: #667eea;
    font-weight: 600;
}

/* ============ SPINNER (Loading) ============ */
.stSpinner > div {
    color: #667eea !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    text-align: center !important;
    opacity: 0.8 !important;
    padding: 1em 0 !important;
    background: rgba(255, 255, 255, 0.9) !important;
    border-radius: 8px !important;
    margin: 1em 0 !important;
}

.stSpinner > div > div {
    border-color: rgba(102, 126, 234, 0.3) !important;
    border-top-color: #667eea !important;
}

/* ============ METRICS CARD ============ */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.8);
    padding: 1em;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* ============ INPUT BOX ============ */
[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.95);
    padding: 1.2em;
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    backdrop-filter: blur(10px);
}

input[type="text"] {
    border-radius: 12px !important;
    border: 2px solid #e5e7eb !important;
    padding: 0.8em 1em !important;
    font-size: 0.95em !important;
    transition: all 0.3s ease !important;
}

input[type="text"]:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

/* ============ BUTTON MODERN ============ */
button[kind="primary"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.7em 1.5em !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
    transition: all 0.3s ease !important;
}

button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
}

/* ============ ANIMATIONS ============ */
@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* ============ LINKS IN MESSAGES ============ */
.bot-bubble a {
    color: #667eea;
    text-decoration: none;
    font-weight: 600;
    border-bottom: 2px solid rgba(102, 126, 234, 0.3);
    transition: all 0.2s ease;
}

.bot-bubble a:hover {
    color: #764ba2;
    border-bottom-color: #764ba2;
}

/* ============ CHECKBOX MODERN ============ */
[data-testid="stCheckbox"] label {
    font-weight: 500 !important;
    color: #4b5563 !important;
}

/* ============ RESPONSIVE ============ */
@media (max-width:640px) {
    .user-bubble, .bot-bubble { 
        max-width: 90%; 
    }
    .header { 
        border-radius: 0 0 16px 16px;
        padding: 1.2em 1em;
    }
    .header-title {
        font-size: 1.5em;
    }
}
</style>
""", unsafe_allow_html=True)

def get_bot_response(user_msg, name=None, use_live=False, use_rag=True):
    """
    Kullanıcı mesajına akıllı yanıt üret - RAG (Retrieval-Augmented Generation) destekli
    - use_rag=True: RAG Engine ile semantik arama + Gemini AI yanıt üretimi (ÖNERİLEN)
    - use_rag=False: Basit filtreleme + Gemini AI (yedek sistem)
    """
    from data_scraper.base_scraper import BaseEventScraper
    
    # Etkinlik verilerini EventManager'dan çek
    manager = EventManager(use_cache=not use_live)
    user_msg_lower = user_msg.lower()
    
    # Kullanıcı mesajından şehir bilgisini tespit et
    city = None
    if "kocaeli" in user_msg_lower or "izmit" in user_msg_lower:
        city = "Kocaeli"
    elif "sakarya" in user_msg_lower or "adapazarı" in user_msg_lower or "adapazari" in user_msg_lower:
        city = "Sakarya"
    
    # RAG ENGINE MODU (ÖNERİLEN) - Semantik arama ile en alakalı etkinlikleri bul
    if use_rag and (os.getenv('GEMINI_API_KEY') or os.getenv('OPENAI_API_KEY')):
        try:
            # RAG Engine'i başlat (tüm etkinliklerle)
            all_events = manager.get_all_events()
            rag_engine = RAGEngine(all_events)
            
            # Tarih filtresi varsa uygula
            start_date, end_date = BaseEventScraper.parse_turkish_date_query(user_msg)
            if start_date and end_date:
                # Tarihe göre filtrele
                filtered_events = []
                for event in all_events:
                    event_date = event.get('date', '')
                    normalized_date = BaseEventScraper.normalize_event_date(event_date)
                    if normalized_date and start_date <= normalized_date <= end_date:
                        filtered_events.append(event)
                
                if filtered_events:
                    # Filtrelenmiş etkinliklerle yeni RAG Engine oluştur
                    rag_engine = RAGEngine(filtered_events)
            
            # RAG Engine ile yanıt üret (TF-IDF ile en alakalı etkinlikleri bulur)
            top_k = 10 if "hangi etkinlik" in user_msg_lower or "ne yapabiliriz" in user_msg_lower else 5
            result = rag_engine.answer_question(user_msg, city_filter=city, top_k=top_k)
            
            response = result['answer']
            context_events = result['sources']
            
            # Yanıt yoksa fallback
            if not response:
                raise Exception("RAG Engine yanıt vermedi")
            
            # Yanıttaki etkinlik numaralarına link ekle
            import re
            pattern = r'([•\d]+)\.\s+([^\n-]+?)(?:\s*-|$)'
            
            def add_links(match):
                prefix = match.group(1)
                title = match.group(2).strip()
                
                num_match = re.search(r'\d+', prefix)
                if num_match:
                    idx = int(num_match.group()) - 1  # 0-indexed
                    if 0 <= idx < len(context_events):
                        event = context_events[idx]
                        url = event.get('url')
                        if url:
                            return f'{prefix}. <a href="{url}" target="_blank" style="color:#0d9488;text-decoration:underline;">{title}</a>'
                
                return match.group(0)  # Değiştirme yapma
            
            response = re.sub(pattern, add_links, response)
            
            return response
            
        except Exception as e:
            print(f"⚠️ LLM hatası, fallback'e geçiliyor: {e}")
            # LLM hata verirse eski sisteme dön
            use_llm = False
    
    # Eski regex tabanlı sistem (fallback)
    
    # Tarih aralığı çıkar
    start_date, end_date = BaseEventScraper.parse_turkish_date_query(user_msg)
    
    if city and start_date:
        all_city_events = manager.get_events_by_city(city)
        
        # Tarih filtreleme
        filtered_events = []
        for event in all_city_events:
            event_date = event.get('date', '')
            normalized_date = BaseEventScraper.normalize_event_date(event_date)
            
            if normalized_date:
                if start_date <= normalized_date <= end_date:
                    filtered_events.append(event)
        
        if filtered_events:
            if start_date == end_date:
                msg = f"<b>{city}</b>'de {start_date} için bulduğum etkinlikler:<br>"
            else:
                msg = f"<b>{city}</b>'de {start_date} - {end_date} arasında bulduğum etkinlikler:<br>"
            
            for i, event in enumerate(filtered_events, 1):
                url = event.get('url')
                title = event['title']
                location = event.get('location', '')
                date = event.get('date', '')
                if url:
                    msg += f"{i}. <a href='{url}' target='_blank'><b>{title}</b></a> - {location} - {date}<br>"
                else:
                    msg += f"{i}. <b>{title}</b> - {location} - {date}<br>"
        else:
            msg = f"🔍 {city} için {start_date} - {end_date} arasında etkinlik bulunamadı.<br><br>"
            msg += "💡 <b>Alternatif öneriler:</b><br>"
            msg += "• Tarih aralığını genişletmeyi deneyin<br>"
            msg += "• 'Bu hafta sonu ne var?' gibi genel sorular sorun<br>"
            msg += "• Belirli etkinlik türü sorun (konser, tiyatro, sinema)"
    
    elif city:
        events = manager.get_events_by_city(city)
        if events:
            msg = f"<b>{city}</b>'de bulduğum tüm etkinlikler:<br>"
            for i, event in enumerate(events, 1):
                url = event.get('url')
                title = event['title']
                location = event.get('location', '')
                date = event.get('date', '')
                if url:
                    msg += f"{i}. <a href='{url}' target='_blank'><b>{title}</b></a> - {location} - {date}<br>"
                else:
                    msg += f"{i}. <b>{title}</b> - {location} - {date}<br>"
        else:
            msg = f"🔍 {city} için şu anda etkinlik bulunamadı.<br><br>"
            msg += "💡 <b>Neler deneyebilirsiniz:</b><br>"
            msg += "• 'Bu hafta sonu ne var?' sorusu sorun<br>"
            msg += "• Belirli tarih belirtin (örn: '25 Ekim'de ne var?')<br>"
            msg += "• Farklı etkinlik türü deneyin (konser, tiyatro, sinema)"
    
    else:
        msg = "Lütfen şehir belirtin. (örn: 'Kocaeli'deki etkinlikleri listeler misin?' veya '19 ekimde Sakarya'da ne var?')"
    
    return msg

# Kişiselleştirme modalı
if 'registered' not in st.session_state:
    st.session_state['registered'] = False
    st.session_state['name'] = ''
    st.session_state['email'] = ''

if not st.session_state['registered']:
    # Modern Welcome Screen with Black Background
    st.markdown("""
    <style>
    /* Black Background for Welcome Screen */
    [data-testid="stAppViewContainer"] {
        background: #000000 !important;
    }
    
    .welcome-container {
        max-width: 500px;
        margin: 2em auto;
        padding: 2em 1.5em;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .form-container {
        max-width: 500px;
        margin: 0 auto;
    }
    
    .welcome-title {
        text-align: center;
        color: #ffffff;
        font-size: 3em;
        margin-bottom: 0.3em;
    }
    
    .welcome-heading {
        text-align: center;
        color: #ffffff;
        font-size: 2em;
        font-weight: 700;
        margin-bottom: 0.5em;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .welcome-subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.1em;
        margin-bottom: 2em;
        line-height: 1.6;
    }
    
    /* Modern Input Fields */
    .stTextInput input {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        padding: 0.8em 1em !important;
        font-size: 1em !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    .stTextInput input:focus {
        border-color: #667eea !important;
        background: rgba(255, 255, 255, 0.15) !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
    }
    
    .stTextInput label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 500 !important;
        margin-bottom: 0.5em !important;
    }
    
    /* Modern Buttons */
    .stButton button {
        border-radius: 12px !important;
        padding: 0.7em 2em !important;
        font-size: 1em !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        color: white !important;
    }
    
    button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
    }
    
    button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .welcome-footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.85em;
        margin-top: 2em;
        line-height: 1.5;
    }
    
    .welcome-footer a {
        color: #667eea;
        text-decoration: none;
        border-bottom: 1px solid rgba(102, 126, 234, 0.5);
    }
    </style>
    
    <div class="welcome-container">
        <div class="welcome-title">🎭</div>
        <div class="welcome-heading">Rotiva AI</div>
    </div>
    
    <div class="form-container">
    """, unsafe_allow_html=True)
    
    with st.form("register_form"):
        # İsim ve Mail tek kolon (full width)
        name = st.text_input("İsim", key="name_input", placeholder="👤 Adınız Soyadınız", label_visibility="collapsed")
        email = st.text_input("Mail", key="email_input", placeholder="� E-posta adresiniz", label_visibility="collapsed")
        
        # Butonlar yan yana
        col1, col2 = st.columns(2, gap="medium")
        with col1:
            skip = st.form_submit_button("⚡ Atla", use_container_width=True, type="secondary")
        with col2:
            start = st.form_submit_button("🚀 Başla", use_container_width=True, type="primary")
        
        if skip or start:
            # Session state'i hemen güncelle (önce UI'yi değiştir)
            st.session_state['registered'] = True
            st.session_state['name'] = name if start else ''
            st.session_state['email'] = email if start else ''
            
            # Google Sheets'e kaydet (arka planda, hata olsa bile devam et)
            try:
                import threading
                def save_to_sheets():
                    try:
                        sheets_manager = SheetsManager()
                        sheets_manager.save_user(
                            name=name if start else "",
                            email=email if start else "",
                            skip=skip
                        )
                    except Exception as e:
                        print(f"⚠️ Google Sheets kayıt hatası: {e}")
                
                # Arka planda çalıştır (UI beklemez)
                thread = threading.Thread(target=save_to_sheets, daemon=True)
                thread.start()
            except Exception as e:
                print(f"⚠️ Threading hatası: {e}")
            
            st.rerun()
    
    st.markdown("""
    </div>
    
    <div class="welcome-footer">
        Devam ederek <a href="https://docs.google.com/document/d/1e8qdxTzl7GgDy-Bg67ENnVXcw_jKURp-LkcTl69iMDA/edit?usp=sharing" target="_blank">Gizlilik Politikası</a> ve <a href="https://docs.google.com/document/d/1Fh9_sI6rR1c_bR4ZxCuW-S3olKfqtvfPuoUSTu9UTno/edit?usp=sharing" target="_blank">Kullanım Şartları</a>'nı kabul etmiş sayılırsınız.
    </div>
    """, unsafe_allow_html=True)
    
else:
    # Modern Header
    st.markdown('''
    <div class="header">
        <div class="header-title">🎭 Rotiva AI <span style="font-size: 0.5em; font-weight: 400; opacity: 0.9;">Etkinlikleri Senin İçin Keşfeder.</span></div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Sidebar - Modern Ayarlar
    with st.sidebar:
        # Sidebar Logo/Title (Fixed)
        st.markdown('''
        <div style="text-align: center; padding: 1.5em 0 1em 0; border-bottom: 1px solid rgba(255,255,255,0.2); margin-bottom: 1.5em;">
            <div style="font-size: 2.5em; margin-bottom: 0.2em;">🎭</div>
            <div style="font-size: 1.4em; font-weight: 700; color: #ffffff;">Rotiva AI</div>
            <div style="font-size: 0.85em; opacity: 0.7; margin-top: 0.3em;">Etkinlik Asistanınız</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # RAG + AI her zaman aktif (kullanıcı seçimi yok)
        use_llm = True  # Her zaman RAG + AI kullan
        
        # AI Badge - Kullanıcıya RAG+AI'ın aktif olduğunu bildir
        st.markdown('''
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 0.8em; border-radius: 10px; text-align: center; margin-bottom: 1em;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="font-size: 0.9em; font-weight: 600; color: white;">
                🤖 RAG + AI Aktif
            </div>
            <div style="font-size: 0.75em; color: rgba(255,255,255,0.8); margin-top: 0.3em;">
                Gemini 2.5 Flash + FAISS + Embeddings
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Modern Stats
        st.markdown("<br>", unsafe_allow_html=True)
        try:
            manager = EventManager(use_cache=True)
            all_events = manager.get_all_events()
            kocaeli_count = len([e for e in all_events if e.get('city', '').lower() == 'kocaeli'])
            sakarya_count = len([e for e in all_events if e.get('city', '').lower() == 'sakarya'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📍 Toplam", len(all_events))
            with col2:
                st.metric("🏙️ Kocaeli", kocaeli_count)
            with col3:
                st.metric("🌊 Sakarya", sakarya_count)
        except:
            pass
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("Her gece 03:00 güncelleme")
        st.markdown("Gemini 2.5 Flash")
    
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    
    # Modern Karşılama Mesajı
    if len(st.session_state['chat_history']) == 0:
        greet = f"Hey! 👋 Ben Rotiva AI, şehrinin etkinlik rehberiyim.<br><br>Kocaeli ve Sakarya'daki konserlerden tiyatrolara kadar her şeyi senin için bulurum.<br>Sadece ne istediğini söyle:<br><br>💞 \"Romantik bir akşam için öneri ver.\"<br>🎬 \"Bugün sinemada ne var?\"<br>👨‍👩‍👧 \"Çocuklarla gidilebilecek bir şey öner.\"<br><br>Hadi başlayalım mı? ✨" if not st.session_state['name'] else f"Hey {st.session_state['name']}! 👋 Ben Rotiva AI, şehrinin etkinlik rehberiyim.<br><br>Kocaeli ve Sakarya'daki konserlerden tiyatrolara kadar her şeyi senin için bulurum.<br>Hangi şehirde ve ne zaman bir şeyler yapmak istersin?"
        st.session_state['chat_history'].append({'role':'bot','msg':greet, 'time': datetime.now().strftime('%H:%M')})
    
    # Modern Chat Bubbles
    # Chat History Container (scrollable)
    chat_container = st.container()
    with chat_container:
        for chat in st.session_state['chat_history']:
            ts = chat.get('time', '')
            if chat['role']=='user':
                st.markdown(f'''
                <div class='user-wrap'>
                    <div class='msg-row' style='flex-direction: row-reverse;'>
                        <div class='avatar avatar-user'>👤</div>
                        <div>
                            <div class='user-bubble'>{chat['msg']}</div>
                            <div class='timestamp' style='text-align: right;'>{ts}</div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class='bot-wrap'>
                    <div class='msg-row'>
                        <div class='avatar avatar-bot'>🤖</div>
                        <div>
                            <div class='bot-bubble'>{chat['msg']}</div>
                            <div class='timestamp'>{ts}</div>
                        </div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
    
    # Loading indicator placeholder (üstte gösterilecek)
    loading_placeholder = st.empty()
    
    # Modern Input Area
    st.markdown("<br>", unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        user_msg = st.text_input(
            "chat_label",
            key="chat_input", 
            placeholder="💬 Mesajınızı yazın... (Örn: Romantik bir akşam planla Sakarya'da)",
            label_visibility="collapsed"
        )
        submitted = st.form_submit_button("📤 Gönder", use_container_width=True)
        if submitted and user_msg.strip():
            tnow = datetime.now().strftime('%H:%M')
            st.session_state['chat_history'].append({'role':'user','msg':user_msg, 'time':tnow})
            
            # Show loading at top
            with loading_placeholder:
                with st.spinner('🤖 Rotiva AI düşünüyor...'):
                    bot_msg = get_bot_response(user_msg, st.session_state['name'], use_live=False, use_rag=use_llm)
            
            st.session_state['chat_history'].append({'role':'bot','msg':bot_msg, 'time':datetime.now().strftime('%H:%M')})
            loading_placeholder.empty()  # Clear loading indicator
            st.rerun()
    
    # Footer with links
    st.markdown("""
    <div style="text-align: center; margin-top: 3em; padding: 2em 0; border-top: 1px solid rgba(255,255,255,0.2);">
        <p style="color: rgba(255,255,255,0.7); font-size: 0.9em; margin-bottom: 1em;">
            © 2025 Rotiva AI - Etkinlikleri Senin İçin Keşfeder
        </p>
        <div style="display: flex; justify-content: center; gap: 2em;">
            <a href="https://docs.google.com/document/d/1e8qdxTzl7GgDy-Bg67ENnVXcw_jKURp-LkcTl69iMDA/edit?usp=sharing" target="_blank" style="color: #667eea; text-decoration: none; font-size: 0.95em;">
                🔒 Gizlilik Politikası
            </a>
            <a href="https://docs.google.com/document/d/1Fh9_sI6rR1c_bR4ZxCuW-S3olKfqtvfPuoUSTu9UTno/edit?usp=sharing" target="_blank" style="color: #667eea; text-decoration: none; font-size: 0.95em;">
                📜 Kullanım Şartları
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
