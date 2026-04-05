import streamlit as st
import os
import google.generativeai as genai
from streamlit_js_eval import streamlit_js_eval

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
    /* Main Widget */
    [data-testid="stVerticalBlock"] > div:has(div.luxury-widget) {{
        max-width: 500px;
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
        padding: 30px 25px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .header-titles h3 {{ 
        margin: 0; font-size: 33px !important; font-weight: 500; color: white; 
    }}
    .header-titles p {{ 
        margin: 0; font-size: 21px !important; color: #AAA; font-weight: 300;
    }}
    .header-icons {{ display: flex; gap: 20px; font-size: 24px; cursor: pointer; }}

    /* MESSAGE ALIGNMENT */
    [data-testid="stChatMessage"]:has(div[data-testid="stChatMessageContent"] > div > p) {{
        background: transparent !important;
    }}
    
    /* User: Right Aligned, No Icon */
    .st-emotion-cache-janm0z {{
        flex-direction: row-reverse !important;
        text-align: right !important;
    }}
    .st-emotion-cache-janm0z [data-testid="stChatMessageAvatar"] {{
        display: none !important;
    }}

    /* Assistant: Left Aligned, Vector Icon */
    .assistant-msg-text {{
        font-size: 21px !important;
        line-height: 1.5;
    }}

    /* SUGGESTED REPLIES (Bottom Most, Tight Spacing) */
    .bottom-starters {{
        padding: 5px 25px;
        display: flex;
        gap: 5px;
        justify-content: flex-start;
    }}
    div.stButton > button {{
        border-radius: 20px !important;
        border: 1px solid #DDD !important;
        background: white !important;
        padding: 4px 12px !important;
        font-size: 18px !important;
    }}

    /* INPUT BAR: 1.5x FONT */
    .stChatInputContainer textarea {{
        font-size: 21px !important;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. CONVERSATION LOGIC
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_genius_reply(query, history):
    context = f"Role: Elite {BRAND_NAME} Concierge. Tone: Sophisticated. Instructions: Short expert answers. Mention Hadasei-3."
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"{context}\nHistory: {history}\nUser: {query}")
        return response.text
    except:
        return "Our archives are refining. How may I assist your ritual?"

# ---------------------------------------------------------
# 4. THE UI WIDGET
# ---------------------------------------------------------
st.markdown("<div class='luxury-widget'>", unsafe_allow_html=True)

# HEADER
col_h1, col_h2 = st.columns([0.8, 0.2])
with st.container():
    st.markdown(f"""
    <div class="rep-header">
        <div class="header-titles">
            <h3>{BRAND_NAME} Concierge</h3>
            <p>Here to help you shop</p>
        </div>
        <div class="header-icons">
            <span id="expand-btn">⤢</span>
            <span id="close-btn">✕</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Functional Buttons using JS
if st.button("✕", key="close_logic", help="Reset Ritual"):
    st.session_state.messages = []
    st.rerun()

# CHAT HISTORY
chat_area = st.container(height=400, border=False)
with chat_area:
    for m in st.session_state.messages:
        role = m["role"]
        if role == "user":
            with st.chat_message("user", avatar=None):
                st.markdown(f"<div style='font-size:21px;'>{m['content']}</div>", unsafe_allow_html=True)
        else:
            # Assistant with Vector Icon
            with st.chat_message("assistant", avatar="✨"):
                st.markdown(f"<div class='assistant-msg-text'>{m['content']}</div>", unsafe_allow_html=True)

# SUGGESTED REPLIES (Pinned to bottom-most above input)
st.markdown("<div class='bottom-starters'>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    if st.button("💜 Dewy vs Water?"):
        st.session_state.messages.append({"role": "user", "content": "Dewy vs Water Cream?"})
        st.rerun()
with c2:
    if st.button("☁️ Rice Wash?"):
        st.session_state.messages.append({"role": "user", "content": "Tell me about Rice Wash."})
        st.rerun()
with c3:
    if st.button("✨ Hadasei-3?"):
        st.session_state.messages.append({"role": "user", "content": "What is Hadasei-3?"})
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# INPUT BAR
if prompt := st.chat_input("How may we assist your ritual today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_area:
        with st.chat_message("assistant", avatar="✨"):
            reply = get_genius_reply(prompt, st.session_state.messages[:-1])
            st.markdown(f"<div class='assistant-msg-text'>{reply}</div>", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
