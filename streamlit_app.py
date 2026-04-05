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
# 2. DESIGN EXPERT CSS (SLIM CHATBOX & 1.5x FONT)
# ---------------------------------------------------------
st.set_page_config(page_title=f"{BRAND_NAME} Concierge", layout="centered")

st.markdown(f"""
<style>
    /* Main Widget Container */
    [data-testid="stVerticalBlock"] > div:has(div.luxury-widget) {{
        max-width: 480px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: auto;
        overflow: hidden;
        border: 1px solid #EDEDED;
        display: flex;
        flex-direction: column;
    }}

    /* SLIM HEADER: Compact and Professional */
    .rep-header {{
        background-color: #000000;
        color: white;
        padding: 15px 20px; /* Reduced padding for slim look */
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .header-titles h3 {{ 
        margin: 0; font-size: 28px !important; font-weight: 500; color: white; 
    }}
    .header-titles p {{ 
        margin: 0; font-size: 18px !important; color: #AAA; font-weight: 300;
    }}
    .header-icons {{ display: flex; gap: 15px; font-size: 22px; opacity: 0.8; }}

    /* MESSAGE ALIGNMENT & 1.5x FONT */
    [data-testid="stChatMessage"] {{
        font-size: 21px !important;
        background: transparent !important;
        padding: 5px 20px !important;
    }}
    
    /* User: Force Right Alignment */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
        flex-direction: row-reverse !important;
        text-align: right !important;
    }}
    [data-testid="stChatMessageAvatarUser"] {{
        display: none !important;
    }}

    /* Assistant: Left Aligned with Large Text */
    .assistant-text {{
        font-size: 21px !important;
        line-height: 1.4;
        color: #1A1A1A;
    }}

    /* SUGGESTED REPLIES (Tight Spacing & Pinned to bottom) */
    .bottom-starters {{
        padding: 0px 20px 10px 20px;
        display: flex;
        gap: 8px !important; /* Reduced gap */
        justify-content: flex-start;
        flex-wrap: wrap;
    }}
    div.stButton > button {{
        border-radius: 20px !important;
        border: 1px solid #DDD !important;
        background: white !important;
        padding: 4px 12px !important;
        font-size: 18px !important;
        margin: 0 !important;
    }}

    /* INPUT BAR: Professional Scale */
    .stChatInputContainer textarea {{
        font-size: 20px !important;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. CONVERSATION LOGIC
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_genius_reply(query, history):
    context = f"Role: Elite {BRAND_NAME} Concierge. Tone: Sophisticated. Data: Dewy Skin Cream ($72), Water Cream ($72), Hadasei-3. Instructions: Short expert answers."
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"{context}\nHistory: {history}\nUser: {query}")
        return response.text
    except:
        return "I am refining our ritual archives. How may I assist your skin today?"

# ---------------------------------------------------------
# 4. THE UI WIDGET
# ---------------------------------------------------------
st.markdown("<div class='luxury-widget'>", unsafe_allow_html=True)

# SLIM HEADER
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

# CHAT HISTORY
chat_area = st.container(height=420, border=False)
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

# SUGGESTED REPLIES (Tight Spacing)
st.markdown("<div class='bottom-starters'>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1.1, 1, 1])
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
