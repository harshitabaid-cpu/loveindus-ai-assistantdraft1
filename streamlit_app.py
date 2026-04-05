import streamlit as st
import os
import google.generativeai as genai
from datetime import datetime

# ---------------------------------------------------------
# 1. BRAND ASSETS & GENIUS BRAIN CONFIG
# ---------------------------------------------------------
BRAND_NAME = "Tatcha"
# Using a high-quality verified logo URL
BRAND_LOGO = "https://www.tatcha.com/on/demandware.static/-/Library-Sites-TatchaSharedLibrary/default/dw106093d5/images/logo-black.png"
ACCENT_COLOR = "#613082" 

api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# ---------------------------------------------------------
# 2. DESIGN EXPERT CSS (Fixing Overlaps & Layout)
# ---------------------------------------------------------
st.set_page_config(page_title=f"{BRAND_NAME} Concierge", layout="centered")

st.markdown(f"""
<style>
    /* Global Widget Styling */
    [data-testid="stVerticalBlock"] > div:has(div.rep-clone) {{
        max-width: 450px;
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.15);
        margin: auto;
        overflow: hidden;
        border: 1px solid #F0F0F0;
    }}

    /* FIXED HEADER: No overlapping */
    .rep-header {{
        background-color: #000000;
        color: white;
        padding: 20px 25px;
        display: flex;
        align-items: center;
        justify-content: space-between; /* Keeps text left, icons right */
    }}
    .header-left {{ display: flex; align-items: center; flex: 1; }}
    .logo-container {{
        width: 55px; height: 55px; 
        background: white; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        margin-right: 15px; flex-shrink: 0;
    }}
    .header-text-group {{ display: flex; flex-direction: column; }}
    .header-text-group h3 {{ 
        margin: 0; font-size: 20px; font-weight: 500; color: white; line-height: 1.2;
    }}
    .header-text-group p {{ 
        margin: 0; font-size: 14px; color: #AAA; font-weight: 300;
    }}
    .header-icons {{ display: flex; gap: 15px; opacity: 0.8; font-size: 18px; cursor: pointer; }}

    /* SUGGESTION CHIPS (Suggested Response Options) */
    .chip-container {{
        display: flex; flex-wrap: wrap; gap: 8px; padding: 15px 25px;
    }}
    div.stButton > button {{
        border-radius: 20px !important;
        border: 1px solid #E0E0E0 !important;
        background: white !important;
        color: #444 !important;
        font-size: 13px !important;
        transition: 0.2s;
    }}
    div.stButton > button:hover {{
        border-color: {ACCENT_COLOR} !important;
        color: {ACCENT_COLOR} !important;
    }}

    /* CHAT BUBBLES */
    [data-testid="stChatMessage"] {{
        background: transparent !important;
        padding: 10px 20px !important;
    }}
    .stChatInputContainer {{
        border-radius: 30px !important;
        background: #F4F4F7 !important;
        border: 1px solid #E0E0E0 !important;
        margin: 10px 20px 25px 20px !important;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. CONVERSATION LOGIC
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_genius_reply(query, history):
    context = f"""
    Role: Elite {BRAND_NAME} Concierge.
    Tone: Sophisticated, warm, mindful, Japanese-inspired.
    Instructions: Give short, expert answers. Always mention the specific superfoods (Hadasei-3). 
    IMPORTANT: End your response by offering two specific paths (e.g. 'Would you like to know the ritual or see the results?')
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        full_prompt = f"{context}\nHistory: {history}\nUser: {query}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception:
        return "I am currently refining our botanical archives. How may I assist your skin's journey today?"

# ---------------------------------------------------------
# 4. THE WIDGET UI
# ---------------------------------------------------------
st.markdown("<div class='rep-clone'>", unsafe_allow_html=True)

# HEADER
st.markdown(f"""
<div class="rep-header">
    <div class="header-left">
        <div class="logo-container">
            <img src="{BRAND_LOGO}" width="35">
        </div>
        <div class="header-text-group">
            <h3>{BRAND_NAME} Concierge</h3>
            <p>Here to help you shop</p>
        </div>
    </div>
    <div class="header-icons">
        <span>⤢</span>
        <span onclick="window.location.reload()">✕</span>
    </div>
</div>
""", unsafe_allow_html=True)

# CHAT AREA
chat_placeholder = st.container(height=450, border=False)

with chat_placeholder:
    if not st.session_state.messages:
        # BRANDED WARM OPENING
        st.markdown(f"""
        <div style='padding: 20px; font-size: 17px; color: #333; font-family: serif;'>
        Good afternoon. Welcome to {BRAND_NAME}. <br><br>
        Find your beginning, and let us guide you. How shall we refine your ritual today?
        </div>
        """, unsafe_allow_html=True)
    
    for m in st.session_state.messages:
        avatar = BRAND_LOGO if m["role"] == "assistant" else None
        with st.chat_message(m["role"], avatar=avatar):
            st.markdown(m["content"])

# DYNAMIC SUGGESTION OPTIONS (Conversation Continuing)
st.markdown("<div class='chip-container'>", unsafe_allow_html=True)
cols = st.columns([1, 1, 1])
if not st.session_state.messages:
    if cols[0].button("💜 Dewy vs Water?"):
        st.session_state.messages.append({"role": "user", "content": "What is the difference between Dewy and Water cream?"})
        st.rerun()
    if cols[1].button("☁️ The Rice Wash?"):
        st.session_state.messages.append({"role": "user", "content": "Tell me about the Rice Cleansing Ritual."})
        st.rerun()
    if cols[2].button("✨ Hadasei-3?"):
        st.session_state.messages.append({"role": "user", "content": "What is the Hadasei-3 complex?"})
        st.rerun()
else:
    # Post-conversation chips to keep them shopping
    if cols[0].button("🛍️ View Rituals"):
        st.session_state.messages.append({"role": "user", "content": "Show me the full ritual sets."})
        st.rerun()
    if cols[1].button("🧴 Check Ingredients"):
        st.session_state.messages.append({"role": "user", "content": "I want to see the key ingredients again."})
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# INPUT BAR
if prompt := st.chat_input("How may we assist your ritual today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_placeholder:
        with st.chat_message("assistant", avatar=BRAND_LOGO):
            with st.spinner("Consulting..."):
                reply = get_genius_reply(prompt, st.session_state.messages[:-1])
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
