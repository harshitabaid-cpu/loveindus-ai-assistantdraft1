# streamlit_app.py
import streamlit as st
import os
import google.generativeai as genai

# -------------------------
# 1. FLAGSHIP LUXURY CSS
# -------------------------
st.set_page_config(page_title="Tatcha Ritual Consultant", page_icon="💜", layout="wide")

st.markdown("""
<style>
    /* Full Page Aesthetic */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9)), 
                    url('https://www.tatcha.com/on/demandware.static/-/Library-Sites-TatchaSharedLibrary/default/dw4b2e1e32/images/hero/HP_Desktop_Hero.jpg');
        background-size: cover;
    }

    /* Modern Floating Chat Container */
    [data-testid="stVerticalBlock"] > div:has(div.chat-container) {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 30px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.5);
    }

    /* Product Cards - Luxury Minimalist */
    .product-box {
        background: white;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        border: 1px solid #F0F0F0;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .product-box:hover {
        box-shadow: 0 15px 30px rgba(97, 48, 130, 0.1);
        transform: scale(1.02);
        border-color: #613082;
    }

    /* Typography */
    h1, h2, h3 { font-family: 'Playfair Display', serif; font-weight: 400 !important; color: #1A1A1A; }
    .price-tag { color: #613082; font-family: 'Inter', sans-serif; font-weight: 600; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

# -------------------------
# 2. HERO SECTION
# -------------------------
st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-bottom: 0;'>TATCHA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; letter-spacing: 4px; color: #613082; text-transform: uppercase; font-size: 0.8rem; margin-bottom: 50px;'>The Beauty of Mindfulness</p>", unsafe_allow_html=True)

# -------------------------
# 3. DYNAMIC TWO-COLUMN LAYOUT
# -------------------------
left_side, right_side = st.columns([1.2, 1], gap="large")

with left_side:
    st.markdown("### Curated for Your Ritual")
    st.write("Our formulations are rooted in Hadasei-3™, a trinity of anti-aging Japanese superfoods.")
    
    # Grid of Products
    p_row1_col1, p_row1_col2 = st.columns(2)
    
    products = [
        {"name": "The Dewy Skin Cream", "price": "$72", "icon": "💜", "label": "Rich Hydration"},
        {"name": "The Water Cream", "price": "$72", "icon": "💎", "label": "Pore Refining"},
        {"name": "The Rice Wash", "price": "$40", "icon": "☁️", "label": "Gentle Polish"},
        {"name": "The Essence", "price": "$110", "icon": "✨", "label": "Resurfacing"}
    ]

    # Displaying products in a 2x2 grid
    for i, p in enumerate(products):
        target_col = p_row1_col1 if i % 2 == 0 else p_row1_col2
        with target_col:
            st.markdown(f"""
            <div class="product-box">
                <div style="font-size: 40px; margin-bottom: 15px;">{p['icon']}</div>
