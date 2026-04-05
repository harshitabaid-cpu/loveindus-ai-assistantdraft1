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
# 2. DESIGN EXPERT CSS
# ---------------------------------------------------------
st.set_page_config(page_title=f"{BRAND_NAME} Concierge", layout="centered")

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
    
    /* User: Right Aligned Content */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        flex-direction: row-reverse !important;
        text-align: right !important;
    }
    [data-testid="stChatMessageAvatarUser"] { display: none !important; }

    /* Assistant: Left Aligned Text */
    .assistant-text { font-size: 21px !important; line-height: 1.4; color: #1A1A1A; }

    /* SUGGESTION CHIPS: Ultra-Compact & Right Above Input */
    [data-testid="column"] {
        width: fit-content !important;
        flex: unset !important;
        min-width: unset !important;
        padding: 0 !important;
    }
    
    .stHorizontalBlock {
        gap: 6px !important; 
        margin-bottom: -32px !important; 
        padding: 0 20px !important;
        justify-content: flex-start !important;
    }
    
    div.stButton > button {
        border-radius: 20px !important;
        border: 1px solid #DDD !important;
        background: white !important;
        padding: 2px 8px !important;
        font-size: 16px !important;
        height: auto !important;
    }

    /* INPUT BAR: Right Aligned Text & RTL for Cursor */
    .stChatInputContainer textarea {
        font-size: 20px !important;
        text-align: right !important;
        direction: rtl !important;
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
        # Format history for context
        history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history])
        # FIX: Added the missing generate_content method call
        response = model.generate_content(f"{context}\n{history_text}\nUser: {query}")
        return response.text
    except Exception:
        return "Our botanical experts are currently refining the archives. How may I assist your skin today?"

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

# COMPACT SUGGESTED REPLIES
c1, c2, c3 = st.columns([0.33, 0.33, 0.33])
with c1:
    if st.button("💜 Dewy vs Water?"):
        st.session_state.messages.append({"role": "user", "content": "Difference between Dewy and Water?"})
        st.rerun()
with c2:
    if st.button("☁️ Rice Wash?"):
        st.session_state.messages.append({"role": "user", "content": "Tell me about Rice Wash."})
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
