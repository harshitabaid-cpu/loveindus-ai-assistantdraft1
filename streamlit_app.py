# streamlit_app.py
import streamlit as st
import os
import google.generativeai as genai

# -------------------------
# 1. High-Fidelity UI/UX Styling
# -------------------------
st.set_page_config(page_title="Luxe AI Consultant", page_icon="✨", layout="wide")

st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Clean Title Styling */
    .main-title {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 200;
        color: #1a1a1a;
        letter-spacing: 2px;
        text-align: center;
        padding-bottom: 20px;
    }

    /* Product Card Styling */
    .product-holder {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        transition: transform 0.3s ease;
        margin-bottom: 20px;
    }
    .product-holder:hover {
        transform: translateY(-5px);
    }

    /* Assistant Message Styling */
    .stChatMessage {
        background-color: transparent !important;
    }
    
    /* Sidebar aesthetic */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# -------------------------
# 2. Configuration & State
# -------------------------
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Simulated Product Database
products = [
    {"name": "The Dewy Skin Cream", "price": "$72", "tag": "Hydrate", "desc": "Rich, plumping hydration.", "img": "💜"},
    {"name": "The Water Cream", "price": "$72", "tag": "Clarify", "desc": "Pore-refining, oil-free hydration.", "img": "💎"},
    {"name": "The Rice Wash", "price": "$40", "tag": "Cleanse", "desc": "Softening cream cleanser.", "img": "☁️"}
]

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# 3. Layout: Two-Column Interface
# -------------------------
st.markdown("<h1 class='main-title'>SKINCARE CONSULTANT </h1>", unsafe_allow_html=True)

# Main container for the layout
left_col, right_col = st.columns([1, 2], gap="large")

# --- LEFT COLUMN: The Product Shelf ---
with left_col:
    st.subheader("Your Personalized Shelf")
    for p in products:
        with st.container():
            st.markdown(f"""
            <div class="product-holder">
                <span style="font-size: 24px;">{p['img']}</span>
                <span style="float: right; color: #888;">{p['tag']}</span>
                <h4 style="margin: 10px 0 5px 0;">{p['name']}</h4>
                <p style="color: #444; font-size: 14px;">{p['desc']}</p>
                <strong style="font-size: 18px;">{p['price']}</strong>
            </div>
            """, unsafe_allow_html=True)
            # Add a small button to "ask" about it specifically
            if st.button(f"Ask about {p['name']}", key=p['name']):
                st.session_state.temp_input = f"Tell me more about {p['name']}"

# --- RIGHT COLUMN: The Modern Chatroom ---
with right_col:
    chat_container = st.container(height=500, border=False)
    
    with chat_container:
        # Initial greeting if chat is empty
        if not st.session_state.messages:
            st.chat_message("assistant", avatar="✨").write("Welcome back. How shall we refine your ritual today?")

        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="✨" if message["role"] == "assistant" else "👤"):
                st.markdown(message["content"])

    # Input Logic
    if prompt := st.chat_input("Message your consultant..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)

        # Generate AI response
        with chat_container:
            with st.chat_message("assistant", avatar="✨"):
                with st.spinner("Consulting archives..."):
                    # Dummy response logic for UI testing
                    def mock_ai(q):
                        return f"The {q} ritual is designed to restore balance. Based on our clinical data, it would suit your profile perfectly."
                    
                    # Real AI call (uncomment when API quota is back)
                    # model = genai.GenerativeModel("gemini-2.5-flash")
                    # response = model.generate_content(prompt)
                    # full_response = response.text
                    
                    full_response = mock_ai(prompt) 
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
