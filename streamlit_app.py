# streamlit_app.py
import streamlit as st
import google.generativeai as genai
import os
from scrape_products import scrape_products

# Configure Gemini
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")
st.write("API KEY LOADED:", "YES" if os.environ.get("GOOGLE_API_KEY") else "NO")
# UI
st.set_page_config(page_title="Love, Indus AI Assistant", page_icon="🛍️", layout="wide")
st.title("🛍️ Love, Indus AI Sales Assistant")
st.write("Get personalized product recommendations and explanations for Love, Indus products!")

# Sidebar
st.sidebar.header("Quick Questions")
quick_qs = [
    "Best product for glowing skin",
    "Which product is suitable for dry skin?",
    "Why is Amrutini Luminosity Dewdrops worth buying?",
    "Explain Radiance Serum benefits"
]
selected_q = st.sidebar.radio("Choose a question:", [""] + quick_qs)

# Load products
with st.spinner("Fetching product info..."):
    products = scrape_products()

# Input
user_input = st.text_input("Ask your question or describe your skin concern:")
if selected_q:
    user_input = selected_q

# Build context
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

# Gemini response
def get_ai_response(query):
    prompt = f"""
You are an expert Love, Indus skincare assistant.

Goals:
- Recommend products based on user's skin type or concern
- Explain product benefits
- Handle objections about price or effectiveness
- Use friendly, premium tone

Product data:
{get_product_context()}

User query:
{query}

Answer conversationally with recommendation and reasoning.
"""

    try:
        response = model.generate_content(prompt)

        if response and hasattr(response, "text") and response.text:
            return response.text
        else:
            return "⚠️ No response generated. Try again."

    except Exception as e:
        return f"""
⚠️ AI error occurred.

Quick recommendations:
- Glowing skin: Amrutini Luminosity Dewdrops
- Dry skin: Hydrating oils/serums
- Radiance: Vitamin C products

(Error: {str(e)})
"""

# Output
if st.button("Get Recommendation") and user_input:
    with st.spinner("Thinking..."):
        answer = get_ai_response(user_input)
    st.markdown("### 🤖 AI Assistant Says:")
    st.success(answer)
