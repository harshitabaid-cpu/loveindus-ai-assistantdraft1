import streamlit as st
import os
import google.generativeai as genai
from datetime import datetime

# ---------------------------------------------------------
# CONFIGURATION: CHANGE BRAND DATA HERE
# ---------------------------------------------------------
BRAND_NAME = "Tatcha" 
BRAND_LOGO_CDN = "https://tatcha.com/on/demandware.static/-/Library-Sites-TatchaSharedLibrary/default/dw106093d5/images/logo-black.png"
ACCENT_COLOR = "#613082" # Tatcha Purple

# ---------------------------------------------------------
# UI SETUP & POLISHED CSS
# ---------------------------------------------------------
# Constraining width to create a focused widget feel.
st.set_page_config(page_title=f"{BRAND_NAME} Concierge", layout="centered")

# Custom indentation and indents are vital for triple-quoted strings.
st.markdown(f"""
<style>
    /* 1. Main Widget Container (Glassmorphism Effect) */
    [data-testid="stVerticalBlock"] > div:has(div.ritual-widget) {{
        max-width: 440px;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.12);
        margin: auto;
        overflow: hidden;
        border: 1px solid #EAEAEA;
        padding: 0;
    }}

    /* 2. THE HEADER (High-Contrast & Large Fonts) */
    .ritual-header {{
        background-color: #000000;
        color: white;
        padding: 25px 20px; /* Increased padding */
        display: flex;
        align-items: center;
        width: 100%;
    }}
    .header-left-group {{ display: flex; align-items: center; }}
    .brand-avatar {{
        width: 50px; height: 50px; background: white; border-radius: 50%;
        display: flex; align-items: center; justify-content: center; margin-right: 18px;
    }}
    .header-titles h3 {{ 
        margin: 0; font-size: 22px !important; font-weight: 400; color: white; /* Large Headline */
    }}
    .header-titles p {{ 
        margin: 0; font-size: 16px !important; color: #BBB; margin-top: 4px; /* Large Subtitle */
    }}

    /* 3. The Conversation Greet & Starters Layout */
    .greet-and-start {{
        padding: 25px;
        border-bottom: 1px solid #F0F0F0;
    }}
    .tatcha-greet {{
        font-family: 'Times New Roman', Times, serif; /* Brand Serif feel */
        font-size: 19px; color: #1A1A1A; line-height: 1.4;
    }}

    /* Simplified Indentation for Pill Button Layout */
    .stColumn {{
        padding: 0 5px !important;
    }}
    div.stButton > button {{
        border-radius: 30px !important; /* Perfect Pill */
        border: 1px solid #D1D1D1 !important;
        background: white !important;
        color: #1A1A1A !important;
        font-size: 14px !important;
        width: 100%;
        text-align: left;
        padding: 10px 20px !important;
        margin-bottom: 5px;
    }}
    div.stButton > button:hover {{
        border-color: {ACCENT_COLOR} !important;
        color: {ACCENT_COLOR} !important;
    }}

    /* 4. Chat Area and Indentation */
    .stChatMessage {{ background: transparent !important; border: none !important; padding-top: 15px; }}
    [data-testid="stChatMessage"] div.stMarkdown {{
        background-color: rgba(97, 48, 130, 0.05); /* Soft purple tint */
        padding: 10px 15px; border-radius: 10px;
    }}
    .timestamp {{ font-size: 10px; color: #BBB; float: right; margin-top: -10px; padding-right: 10px; }}

    /* 5. Pill Input Pinned to Bottom */
    .stChatInputContainer {{
        border-radius: 30px !important;
        background-color: #F8F9FA !important;
        border: 1.5px solid #E0E0E0 !important;
        margin: 15px;
    }}
    .stChatInputContainer:focus-within {{
        border-color: {ACCENT_COLOR} !important;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# WIDGET CONSTRUCTION
# ---------------------------------------------------------
# A unique class to allow our CSS to target the entire container.
st.markdown("<div class='ritual-widget'>", unsafe_allow_html=True)

# --- THE HEADER INJECTION ---
# Pulling the brand logo and centering it with HTML/CSS
st.markdown(f"""
<div class="ritual-header">
    <div class="header-left-group">
        <div class="brand-avatar">
            <img src="{BRAND_LOGO_CDN}" width="35" alt="Tatcha Logo">
        </div>
        <div class="header-titles">
            <h3>{BRAND_NAME} Concierge</h3>
            <p>Here to help you shop</p>
        </div>
    </div>
    <div style="font-size: 20px; color: white; opacity: 0.6;">⤢ &nbsp; ✕</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# CONFIG & GENIUS BRAIN
# ---------------------------------------------------------
# Ensure indentation for the configuration block is standardized.
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key: genai.configure(api_key=api_key)

def get_polished_response(prompt, history):
    """Refined tone for the communication specialist's validation."""
    context = f"""
    You are the 'ritual consultant' for {BRAND_NAME}. 
    Use a calm, empathetic, mindful, and high-end Japanese beauty tone. 
    Never use aggressive sales language. 
    When discussing The Dewy Skin Cream, mention Japanese Purple Rice for hydration. 
    When discussing Hadasei-3™, mention Rice, Algae, and Green Tea as anti-aging superfoods.
    End with a considerate, consultative question.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        # History is injected here for continuity.
        response = model.generate_content(f"{context} \n {history} \n User Query: {prompt}")
        return response.text
    except:
        return "I am currently consulting our archives. Please allow me a moment to restore balance to your query."

# ---------------------------------------------------------
# CONVERSATION FLOW (Memory)
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- GREET & STARTERS BLOCK (If chat is empty) ---
# Fixing the layout and the communication tone.
if not st.session_state.messages:
    # Acknowledge the indents for nested HTML blocks.
    st.markdown("<div class='greet-and-start'>", unsafe_allow_html=True)
    
    # 1. Empathetic Communication Specialist Opening
    st.markdown("""
    <p class="tatcha-greet">
    Welcome to Tatcha. Find your beginning, and let us guide you.
    <br><br>
    Our botanical archives are open. Tell us about your skin’s journey, or allow us to recommend a ritual starter:
    </p>
    """, unsafe_allow_html=True)

    # 2. Corrected Starter Layout (Centered Columns)
    st.write("") # Spacer
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💜 Is my skin Dewy or Water?"):
            st.session_state.messages.append({"role": "user", "content": "I'm unsure if my skin needs The Dewy Skin Cream or The Water Cream."})
            st.rerun()
    with c2:
        if st.button("✨ What is the Hadasei-3 ritual?"):
            st.session_state.messages.append({"role": "user", "content": "Explain Tatcha's signature Hadasei-3 complex and why it is special."})
            st.rerun()
    
    st.markdown("<div style='text-align: center; width: 100%;'>", unsafe_allow_html=True)
    if st.button("☁️ The Rice Cleansing Ritual", key="quick_c3"):
        st.session_state.messages.append({"role": "user", "content": "Which Tatcha Rice cleanser is best for me?"})
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True) # Closing greet block

# --- Chat Display Area ---
chat_area = st.container(height=450, border=False)
with chat_area:
    for m in st.session_state.messages:
        # Standardize indents for nested control flow.
        # Showing the brand logo in bot replies
        avatar = BRAND_LOGO_CDN if m["role"] == "assistant" else None
        with st.chat_message(m["role"], avatar=avatar):
            st.markdown(m["content"])
            # Timestamp Indentation
            st.markdown(f"<div class='timestamp'>{datetime.now().strftime('%H:%M %p')}</div>", unsafe_allow_html=True)

# --- PILL INPUT & PROCESSING ---
if prompt := st.chat_input("How may we assist your ritual today?"):
    # Indentation for user message logic block
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Page Reruns to update the chat area with the user message immediately.
    
    # Indentation for bot message logic block
    with chat_area:
        with st.chat_message("assistant", avatar=BRAND_LOGO_CDN):
            with st.spinner("Consulting the archives..."):
                full_response = get_polished_response(prompt, st.session_state.messages[:-1])
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()

# No "Powered by REP" footer for this polished demo.
st.markdown("</div>", unsafe_allow_html=True) # Closing widget block
