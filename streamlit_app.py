import streamlit as st
import os
import google.generativeai as genai

BRAND_NAME = "Tatcha"
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

st.set_page_config(page_title=f"{BRAND_NAME} Concierge", layout="centered")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300&family=Jost:wght@300;400;500&display=swap" rel="stylesheet"/>
<style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background-color: #f5f0eb !important;
        font-family: 'Jost', sans-serif !important;
    }
    #MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }

    [data-testid="stMain"] > div {
        max-width: 500px;
        margin: 0 auto;
        padding: 1.5rem 1rem 1rem;
    }

    /* ── HEADER ── */
    .rep-header {
        background-color: #1a120b;
        padding: 14px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-radius: 3px 3px 0 0;
    }
    .header-titles h3 {
        margin: 0;
        font-family: 'Jost', sans-serif;
        font-size: 17px;
        font-weight: 500;
        letter-spacing: 0.06em;
        color: white;
    }
    .header-titles p {
        margin: 2px 0 0;
        font-family: 'Jost', sans-serif;
        font-size: 12px;
        font-weight: 300;
        color: #c4a882;
    }
    .header-icons { display: flex; gap: 15px; font-size: 15px; opacity: 0.6; color: white; }

    /* ── CHAT MESSAGES ── */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        padding: 4px 4px !important;
        border: none !important;
    }
    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarAssistant"] { display: none !important; }

    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        flex-direction: row-reverse !important;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p {
        font-family: 'Jost', sans-serif !important;
        font-size: 14px !important;
        font-weight: 300 !important;
        line-height: 1.6 !important;
        color: #f5ede3 !important;
        background: #1a120b !important;
        border-radius: 12px 2px 12px 12px !important;
        padding: 10px 14px !important;
        display: inline-block !important;
        max-width: 84% !important;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) p,
    .assistant-text {
        font-family: 'Jost', sans-serif !important;
        font-size: 14px !important;
        font-weight: 300 !important;
        line-height: 1.6 !important;
        color: #1a120b !important;
        background: #ffffff !important;
        border: 1px solid rgba(160,120,80,0.18) !important;
        border-radius: 2px 12px 12px 12px !important;
        padding: 10px 14px !important;
        display: inline-block !important;
        max-width: 84% !important;
    }

    /* ── CHIP BUTTONS — fix: inline row, compact, no stacking ── */
    div.stButton > button {
        font-family: 'Jost', sans-serif !important;
        font-size: 12px !important;
        font-weight: 400 !important;
        letter-spacing: 0.03em !important;
        border-radius: 20px !important;
        border: 1px solid rgba(160,120,80,0.35) !important;
        background: #fffdf9 !important;
        color: #7c5c3e !important;
        padding: 5px 14px !important;
        height: auto !important;
        white-space: nowrap !important;
        transition: all 0.18s !important;
    }
    div.stButton > button:hover {
        background: #9c7c5a !important;
        color: #fff !important;
        border-color: #9c7c5a !important;
    }

    /* fix: columns stay compact side-by-side */
    [data-testid="column"] {
        width: auto !important;
        flex: 0 0 auto !important;
        min-width: unset !important;
        padding: 0 4px 0 0 !important;
    }
    .stHorizontalBlock {
        flex-wrap: nowrap !important;
        gap: 0 !important;
        padding: 10px 0 6px !important;
        background: transparent !important;
        border: none !important;
        justify-content: flex-start !important;
    }

    /* ── INPUT ── */
    [data-testid="stChatInput"] textarea,
    .stChatInputContainer textarea {
        font-family: 'Jost', sans-serif !important;
        font-size: 13px !important;
        font-weight: 300 !important;
        color: #1a120b !important;
        direction: ltr !important;
        text-align: left !important;
        background: #fffdf9 !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #c4a882 !important;
    }
    [data-testid="stBottom"] {
        background: #fffdf9 !important;
        border-top: 1px solid rgba(160,120,80,0.15) !important;
        padding: 8px 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chips_done" not in st.session_state:
    st.session_state.chips_done = False

# ── AI ──
def get_genius_reply(query, history):
    context = (
        f"Role: Elite {BRAND_NAME} Concierge. Tone: Sophisticated, warm, brief. "
        f"Products: Dewy Skin Cream (rich, for dry skin), Water Cream (oil-free, for oily/combo), "
        f"Hadasei-3 (green tea + rice + algae complex), Rice Wash (gentle brightening cleanser). "
        f"Instructions: Answer in 2-3 sentences max."
    )
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history])
        response = model.generate_content(f"{context}\n{history_text}\nUser: {query}")
        return response.text
    except Exception:
        return "Our botanical experts are momentarily away. How may I assist your ritual today?"

# ── HEADER ──
st.markdown(f"""
<div class="rep-header">
    <div class="header-titles">
        <h3>{BRAND_NAME} Concierge</h3>
        <p>Here to help you shop</p>
    </div>
    <div class="header-icons"><span>⤢</span><span>✕</span></div>
</div>
""", unsafe_allow_html=True)

# ── CHAT AREA — dynamic height, no fixed large container ──
chat_area = st.container(height=400, border=False)
with chat_area:
    if not st.session_state.messages:
        st.markdown(
            "<p style='font-family:Jost,sans-serif;font-size:14px;font-weight:300;"
            "line-height:1.6;color:#7c5c3e;padding:4px 4px;'>"
            "Good afternoon. How shall we refine your ritual today?</p>",
            unsafe_allow_html=True
        )
    for m in st.session_state.messages:
        if m["role"] == "user":
            with st.chat_message("user", avatar=None):
                st.markdown(m["content"])
        else:
            with st.chat_message("assistant", avatar=None):
                st.markdown(
                    f"<div class='assistant-text'>{m['content']}</div>",
                    unsafe_allow_html=True
                )

# ── CHIPS — only shown before first message, all on one row ──
if not st.session_state.chips_done:
    chip_clicked = None
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("Dewy vs Water?", key="chip1"):
            chip_clicked = "What's the difference between the Dewy and Water Cream?"
    with c2:
        if st.button("Rice Wash?", key="chip2"):
            chip_clicked = "Tell me about the Rice Wash."
    with c3:
        if st.button("Hadasei-3?", key="chip3"):
            chip_clicked = "What is Hadasei-3?"

    if chip_clicked:
        st.session_state.chips_done = True
        st.session_state.messages.append({"role": "user", "content": chip_clicked})
        reply = get_genius_reply(chip_clicked, st.session_state.messages[:-1])
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

# ── INPUT ──
if prompt := st.chat_input("How may we assist your ritual today?"):
    st.session_state.chips_done = True
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_area:
        with st.chat_message("user", avatar=None):
            st.markdown(prompt)
        with st.chat_message("assistant", avatar=None):
            reply = get_genius_reply(prompt, st.session_state.messages[:-1])
            st.markdown(
                f"<div class='assistant-text'>{reply}</div>",
                unsafe_allow_html=True
            )
            st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
