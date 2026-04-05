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
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300&family=Jost:wght@300;400;500&display=swap" rel="stylesheet"/>
<style>
    /*
    ═══════════════════════════════════════════
    TYPE SCALE (consistent across all elements)
    ───────────────────────────────────────────
    Header brand name  : 17px / weight 500
    Header subtitle    : 12px / weight 300
    Chat bubbles       : 14px / weight 300 / line-height 1.6
    Welcome message    : 14px / weight 300
    Chip buttons       : 12px / weight 400
    Input placeholder  : 13px / weight 300
    ═══════════════════════════════════════════
    */

    /* ── GLOBAL ── */
    html, body, [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background-color: #f5f0eb !important;
        font-family: 'Jost', sans-serif !important;
    }
    #MainMenu, footer, header, [data-testid="stToolbar"] {
        visibility: hidden;
        display: none;
    }

    /* ── PAGE CENTERING ── */
    [data-testid="stMain"] > div {
        max-width: 500px;
        margin: 0 auto;
        padding: 2rem 1rem 1rem;
    }

    /* ── WIDGET CARD ── */
    [data-testid="stVerticalBlock"] > div:has(div.luxury-widget) {
        max-width: 480px;
        background: #fffdf9;
        border-radius: 3px;
        border: 1px solid rgba(160,120,80,0.18);
        margin: auto;
        overflow: hidden;
    }

    /* ── HEADER ── */
    .rep-header {
        background-color: #1a120b;
        padding: 14px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* FIX 1: header title was 26px — too large for a compact bar */
    .header-titles h3 {
        margin: 0;
        font-family: 'Jost', sans-serif !important;
        font-size: 17px !important;   /* was 26px */
        font-weight: 500 !important;
        letter-spacing: 0.06em;
        color: white;
    }

    /* FIX 2: header subtitle was 16px — should be smaller than title */
    .header-titles p {
        margin: 0;
        font-family: 'Jost', sans-serif !important;
        font-size: 12px !important;   /* was 16px */
        font-weight: 300 !important;
        color: #c4a882;
        margin-top: 2px;
    }

    .header-icons {
        display: flex;
        gap: 15px;
        font-size: 16px;
        opacity: 0.6;
    }

    /* ── CHAT CONTAINER ── */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        padding: 4px 20px !important;
        border: none !important;
    }

    /* hide default avatars */
    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }

    /* FIX 3: user bubble was 21px — far too large */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        flex-direction: row-reverse !important;
        text-align: right !important;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p {
        font-family: 'Jost', sans-serif !important;
        font-size: 14px !important;   /* was 21px */
        font-weight: 300 !important;
        line-height: 1.6 !important;
        color: #f5ede3 !important;
        background: #1a120b !important;
        border-radius: 12px 2px 12px 12px !important;
        padding: 10px 14px !important;
        display: inline-block !important;
        max-width: 84% !important;
    }

    /* FIX 4: assistant bubble also 21px — corrected to match user bubble */
    .assistant-text {
        font-family: 'Jost', sans-serif !important;
        font-size: 14px !important;   /* was 21px */
        font-weight: 300 !important;
        line-height: 1.6 !important;
        color: #1a120b !important;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) p {
        font-family: 'Jost', sans-serif !important;
        font-size: 14px !important;
        font-weight: 300 !important;
        line-height: 1.6 !important;
        color: #1a120b !important;
        background: #ffffff !important;
        border: 1px solid rgba(160,120,80,0.15) !important;
        border-radius: 2px 12px 12px 12px !important;
        padding: 10px 14px !important;
        display: inline-block !important;
        max-width: 84% !important;
    }

    /* ── CHIPS ── */
    [data-testid="column"] {
        width: fit-content !important;
        flex: unset !important;
        min-width: unset !important;
        padding: 0 3px !important;
    }
    .stHorizontalBlock {
        flex-wrap: wrap !important;
        gap: 0 !important;
        padding: 8px 17px 10px !important;
        background: #fffdf9;
        border-bottom: 1px solid rgba(160,120,80,0.1);
    }

    /* FIX 5: chip buttons were 16px — too large, chips should feel small */
    div.stButton > button {
        font-family: 'Jost', sans-serif !important;
        font-size: 12px !important;   /* was 16px */
        font-weight: 400 !important;
        letter-spacing: 0.03em !important;
        border-radius: 20px !important;
        border: 1px solid rgba(160,120,80,0.3) !important;
        background: transparent !important;
        color: #7c5c3e !important;
        padding: 5px 12px !important;
        height: auto !important;
        transition: all 0.18s !important;
    }
    div.stButton > button:hover {
        background: #9c7c5a !important;
        color: #fff !important;
        border-color: #9c7c5a !important;
    }

    /* FIX 6: input was 20px with direction:rtl (made text go backwards!) */
    .stChatInputContainer textarea,
    [data-testid="stChatInput"] textarea {
        font-family: 'Jost', sans-serif !important;
        font-size: 13px !important;   /* was 20px */
        font-weight: 300 !important;
        color: #1a120b !important;
        direction: ltr !important;    /* was rtl — this was a bug */
        text-align: left !important;  /* was right — another bug */
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #c4a882 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. CONVERSATION LOGIC  (unchanged)
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_genius_reply(query, history):
    context = f"Role: Elite {BRAND_NAME} Concierge. Tone: Sophisticated. Data: Dewy Skin Cream, Water Cream, Hadasei-3. Instructions: Short expert answers."
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history])
        response = model.generate_content(f"{context}\n{history_text}\nUser: {query}")
        return response.text
    except Exception:
        return "Our botanical experts are currently refining the archives. How may I assist your skin today?"

# ---------------------------------------------------------
# 4. THE UI WIDGET  (unchanged except welcome message size fix)
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
        # FIX 7: welcome message was 20px inline style — now matches bubble size
        st.markdown(
            "<div style='font-size:14px; font-family:Jost,sans-serif; "
            "font-weight:300; line-height:1.6; padding:16px 20px; color:#555;'>"
            "Good afternoon. How shall we refine your ritual today?</div>",
            unsafe_allow_html=True
        )
    for m in st.session_state.messages:
        if m["role"] == "user":
            with st.chat_message("user", avatar=None):
                st.markdown(m["content"])
        else:
            with st.chat_message("assistant", avatar="✨"):
                st.markdown(
                    f"<div class='assistant-text'>{m['content']}</div>",
                    unsafe_allow_html=True
                )

# SUGGESTION CHIPS
c1, c2, c3 = st.columns([0.33, 0.33, 0.33])
with c1:
    if st.button("Dewy vs Water?"):
        st.session_state.messages.append({"role": "user", "content": "Difference between Dewy and Water?"})
        st.rerun()
with c2:
    if st.button("Rice Wash?"):
        st.session_state.messages.append({"role": "user", "content": "Tell me about Rice Wash."})
        st.rerun()
with c3:
    if st.button("Hadasei-3?"):
        st.session_state.messages.append({"role": "user", "content": "What is Hadasei-3?"})
        st.rerun()

# INPUT BAR
if prompt := st.chat_input("How may we assist your ritual today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_area:
        with st.chat_message("assistant", avatar="✨"):
            reply = get_genius_reply(prompt, st.session_state.messages[:-1])
            st.markdown(
                f"<div class='assistant-text'>{reply}</div>",
                unsafe_allow_html=True
            )
            st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
