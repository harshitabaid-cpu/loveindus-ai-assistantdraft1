# streamlit_app.py
import streamlit as st
import os
import google.generativeai as genai

# -------------------------
# Streamlit UI Setup (Must be first Streamlit command)
# -------------------------
st.set_page_config(page_title="Love, Indus AI Assistant", page_icon="🛍️", layout="wide")
st.title("🛍️ Love, Indus AI Sales Assistant")
st.write("Get personalized product recommendations and explanations for Love, Indus products!")

# -------------------------
# Configure Gemini API Safely
# -------------------------
api_key = os.environ.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    st.sidebar.success("API KEY LOADED: YES")
else:
    st.sidebar.error("API KEY LOADED: NO. Please set your GOOGLE_API_KEY environment variable.")

# Sidebar Quick Questions
st.sidebar.header("Quick Questions")
quick_qs = [
    "Best product for glowing skin",
    "Which product is suitable for dry skin?",
    "Why is Amrutini Luminosity Dewdrops worth buying?",
    "Explain Radiance Serum benefits"
]
selected_q = st.sidebar.radio("Choose a question:", [""] + quick_qs)

# -------------------------
# Load products (SAFE MODE: Bypassing the scraper temporarily)
# -------------------------
# from scrape_products import scrape_products  <-- Commented out for now!
with st.spinner("Fetching product info..."):
    # Using dummy data to guarantee the app loads without hanging
    products = [
        {
            "name": "Amrutini Luminosity Dewdrops",
            "price": "$135",
            "description": "A hydrating serum that brings out your inner glow.",
            "benefits": ["Glowing skin", "Hydration", "Plumping"],
            "skin_type": ["All", "Dry"]
        }
    ]

# -------------------------
# User input
# -------------------------
user_input = st.text_input("Ask your question or describe your skin concern:")
if selected_q:
    user_input = selected_q

# -------------------------
# Build product context
# -------------------------
def get_product_context():
    context = ""
    for p in products:
        context += f"""
Product: {p['name']}
Price: {p['price']}
Description: {p['description']}
Benefits: {', '.join(p['benefits']) if p['benefits'] else 'N/A'}
Skin types: {', '.join(p['skin_type']) if p['skin_type'] else 'All'}
"""
    return context

# -------------------------
# Gemini AI response
# -------------------------
def get_ai_response(query):
    if not api_key:
        return "⚠️ Please add your Google API Key to use the assistant."
        
    prompt = f"""
You are an expert Love, Indus skincare assistant.
Goals:
- Recommend products based on user's skin type or concern
- Explain product benefits
- Use friendly, premium tone

Product data:
{get_product_context()}

User query:
{query}
"""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                max_output_tokens=500
            )
        )
        return response.text if response.text else "⚠️ No response generated."
    except Exception as e:
        return f"⚠️ AI error occurred: {str(e)}"

# -------------------------
# Display AI answer
# -------------------------
if st.button("Get Recommendation") and user_input:
    with st.spinner("Thinking..."):
        answer = get_ai_response(user_input)
    st.markdown("### 🤖 AI Assistant Says:")
    st.info(answer)
