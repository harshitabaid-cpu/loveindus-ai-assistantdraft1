import streamlit as st
import os
import google.generativeai as genai

# -------------------------
# 1. FLAGSHIP LUXURY CSS
# -------------------------
st.set_page_config(page_title="Tatcha Ritual Consultant", page_icon="💜", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    .product-box {
        background: #FFF;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid #F0F0F0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }
    .price-tag { color: #613082; font-weight: 600; font-family: 'Inter', sans-serif; }
    [data-testid="stChatMessage"] { border-radius: 15px; }
</style>
""", unsafe_allow_html=True)

# -------------------------
# 2. BRAND DATA (The "Brain's" Knowledge)
# -------------------------
products = [
    {
        "name": "The Dewy Skin Cream", 
        "price": "$72", 
        "ingredients": "Japanese Purple Rice, Algae, Hyaluronic Acid",
        "description": "A rich, plumping moisturizer for a healthy glow.",
        "conflicts": "None. Pairs well with The Essence.",
        "icon": "💜"
    },
    {
        "name": "The Water Cream", 
        "price": "$72", 
        "ingredients": "Japanese Wild Rose, Japanese Leopard Lily",
        "description": "Oil-free, pore-refining water cream.",
        "conflicts": "None. Ideal for oily/combination skin.",
        "icon": "💎"
    },
    {
        "name": "The Rice Wash", 
        "price": "$40", 
        "ingredients": "Japanese Rice Powder, Hyaluronic Acid",
        "description": "PH-neutral cream cleanser.",
        "conflicts": "None.",
        "icon": "☁️"
    }
]

# -------------------------
# 3. GENIUS AI LOGIC
# -------------------------
def get_ai_response(user_query, history):
    # Re-building the Deep Knowledge Base
    context = "YOU ARE AN ELITE TATCHA SKINCARE CONSULTANT.\n\nPRODUCT KNOWLEDGE:\n"
    for p in products:
        context += f"- {p['name']} ({p['price']}): {p['description']}. Ingredients: {p['ingredients']}. Warnings: {p['conflicts']}\n"
    
    # Adding Sales Tactics & Multi-part handling
    context += """
    \nCORE DIRECTIVES:
    1. VALIDATE: Start by acknowledging the user's specific skin concern.
    2. EDUCATE: Explain the science of the recommended product.
    3. UPSELL: Always suggest a complementary ritual step.
    4. SAFETY: If they ask to mix incompatible products, warn them.
    5. MULTI-PART: Answer every single question asked in the prompt.
    """
    
    # Injecting History for Continuity
    context += "\nCONVERSATION HISTORY:\n"
    for msg in history:
        context += f"{msg['role'].upper()}: {msg['content']}\n"
    
    context += f"\nNEW USER QUERY: {user_query}\n"

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(context)
        return response.text
    except Exception as e:
        return f"⚠️ I'm refining my notes (API Limit). Try again in 30s. Error: {str(e)}"

# -------------------------
# 4. TWO-COLUMN INTERFACE
# -------------------------
st.markdown("<h1 style='text-align: center; color: #1A1A1A;'>TATCHA</h1>", unsafe_allow_html=True)

left_side, right_side = st.columns([1, 1.2], gap="large")

with left_side:
    st.subheader("Featured Rituals")
    p_col1, p_col2 = st.columns(2)
    for i, p in enumerate(products):
        target = p_col1 if i % 2 == 0 else p_col2
        with target:
            st.markdown(f"""
            <div class="product-box">
                <div style="font-size: 35px;">{p['icon']}</div>
                <div style="font-weight: 500;">{p['name']}</div>
                <div class="price-tag">{p['price']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Consult on {p['name']}", key=f"btn_{i}", use_container_width=True):
                if "messages" not in st.session_state: st.session_state.messages = []
                st.session_state.messages.append({"role": "user", "content": f"Tell me about {p['name']}"})

with right_side:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_display = st.container(height=500, border=True)
    
    with chat_display:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"], avatar="💜" if msg["role"] == "assistant" else None):
                st.markdown(msg["content"])

    if prompt := st.chat_input("How can I assist your ritual today?"):
        # 1. User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 2. Get Genius Response
        with chat_display:
            with st.chat_message("assistant", avatar="💜"):
                with st.spinner("Consulting the archives..."):
                    full_response = get_ai_response(prompt, st.session_state.messages[:-1])
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.rerun()
