import streamlit as st
import os
import google.generativeai as genai
from datetime import datetime

# ---------------------------------------------------------
# CONFIGURATION: CHANGE BRAND NAME HERE
# ---------------------------------------------------------
BRAND_NAME = "Tatcha" 
BRAND_LOGO_URL = "https://tatcha.com/on/demandware.static/-/Library-Sites-TatchaSharedLibrary/default/dw106093d5/images/logo-black.png"
ACCENT_COLOR = "#613082" # Tatcha Purple

# ---------------------------------------------------------
# UI SETUP & REP-STYLE CSS
# ---------------------------------------------------------
st.set_page_config(page_title=f"{BRAND_NAME} Concierge", layout="centered")

st.markdown(f"""
<style>
    /* REP Widget Shell */
    [data-testid="stVerticalBlock"] > div:has(div.rep-container) {{
        max-width: 420px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        margin: auto;
        overflow: hidden;
        border: 1px solid #E0E0E0;
    }}

    /* THE REP HEADER (Black High-Contrast) */
    .rep-header {{
        background-color: #000000;
        color: white;
        padding: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .header-left {{ display: flex; align-items: center; }}
    .rep-icon {{
        width: 45px; height: 45px; background: white; border-radius: 50%;
        display: flex; align-items: center; justify-content: center; margin-right: 15px;
    }}
    .header-titles h3 {{ margin: 0; font-size: 18px; font-weight: 500; color: white; }}
    .header-titles p {{ margin: 0; font-size: 13px; color: #AAA; }}

    /* REP Message Area */
    .stChatMessage {{ background: transparent !important; border: none !important; }}
    .timestamp {{ font-size: 10px; color: #BBB; float: right; margin-top: -15px; }}
    
    /* Automated Reply Pill Buttons */
    div.stButton > button {{
        border-radius: 20px !important;
        border: 1px solid #CCC !important;
        background: white !important;
        color: #333 !important;
        font-size: 13px !important;
        margin-bottom: 8px;
        width: 100%;
    }}
    
    /* THE PILL INPUT */
    .stChatInputContainer {{
        border-radius: 30px !important;
        background-color: #F2F2F2 !important;
        border: none !important;
        padding: 5px 15px !important;
    }}

    /* Powered by REP Footer */
    .rep-footer {{
        text-align: center; font-size: 10px; color: #CCC; 
        letter-spacing: 2px; padding: 15px 0; text-transform: uppercase;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# THE WIDGET CONTENT
# ---------------------------------------------------------
st.markdown("<div class='rep-container'>", unsafe_allow_html=True)

# 1. HEADER
st.markdown(f"""
<div class="rep-header">
    <div class="header-left">
        <div class="rep-icon"><img src="{BRAND_LOGO_URL}" width="30"></div>
        <div class="header-titles">
            <h3>{BRAND_NAME} Concierge</h3>
            <p>Here to help you shop</p>
        </div>
    </div>
    <div style="font-size: 20px; opacity: 0.7;">⤢ &nbsp; ✕</div>
</div>
""", unsafe_allow_html=True)

# 2. AI LOGIC
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key: genai.configure(api_key=api_key)

def get_response(prompt, history):
    context = f"You are the {BRAND_NAME} Concierge. Use a sophisticated, expert Japanese beauty tone. Data: The Dewy Skin Cream (Dry skin, $72), The Water Cream (Oily skin, $72), Hadasei-3 (fermented superfoods). End with a follow-up question."
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        res = model.generate_content(f"{context} \n {history} \n User: {prompt}")
        return res.text
    except: return "I am refining our archives. One moment."

# 3. CHAT DISPLAY
if "messages" not in st.session_state: st.session_state.messages = []

chat_h = st.container(height=400, border=False)
with chat_h:
    # CONSULTATION STARTERS (If chat is empty)
    if not st.session_state.messages:
        st.write(f"Welcome. Which {BRAND_NAME} ritual may I assist you with?")
        col1, col2 = st.columns(2)
        if col1.button("💜 Dewy vs. Water Cream?"):
            st.session_state.messages.append({"role": "user", "content": "What is the difference between the Dewy Skin Cream and the Water Cream?"})
            st.rerun()
        if col2.button("☁️ Rice Wash or Deep Cleanse?"):
            st.session_state.messages.append({"role": "user", "content": "Should I use The Rice Wash or The Deep Cleanse?"})
            st.rerun()
        if st.button("✨ Tell me about Hadasei-3™"):
            st.session_state.messages.append({"role": "user", "content": "What makes Tatcha's Hadasei-3 complex special?"})
            st.rerun()

    for m in st.session_state.messages:
        avatar = BRAND_LOGO_URL if m["role"] == "assistant" else None
        with st.chat_message(m["role"], avatar=avatar):
            st.markdown(m["content"])
            st.markdown(f"<div class='timestamp'>{datetime.now().strftime('%H:%M %p')}</div>", unsafe_allow_html=True)

# 4. INPUT PILL
if prompt := st.chat_input("Type anything here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_h:
        with st.chat_message("assistant", avatar=BRAND_LOGO_URL):
            ans = get_response(prompt, st.session_state.messages[:-1])
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
    st.rerun()

st.markdown("<div class='rep-footer'>Powered by REP</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
