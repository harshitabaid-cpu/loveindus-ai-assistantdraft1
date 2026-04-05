# streamlit_app.py
import streamlit as st
from openai import OpenAI
import os
from scrape_products import scrape_products

# Use Streamlit Secrets for API key
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# UI setup
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

# User input
user_input = st.text_input("Ask your question or describe your skin concern:")
if selected_q:
    user_input = selected_q

# Build product context
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

# AI response function (UPDATED)
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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except Exception:
        return """
⚠️ AI is temporarily unavailable (quota or connection issue).

Here’s a quick recommendation:
- For glowing skin: Try **Amrutini Luminosity Dewdrops**
- For dry skin: Use hydrating serums with oils
- For radiance: Use Vitamin C based products

(Your AI assistant will be back shortly!)
"""

# Show result
if st.button("Get Recommendation") and user_input:
    with st.spinner("Thinking..."):
        answer = get_ai_response(user_input)
    st.markdown("### 🤖 AI Assistant Says:")
    st.success(answer)
