# streamlit_app.py
import streamlit as st
import os
import google.generativeai as genai

# -------------------------
# 1. LUXURY CSS INJECTION
# -------------------------
st.set_page_config(page_title="Tatcha AI Ritual", page_icon="💜", layout="centered")

st.markdown("""
<style>
    /* Premium Font and Background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #FFFFFF;
    }

    /* Product Card Grid */
    .product-card {
        border: 1px solid #EAEAEA;
        border-radius: 4px;
        padding: 15px;
        text-align: center;
        background: #FFF;
        transition: all 0.3s ease;
    }
    .product-card:hover {
        border-color: #613082; /* Tatcha Purple */
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }

    /* Custom Chat Bubbles */
    .stChatMessage {
        border-radius: 15px !important;
        padding: 10px !important;
    }

    /* Hide Streamlit Header/Footer for clean look */
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------------
# 2. BRAND HEADER
# -------------------------
st.markdown("<h2 style='text-align: center; color: #613082; font-weight: 300;'>TATCHA</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 14px;'>Find your beginning. Discover your ritual.</p>", unsafe_allow_html=True)
st.divider()

# -------------------------
# 3. INTERACTIVE PRODUCT SHELF
# -------------------------
# We use columns to show products as a "Quick Shop" bar
p_cols = st.columns(3)

products = [
    {"name": "The Water Cream", "price": "$72", "icon": "💎"},
    {"name": "The Dewy Skin", "price": "$72", "icon": "💜"},
    {"name": "The Rice Wash", "price": "$40", "icon": "☁️"}
]

for i, p in enumerate(products):
    with p_cols[i]:
        st.markdown(f"""
        <div class="product-card">
            <div style="font-size: 30px; margin-bottom: 10px;">{p['icon']}</div>
            <div style="font-weight: 600; font-size: 13px;">{p['name']}</div>
            <div style="color: #613082; font-size: 12px;">{p['price']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Details", key=f"btn_{i}"):
             st.session_state.messages.append({"role": "user", "content": f"Tell me about {p['name']}"})
             # This triggers the AI in the next rerun

st.write("") # Spacer

# -------------------------
# 4. THE CONVERSATION HUB
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Create a clean, focused area for the chat
chat_box = st.container(height=400, border=True)

with chat_box:
    if not st.session_state.messages:
        st.markdown("<p style='text-align: center; color: #AAA; margin-top: 150px;'>Ask your consultant about your skin type or specific ingredients.</p>", unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        avatar = "💜" if message["role"] == "assistant" else "👤"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# -------------------------
# 5. INPUT & LOGIC
# -------------------------
if prompt := st.chat_input("Message your ritual consultant..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Rerunning manually to show the user message immediately in the box
    st.rerun()

# Processing logic (Triggered after a rerun if the last message is from user)
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with chat_box:
        with st.chat_message("assistant", avatar="💜"):
            with st.spinner("Refining recommendations..."):
                # Insert your get_ai_response() logic here
                # For now, a placeholder for the quota-limited AI:
                response = "In the tradition of Japanese beauty, we believe in purity. This formulation utilizes Hadasei-3 to restore a youthful glow. Shall I explain the application ritual?"
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
