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
# 2. DESIGN EXPERT CSS (FIXED SYNTAX & ALIGNMENT)
# ---------------------------------------------------------
st.set_page_config(page_title=f"{BRAND_NAME} Concierge", layout="centered")

# Use a standard string (no 'f') for CSS to avoid the curly brace error
st.markdown("""
<style>
    /* Main Widget Container */
    [data-testid="stVerticalBlock"] > div:has(div.luxury-widget) {
        max-width: 480px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: auto;
        overflow: hidden;
        border: 1px solid #EDEDED;
        display: flex;
        flex-direction: column;
    }

    /* SLIM HEADER */
    .rep-header {
        background-color: #000000;
        color: white;
        padding: 12px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .header-titles h3 { margin: 0; font-size: 26px !important; font-weight: 500; color: white; }
    .header-titles p { margin: 0; font-size: 16px !important; color: #AAA; font-weight: 300; }
    .header-icons { display: flex; gap: 15px; font-size: 20px; opacity: 0.8; }

    /* CHAT ALIGNMENT */
    [data-testid="stChatMessage"] {
        font-size: 21px !important;
        background: transparent !important;
        padding: 5px 20px !important;
    }
    
    /* User: Right Aligned */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        flex-direction: row-reverse !important;
        text-align: right !important;
    }
    [data-testid="stChatMessageAvatarUser"] { display: none !important; }

    /* Assistant: Left Aligned */
    .assistant-text { font-size: 21px !important; line-height: 1.4; color: #1A1A1A; }

    /* SUGGESTION CHIPS: Ultra-Compact & Right Above Input */
    div[data-testid="column"] {
        padding: 0 !important;
        margin: 0 !important;
        width: fit-content !important;
        flex: none !important;
    }
    
    .stHorizontalBlock {
        gap: 8px !important; 
        margin-bottom: -20px !important;
        padding: 0 20px !important;
    }
    
    div.stButton > button {
        border-radius: 20px !important;
        border: 1px solid #DDD !important;
        background: white !important;
        padding: 2px 10px !important;
        font-size: 16px !important;
        height: auto !important;
    }

    /* INPUT BAR: Right Aligned Text */
    .stChatInputContainer textarea {
        font-size: 20px !important;
        text-align: right !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. CONVERSATION LOGIC
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_genius_reply(query, history):
    context = f"Role: Elite {BRAND_NAME} Concierge. Tone: Sophisticated. Data: Dewy Skin Cream, Water Cream, Hadasei-3. Instructions: Short expert answers."
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"{context}\nHistory: {history}\nUser: {query}")
        return response.text
    except:
        return "Our botanical experts are currently refining the archives."

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
    <div class="header-icons"><span>⤢</span><span>✕</span></div>
</div>
""", unsafe_allow_html=True)

# CHAT HISTORY
chat_area = st.container(height=450, border=False)
with chat_area:
    if not st.session_state.messages:
        st.markdown("<div style='font-size:20px; padding:20px; color:#555;'>Good afternoon. How shall we refine your ritual today?</div>", unsafe_allow_html=True)
    
    for m in st.session_state.messages:
        if m["role"] == "user":
            with st.chat_message("user", avatar=None):
                st.markdown(f"<div style='font-size:21px;'>{m['content']}</div>", unsafe_allow_html=True)
        else:
            with st.chat_message("assistant", avatar="✨"):
                st.markdown(f"<div class='assistant-text'>{m['content']}</div>", unsafe_allow_html=True)

# COMPACT SUGGESTED REPLIES (Pinned Right Above Input)
c1, c2, c3 = st.columns([0.35, 0.3, 0.35])
with c1:
    if st.button("💜 Dewy vs Water?"):
        st.session_state.messages.append({"role": "user", "content": "Dewy vs Water Cream?"})
        st.rerun()
with c2:
    if st.button("☁️ Rice Wash?"):
        st.session_state.messages.append({"role": "user", "content": "Rice Wash ritual?"})
        st.rerun()
with c3:
    if st.button("✨ Hadasei-3?"):
        st.session_state.messages.append({"role": "user", "content": "What is Hadasei-3?"})
        st.rerun()

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
