import streamlit as st
import os
import google.generativeai as genai

# -------------------------
# 1. PAGE SETUP & CLONE CSS
# -------------------------
# 'centered' layout is key to constraining the width like a widget.
st.set_page_config(page_title="AI Concierge", page_icon="✨", layout="centered")

# --- ADVANCED CUSTOM CSS: The Visual Clone ---
# Meticulously aligning indentation for all nested CSS blocks
st.markdown("""
<style>
    /* 1. Overall Background (Light Gray like image) */
    .stApp {
        background-color: #F9F9FB;
    }
    
    /* 2. THE WIDGET CONTAINER (The Floating Box) */
    /* We use unique selectors to target the main content block */
    [data-testid="stVerticalBlock"] > div:has(div.concierge-widget) {
        max-width: 420px; /* Constraining width like a phone screen */
        height: 600px; /* Setting a fixed height for the widget */
        background: white;
        border-radius: 20px;
        box-shadow: 0 30px 60px rgba(0,0,0,0.1);
        margin: 50px auto; /* Centers it on screen */
        overflow: hidden; /* Ensures rounded corners on header */
        border: 1px solid #EDEDED;
        display: flex;
        flex-direction: column; /* Allows us to pin the input to the bottom */
    }

    /* 3. THE HEADER (Dark Gray Bar from image) */
    .chat-header {
        background-color: #6D6D6D; /* Exact dark gray */
        color: white;
        padding: 30px 25px; /* Increased padding */
        display: flex;
        align-items: center;
        width: 100%;
        box-sizing: border-box;
    }
    .header-text {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        margin-left: 20px;
    }
    .header-text h3 { margin: 0; color: white; font-weight: 500; font-size: 24px; } /* Increased size */
    .header-text p { margin: 0; color: #DEDEDE; font-size: 16px; font-weight: 300; margin-top: 5px; } /* Increased size */

    /* 4. Chat Area and History Indentation */
    .chat-history {
        flex-grow: 1; /* Pushes input down */
        overflow-y: auto; /* Allows history to scroll */
        padding: 20px 25px;
    }
    [data-testid="stChatMessage"] {
        border-radius: 0;
        border: none;
        padding-top: 15px;
        padding-bottom: 15px;
        border-bottom: 1px solid #F0F0F0;
    }

    /* 5. Input Indentation and position (Force Pinned to Bottom) */
    .stChatInputContainer {
        border-radius: 40px !important;
        padding: 10px 20px !important;
        background-color: white !important;
        border: 2px solid #DEDEDE !important;
        width: 380px !important;
        margin: 0 auto 30px auto !important; /* Pushes it to absolute bottom and centers */
    }
    .stChatInputContainer:focus-within {
        border-color: #6D6D6D !important;
    }

    /* 6. Quick Reply Button Indentation and layout */
    .quick-replies-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 10px;
    }
    div.quick-reply-button > button {
        border-radius: 40px !important;
        border: 1.5px solid #C0C0C0 !important;
        background-color: white !important;
        color: #333 !important;
        font-weight: 400;
        font-size: 14px;
        text-transform: none;
        margin-bottom: 12px;
        width: 320px !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------
# 2. MARKER FOR WIDGET CONTAINER
# -------------------------
# We start the widget with a unique HTML class so our CSS can target it.
st.markdown("<div class='concierge-widget'>", unsafe_allow_html=True)

# -------------------------
# 3. HEADER INJECTION
# -------------------------
# Replacing the blue heart with the circular Love, Indus brand logo.
# Update 'brand-logo.png' to your actual logo filename in your folder.
# Indentation for the HTML block
st.markdown("""
<div class="chat-header">
    <div style="width: 70px; height: 70px; border-radius: 50%; display: flex; align-items: center; justify-content: center; overflow: hidden; background-color: white;">
        <img src="/mount/src/loveindus-ai-assistantdraft1/brand-logo.png" style="width: 100%; height: auto;">
    </div>
    <div class="header-text">
        <h3>Love, Indus Concierge</h3>
        <p>Here to help you shop</p>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------
# 4. CHAT AREA & AI LOGIC
# -------------------------
# Indentation for the configuration block
# Configuration for Gemini AI (Keep your original code)
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Standardize indentation for the get_ai_response function
def get_ai_response(query):
    if not api_key: return "⚠️ API Key Missing."
    context = f"You are Love, Indus AI. Data: The Dewy Skin Cream: $72. Ingredients: Hadasei-3. Oily skin. Query: {query}" # Genius data context
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(context)
        return response.text
    except:
        return "⚠️ I'm resting (Rate Limit). Try again in 30s."

# Start of the Chat History logic
st.markdown("<div class='chat-history'>", unsafe_allow_html=True)

# Indentation for the initial prompt (if history is empty)
if not st.session_state.messages:
    # Adding quick automated reply options
    st.markdown("<div class='quick-replies-container'>", unsafe_allow_html=True)
    st.write("Share your concerns, or pick a starting point:")
    
    # Standard indentation for st.container in a side column layout
    q1_col, q1_btn_col, q1_col2 = st.columns([0.1, 1, 0.1])
    with q1_btn_col:
        # Automated Quick Reply 1
        st.markdown("<div class='quick-reply-button'>", unsafe_allow_html=True)
        if st.button("ⓘ Difference between Water & Dewy Cream?", key="quick_q1"):
             st.session_state.messages.append({"role": "user", "content": "Tell me difference between Water and Dewy cream?"})
             st.rerun()
        # Automated Quick Reply 2
        if st.button("✨ What is Hadasei-3?", key="quick_q2"):
             st.session_state.messages.append({"role": "user", "content": "What is Hadasei-3?"})
             st.rerun()
        # Automated Quick Reply 3
        if st.button("☁️ Recommend a product for oily skin", key="quick_q3"):
             st.session_state.messages.append({"role": "user", "content": "Recommend for oily skin"})
             st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Indentation for displaying message history
for msg in st.session_state.messages:
    # Showing the brand logo next to assistant responses
    avatar = "/mount/src/loveindus-ai-assistantdraft1/brand-logo.png" if msg["role"] == "assistant" else None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# 5. INPUT LOGIC (Force Pinned to Bottom)
# -------------------------
# The styled chat input pill bar
if prompt := st.chat_input("Type anything here..."):
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    # This triggers the page to rerun and process the Genius response
    
    # Indentation for the Genius interaction processing block
    with st.spinner("Refining ritual..."):
        # 2. Get Genius Response
        full_response = get_ai_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()

# Close the concierge widget container marker
st.markdown("</div>", unsafe_allow_html=True)
