import streamlit as st
import os
import google.generativeai as genai

# -------------------------
# 1. FLAGSHIP LUXURY CSS
# -------------------------
st.set_page_config(page_title="Tatcha Ritual Consultant", page_icon="💜", layout="wide")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9)), 
                    url('https://www.tatcha.com/on/demandware.static/-/Library-Sites-TatchaSharedLibrary/default/dw4b2e1e32/images/hero/HP_Desktop_Hero.jpg');
        background-size: cover;
    }
    .product-box {
        background: white;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        border: 1px solid #F0F0F0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .price-tag { color: #613082; font-weight: 600; }
    /* Fix for chat container contrast */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.6) !important;
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------
# 2. BRAND HEADER
# -------------------------
st.markdown("<h1 style='text-align: center; font-size: 3rem;'>TATCHA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; letter-spacing: 3px; color: #613082;'>JAPANESE BOTANICAL RITUALS</p>", unsafe_allow_html=True)

# -------------------------
# 3. LAYOUT & DATA
# -------------------------
products = [
    {"name": "The Dewy Skin Cream", "price": "$72", "icon": "💜", "label": "Rich Hydration"},
    {"name": "The Water Cream", "price": "$72", "icon": "💎", "label": "Pore Refining"},
    {"name": "The Rice Wash", "price": "$40", "icon": "☁️", "label": "Gentle Polish"},
    {"name": "The Essence", "price": "$110", "icon": "✨", "label": "Resurfacing"}
]

left_side, right_side = st.columns([1.2, 1], gap="large")

with left_side:
    st.markdown("### Curated Formulations")
    # Grid Logic
    p_col1, p_col2 = st.columns(2)
    
    for i, p in enumerate(products):
        target = p_col1 if i % 2 == 0 else p_col2
        with target:
            # THIS IS THE SECTION THAT WAS CAUSING THE SYNTAX ERROR - FIXED INDENTATION:
            st.markdown(f"""
            <div class="product-box">
                <div style="font-size: 40px;">{p['icon']}</div>
                <div style="font-size: 10px; color: #888; text-transform: uppercase;">{p['label']}</div>
                <div style="font-size: 16px; margin: 10px 0;">{p['name']}</div>
                <div class="price-tag">{p['price']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Consult on {p['name']}", key=f"btn_{i}", use_container_width=True):
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                st.session_state.messages.append({"role": "user", "content": f"Tell me more about {p['name']}"})

with right_side:
    st.markdown("### Ritual Consultant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_display = st.container(height=450, border=True)
    
    with chat_display:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"], avatar="💜" if msg["role"] == "assistant" else None):
                st.markdown(msg["content"])

    if prompt
