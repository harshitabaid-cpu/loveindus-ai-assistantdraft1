import streamlit as st
import os
import google.generativeai as genai

# -------------------------
# 1. PAGE SETUP & CORE UI STYLING
# -------------------------
# We use 'centered' to constrain the app like a widget, not full width.
st.set_page_config(page_title="Luxe Concierge", page_icon="✨", layout="centered")

# --- CUSTOM CSS: Replicating the Screenshot & L'Oréal Aesthetic ---
st.markdown("""
<style>
    /* 1. Overall Background */
    .stApp {
        background: #F8F9FA;
    }
    
    /* 2. Constraining the app to feel like a widget */
    div.block-container {
        max-width: 500px;
        padding: 0;
        border: 1px solid #EDEDED;
        border-radius: 20px;
        background: white;
        margin-top: 50px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
        overflow: hidden; /* Important for rounded corners */
    }

    /* 3. The Top Header Bar (from image) */
    .chat-header {
        background-color: #6D6D6D; /* The specific dark gray from screenshot */
        color: white;
        padding: 20px 25px;
        display: flex;
        align-items: center;
        border-top-left-radius: 20px;
        border-top-right-radius: 20px;
    }
    .header-text {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        margin-left: 15px;
    }
    .header-text h3 { margin: 0; color: white; font-weight: 500; font-size: 18px; }
    .header-text p { margin: 0; color: #EDEDED; font-size: 13px; font-weight: 300; }

    /* 4. Product Card Styling (Minimalist) */
    [data-testid="stColumn"] {
        padding: 0 20px;
    }
    .product-details {
        text-align: left;
        padding: 20px 0;
    }
    .product-name {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 600;
        font-size: 16px;
        color: #1A1A1A;
        margin-bottom: 10px;
    }
    .product-price {
        font-size: 24px;
        font-weight: 700;
        color: #1A1A1A;
        margin-bottom: 20px;
    }

    /* 5. Modern Button Styling (Rounded & Outline) */
    .stButton > button {
        width: 100%;
        border-radius: 30px;
        font-weight: 400;
        text-transform: none;
        letter-spacing: normal;
        margin-bottom: 10px;
    }
    /* "Learn More" (Outline style) */
    .outline-button button {
        background-color: white !important;
        color: #1A1A1A !important;
        border: 1px solid #C0C0C0 !important;
    }
    /* "Consult" (Filled gray style) */
    .filled-button button {
        background-color: #6D6D6D !important;
        color: white !important;
        border: none !important;
    }

    /* 6. Text Area & Input (Pill Shape) */
    div.stTextArea textarea {
        border-radius: 30px !important;
        background-color: transparent !important;
        border: 1.5px solid #DEDEDE !important;
        padding: 10px 25px !important;
        font-size: 14px;
    }
    div.stTextArea textarea:focus {
        border-color: #6D6D6D !important;
        box-shadow: none !important;
    }
    
    /* 7. Chat Message Bubble Adjustments */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border-bottom: 1px solid #F0F0F0;
        border-radius: 0;
        padding-top: 15px;
        padding-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------
# 2. THE WIDGET HEADER
# -------------------------
# Custom HTML/CSS to mimic the screenshot
st.markdown("""
<div class="chat-header">
    <div style="width: 50px; height: 50px; background-color: #1200E4; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
        <span style="font-size: 24px;">👤</span>
    </div>
    <div class="header-text">
        <h3>AI Concierge</h3>
        <p>Here to help you shop</p>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------
# 3. CONVERSATION HUB (Hidden in Popover)
# -------------------------
# To mimic that a user clicks to enter chat, we use a popover
with st.popover("Open Chat Ritual", use_container_width=True):
    st.subheader("Mindful Ritual Chat")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_box = st.container(height=350, border=False)
    
    with chat_box:
        if not st.session_state.messages:
            st.write("Share your concerns, and we shall guide you.")
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"], avatar="✨" if msg["role"] == "assistant" else None):
                st.markdown(msg["content"])

    # Processing AI Logic
    def get_ai_response(query):
        if not api_key: return "⚠️ API Key Missing."
        context = f"TATCHA CONSULTANT: Users query is: {query}" # Your genius logic here
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(context)
            return response.text
        except:
            return "⚠️ Quota reached. Please try in 30s."

    # User Input Logic
    if prompt := st.chat_input("Message your ritual consultant..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_box:
            with st.chat_message("assistant", avatar="✨"):
                with st.spinner("Consulting..."):
                    answer = get_ai_response(prompt)
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

# -------------------------
# 4. DATA & PRODUCT DISCOVERY
# -------------------------
# Configuration for Gemini AI (Keep your original code)
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# The product we are showing in this "widget" example
featured_product = {
    "name": "The Dewy Skin Cream",
    "price": "$72",
    "ingredients": "Japanese Purple Rice, Algae, Hyaluronic Acid",
    "description": "Rich hydration for a healthy glow."
}

# --- Centered Product Display ---
# We use st.columns with wide side gaps to focus the product card in the center.
left_gap, prod_card, right_gap = st.columns([0.3, 1, 0.3])

with prod_card:
    # 1. Product Icon (Mimicking that photo placeholder)
    st.markdown(f"""
    <div style="background-color: #EEE; height: 200px; border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-top: 30px;">
        <span style="font-size: 80px;">💜</span>
    </div>
    <div class="product-details">
        <p class="product-name">{featured_product['name']}</p>
        <p class="product-price">{featured_product['price']}</p>
    </div>
    """, unsafe_allow_html=True)

    # 2. Buttons: Mimicking that outlined/filled combo from image
    st.markdown("<div class='outline-button'>", unsafe_allow_html=True)
    st.button("ⓘ  Learn More", key="learn_btn")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='filled-button'>", unsafe_allow_html=True)
    st.button("✨  Consult on Ritual", key="consult_btn")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# 5. INPUT & LOADER (Pill Shaped)
# -------------------------
st.markdown("<h4 style='text-align: center; color: #BBB; font-weight: 300; margin-top: 20px;'>Ask your question:</h4>", unsafe_allow_html=True)
user_query = st.text_area("Pill", key="quick_q", height=60, label_visibility="collapsed")
