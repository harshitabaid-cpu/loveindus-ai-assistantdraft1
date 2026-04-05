# streamlit_app.py
import streamlit as st
import os
import google.generativeai as genai
from scrape_products import scrape_products # 🔗 Connecting your scraper!

# -------------------------
# Streamlit UI Setup
# -------------------------
st.set_page_config(page_title="Clinical AI Assistant", page_icon="🧪", layout="wide")
st.title("🧪 Clinical Skincare Expert & Sales Assistant")
st.write("Expert advice, routine building, and safe ingredient pairing.")

# -------------------------
# Configure Gemini API
# -------------------------
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    st.sidebar.success("API KEY LOADED: YES")
else:
    st.sidebar.error("API KEY LOADED: NO. Please set your GOOGLE_API_KEY environment variable.")

# -------------------------
# Load products (With Caching!)
# -------------------------
# We use session_state so it only scrapes ONCE when you load the app
with st.spinner("Fetching clinical data & conflict charts..."):
    if "products" not in st.session_state:
        st.session_state.products = scrape_products()
    products = st.session_state.products

# -------------------------
# Build Deep Product Context
# -------------------------
def get_product_context():
    context = ""
    for p in products:
        context += f"""
Product: {p.get('name', 'Unknown')}
Price: {p.get('price', 'N/A')}
Description: {p.get('description', 'N/A')}
Key Ingredients: {p.get('key_ingredients', 'N/A')}
How to Use: {p.get('how_to_use', 'N/A')}
Conflicts & Warnings: {p.get('conflicts', 'None listed')}
---
"""
    return context

# -------------------------
# The "Genius" AI Logic
# -------------------------
def get_ai_response(query):
    if not api_key:
        return "⚠️ Please add your Google API Key to use the assistant."
        
    prompt = f"""
You are an elite, highly knowledgeable Skincare Sales Consultant. 

YOUR DATA SOURCE:
{get_product_context()}

YOUR CORE DIRECTIVES:
1. MULTI-TASKING: The user may ask multiple questions at once. Break down your response using clear bullet points or bold text to ensure NO part of their query is ignored.
2. SAFETY & EXPERTISE FIRST: Always check the "Conflicts & Warnings" data. If a user asks about combining incompatible ingredients, strictly warn them and explain the science of why they shouldn't mix them.
3. SALES PSYCHOLOGY (The Consultative Close):
   - Acknowledge & Validate: Briefly validate their specific skin concern.
   - Educate: Recommend a product and explain *why* the 'Key Ingredients' solve their problem.
   - The Gentle Upsell: Always suggest a complementary product to build a routine (e.g., if recommending an exfoliator, suggest a hydrating serum for barrier support).
   - Value Proposition: Casually mention the accessible 'Price' to eliminate cost objections.
4. TONE: Clinical, deeply empathetic, highly professional, and persuasive but never "pushy".

USER QUERY:
{query}
"""
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.7, # 0.7 keeps it creative for sales, but logical for science
                max_output_tokens=800 # Increased so it has room to answer complex, multi-part questions
            )
        )
        return response.text if response.text else "⚠️ No response generated."
    except Exception as e:
        return f"⚠️ AI error occurred: {str(e)}"

# -------------------------
# User Input & UI
# -------------------------
# Using a larger text area so users can type complex, multi-part questions
user_input = st.text_area("Ask me multiple questions, ask about building a routine, or check ingredient conflicts:", height=100)

if st.button("Consult Expert"):
    if user_input:
        with st.spinner("Analyzing formulation data and building response..."):
            answer = get_ai_response(user_input)
        st.markdown("### 🧪 Expert Consultation:")
        st.info(answer)
    else:
        st.warning("Please type a question first.")
