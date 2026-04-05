# streamlit_app.py
import streamlit as st
import os
import google.generativeai as genai

# -------------------------
# Streamlit UI Setup (Must be first Streamlit command)
# -------------------------
st.set_page_config(page_title="Tatcha AI Assistant", page_icon="💜", layout="wide")
st.title("💜 Tatcha AI Sales Assistant")
st.write("Discover your ritual with personalized recommendations for Tatcha's Japanese botanical skincare!")

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
    "Difference between Water Cream and Dewy Skin Cream?",
    "What is the best cleanser for dry skin?",
    "What is Hadasei-3 and why is it important?",
    "Which product is best for minimizing pores?"
]
selected_q = st.sidebar.radio("Choose a question:", [""] + quick_qs)

# -------------------------
# Load products (SAFE MODE: Bypassing the scraper temporarily)
# -------------------------
# from scrape_products import scrape_products  <-- Commented out for now!
with st.spinner("Fetching product info..."):
    # Using Tatcha dummy data to test the new brand persona
    products = [
        {
            "name": "The Dewy Skin Cream",
            "price": "$72.00",
            "description": "A rich, moisturizing cream with plumping hydration and antioxidant-packed Japanese purple rice for a dewy, healthy glow.",
            "benefits": ["Intense hydration", "Dewy glow", "Plumping", "Antioxidant protection"],
            "skin_type": ["Dry", "Normal"]
        },
        {
            "name": "The Water Cream",
            "price": "$72.00",
            "description": "An oil-free, clarifying water cream that releases a burst of hydrating nutrients and pore-refining Japanese wild rose.",
            "benefits": ["Lightweight hydration", "Pore refining", "Balancing", "Shine control"],
            "skin_type": ["Oily", "Combination"]
        },
        {
            "name": "The Rice Wash",
            "price": "$40.00",
            "description": "A gently effective, cream cleanser that washes away impurities without stripping skin, leaving a luminous finish.",
            "benefits": ["Gentle cleansing", "Softening", "Luminous finish", "pH balancing"],
            "skin_type": ["All", "Dry", "Combination"]
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
You are an expert, luxurious skincare assistant for Tatcha.

Goals:
- Recommend products based on the user's skin type or concern.
- Explain product benefits, highlighting Japanese botanicals where applicable.
- Adopt a calm, educational, mindful, and premium tone.
- Keep responses concise but highly informative.

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
    with st.spinner("Consulting the ritual..."):
        answer = get_ai_response(user_input)
    st.markdown("### 💜 Tatcha Assistant Says:")
    st.info(answer)
