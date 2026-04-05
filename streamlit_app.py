# streamlit_app.py
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from scrape_products import scrape_products

# Load API key from LI.env
load_dotenv(dotenv_path="LI.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit UI
st.set_page_config(page_title="Love, Indus AI Assistant", page_icon="🛍️", layout="wide")
st.title("🛍️ Love, Indus AI Sales Assistant")
st.write("Get personalized product recommendations and explanations for Love, Indus products!")

# Sidebar Quick Questions
st.sidebar.header("Quick Questions")
quick_qs = [
    "Best product for glowing skin",
    "Which product is suitable for dry skin?",
    "Why is Amrutini Luminosity Dewdrops worth buying?",
    "Explain Radiance Serum benefits"
]
selected_q = st.sidebar.radio("Choose a question:", [""] + quick_qs)

# Load Products
with st.spinner("Fetching product info..."):
    products = scrape_products()

# User Input
user_input = st.text_input("Ask your question or describe your skin concern:")
if selected_q:
    user_input = selected_q

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
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Show Answer
if st.button("Get Recommendation") and user_input:
    with st.spinner("Thinking..."):
        answer = get_ai_response(user_input)
    st.markdown("### 🤖 AI Assistant Says:")
    st.success(answer)
    
