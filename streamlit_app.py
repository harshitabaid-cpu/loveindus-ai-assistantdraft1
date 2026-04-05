import streamlit as st
import os
import google.generativeai as genai

# ---------------------------------------------------------
# 1. BRAIN CONFIG
# ---------------------------------------------------------
BRAND_NAME = "Tatcha"
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# ---------------------------------------------------------
# 2. DESIGN EXPERT CSS (1.5x FONT & ALIGNMENT)
# ---------------------------------------------------------
st.set_page_config(page_title=f"{BRAND_NAME} Concierge", layout="centered")

st.markdown(f"""
<style>
    /* Main Widget Container */
    [data-testid="stVerticalBlock"] > div:has(div.luxury-widget) {{
        max-width: 550px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.1);
        margin: auto;
        overflow: hidden;
        border: 1px solid #EDEDED;
        display: flex;
        flex-direction: column;
    }}

    /* HEADER: 1.5x FONT & NO LOGO */
    .rep-header {{
        background-color: #000000;
        color: white;
        padding: 40px 30px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .header-titles h3 {{ 
        margin: 0; font-size: 36px !important; font-weight: 500; color: white; 
    }}
    .header-titles p {{ 
        margin: 0; font-size: 22px !important; color: #AAA; font-weight: 300;
    }}
    .header-icons {{ display: flex; gap: 25px; font-size: 30px; opacity: 0.8; }}

    /* MESSAGE ALIGNMENT & 1.5x FONT */
    [data-testid="stChatMessage"] {{
        font-size: 21px !important;
        background: transparent !important;
    }}
    
    /* User: Right Aligned, No Icon */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
        flex-direction: row-reverse !important;
        text-align: right !important;
    }}
    [data-testid="stChatMessageAvatarUser"] {{
        display: none !important;
    }}

    /* Assistant: Left Aligned, Large Text */
    .assistant-text {{
        font-size: 21px !important;
        line-height: 1.6;
        color: #1A1A1A;
    }}

    /* SUGGESTED REPLIES (Bottom Most, Tight Spacing) */
    .bottom-starters {{
        padding: 10px 30px;
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: flex-start;
    }}
    div.stButton > button {{
        border-radius: 30px !important;
        border: 1px solid #CCC !important;
        background: white !important;
        padding: 8px 20px !important;
        font-size: 20px !important; /* 1.5x larger */
        transition: 0.3s;
    }}

    /* INPUT BAR: 1.5x FONT */
    .stChatInputContainer textarea {{
        font-size: 22px !important;
        padding: 15px !important;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. CONVERSATION LOGIC
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_genius_reply(query, history):
    context = f"Role: Elite {BRAND_NAME} Concierge. Tone: Sophisticated Japanese luxury. Data: Dewy Skin Cream ($72), Water Cream ($72), Hadasei-3 trinity. Instructions: Expert, short, warm answers."
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"{context}\nHistory: {history}\nUser: {query}")
        return response.text
    except:
        return "Our botanical experts are refining the archives. How may I assist your ritual journey?"

# ---------------------------------------------------------
# 4. THE UI WIDGET
# ---------------------------------------------------------
st.markdown("<div class='luxury-widget'>", unsafe_allow_html=True)

# HEADER
st.markdown(f"""
<div class="rep-header">
    <div class="header-titles">
        <h3>{BRAND_NAME} Concierge</h3>
        <p>Here to help you shop</p>
    </div>
    <div class="header-icons">
        <span>⤢</span>
        <span>✕</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Function to reset conversation (linked to a button inside the widget for stability)
if st.button("Reset Conversation", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# CHAT HISTORY
chat_area = st.container(height=450, border=False)
with chat_area:
    for m in st.session_state.messages:
        if m["role"] == "user":
            with st.chat_message("user", avatar=None):
                st.markdown(m["content"])
        else:
            with st.chat_message("assistant", avatar="✨"):
                st.markdown(f"<div class='assistant-text'>{m['content']}</div>", unsafe_allow_html=True)

# SUGGESTED REPLIES (Pinned to bottom-most)
st.markdown("<div class='bottom-starters'>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    if st.button("💜 Dewy vs Water?"):
        st.session_state.messages.append({"role": "user", "content": "What is the difference between Dewy and Water cream?"})
        st.rerun()
with c2:
    if st.button("☁️ Rice Wash?"):
        st.session_state.messages.append({"role": "user", "content": "Tell me about the Rice Cleansing Ritual."})
        st.rerun()
with c3:
    if st.button("✨ Hadasei-3?"):
        st.session_state.messages.append({"role": "user", "content": "What makes Hadasei-3 special?"})
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# INPUT BAR
if prompt := st.chat_input("How may we assist your ritual today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_area:
        with st.chat_message("assistant", avatar="✨"):
            reply = get_genius_reply(prompt, st.session_state.messages[:-1])
            st.markdown(f"<div class='assistant-text'>{reply}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
