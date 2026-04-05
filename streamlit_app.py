import streamlit as st

# -------------------------
# 1. PAGE SETUP & CLONE CSS
# -------------------------
# 'centered' layout is key to constraining the width like a widget.
st.set_page_config(page_title="AI Concierge", page_icon="✨", layout="centered")

# --- ADVANCED CUSTOM CSS: The Clone ---
st.markdown("""
<style>
    /* 1. Overall Background (Light Gray like image) */
    .stApp {
        background-color: #F9F9FB;
    }
    
    /* 2. THE WIDGET CONTAINER (The Floating Box) */
    /* We use unique selectors to target the main content block */
    [data-testid="stVerticalBlock"] > div:has(div.concierge-widget) {
        max-width: 400px; /* Constraining width like a phone screen */
        padding: 0;
        background: white;
        border-radius: 30px;
        box-shadow: 0 30px 60px rgba(0,0,0,0.1);
        margin: 50px auto; /* Centers it on screen */
        overflow: hidden; /* Ensures rounded corners on header */
        border: 1px solid #EDEDED;
    }

    /* 3. THE HEADER (Dark Gray Bar from image) */
    .chat-header {
        background-color: #6D6D6D; /* Exact dark gray */
        color: white;
        padding: 25px 25px;
        display: flex;
        align-items: center;
        width: 100%;
    }
    .header-text {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        margin-left: 15px;
    }
    .header-text h3 { margin: 0; color: white; font-weight: 500; font-size: 19px; }
    .header-text p { margin: 0; color: #DEDEDE; font-size: 14px; font-weight: 300; }

    /* 4. THE PRODUCT AREA (Pure HTML Card) */
    .product-card {
        padding: 30px;
        text-align: center;
        background-color: white;
    }
    /* Large grey placeholder from image */
    .product-image-placeholder {
        background-color: #EEEEEE; 
        height: 250px; 
        border-radius: 10px; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        margin-bottom: 25px;
        font-size: 70px;
        color: #AAA;
    }
    /* Text styling from image */
    .product-name {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        font-size: 17px;
        color: #1A1A1A;
        margin-bottom: 8px;
        text-align: left;
    }
    .product-price {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 26px;
        font-weight: 800;
        color: #1A1A1A;
        margin-bottom: 25px;
        text-align: left;
    }

    /* 5. BUTTON CLONING (Rounded) */
    div.stButton > button {
        width: 100% !important;
        border-radius: 40px !important; /* Extremely rounded like image */
        font-weight: 400;
        text-transform: none;
        letter-spacing: normal;
        height: 50px;
        margin-bottom: 12px;
        font-size: 16px;
    }
    /* "Learn More" (Outline style) */
    .outline-button button {
        background-color: white !important;
        color: #333 !important;
        border: 1.5px solid #C0C0C0 !important;
    }
    /* "Add to Cart" (Filled gray style) */
    .filled-button button {
        background-color: #6D6D6D !important;
        color: white !important;
        border: none !important;
    }

    /* 6. INPUT CLONING (The Pill shape at the bottom) */
    /* Pinned chat input styling */
    .stChatInputContainer {
        border-radius: 40px !important;
        padding: 10px 20px !important;
        margin-bottom: 30px !important;
        margin-top: 20px !important;
        background-color: white !important;
        border: 2px solid #DEDEDE !important;
    }
    .stChatInputContainer:focus-within {
        border-color: #6D6D6D !important;
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
st.markdown("""
<div class="chat-header">
    <div style="width: 55px; height: 55px; background-color: #1200E4; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
        <span style="color: white; font-size: 28px;">💙</span>
    </div>
    <div class="header-text">
        <h3>AI Concierge</h3>
        <p>Here to help you shop</p>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------
# 4. PRODUCT DISCOVERY (Pure HTML Card)
# -------------------------
# Simulated product data
featured_product = {
    "name": "Velvet :08 Broadway Bright Detox Mask",
    "price": "$58",
}

# Injecting the product visuals as pure HTML to replicate the exact format
st.markdown(f"""
<div class="product-card">
    <div class="product-image-placeholder">
        <span>📸</span>
    </div>
    <p class="product-name">{featured_product['name']}</p>
    <p class="product-price">{featured_product['price']}</p>
</div>
""", unsafe_allow_html=True)

# --- Button Clones (Rounded) ---
# We use standard Streamlit buttons wrapped in a styled container
btn_col_l, btn_col_c, btn_col_r = st.columns([0.1, 1, 0.1])
with btn_col_c:
    st.markdown("<div class='outline-button'>", unsafe_allow_html=True)
    st.button("ⓘ Learn more", key="learn_btn")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='filled-button'>", unsafe_allow_html=True)
    # Using a cart icon placeholder
    st.button("🛒 Add to cart", key="add_btn")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("") # Spacer

# -------------------------
# 5. INPUT & CONVERSATION (The Pill at the bottom)
# -------------------------
# To make this a "same as the screenshot" visual test, we just show the pill.
if prompt := st.chat_input("Type anything here..."):
    # When your API is back, you'd trigger the Genius logic here.
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        st.write("A refined choice. That formulation utilizes Hadasei-3™.")

# Close the concierge widget container
st.markdown("</div>", unsafe_allow_html=True)
