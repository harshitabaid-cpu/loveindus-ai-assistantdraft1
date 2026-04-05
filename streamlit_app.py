import streamlit as st
import os
import google.generativeai as genai

# ---------------------------------------------------------
# 1. BRAIN CONFIG
# ---------------------------------------------------------
BRAND_NAME = "Tatcha"
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# ---------------------------------------------------------
# 2. DESIGN EXPERT CSS (ULTRA-COMPACT & RIGHT ALIGNED)
# ---------------------------------------------------------
st.set_page_config(page_title=f"{BRAND_NAME} Concierge", layout="centered")

st.markdown(f"""
<style>
    /* Main Widget Container */
    [data-testid="stVerticalBlock"] > div:has(div.luxury-widget) {{
        max-width: 480px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: auto;
        overflow: hidden;
        border: 1px solid #EDEDED;
        display: flex;
        flex-direction: column;
    }}

    /* SLIM HEADER */
    .rep-header {{
        background-color: #000000;
        color: white;
        padding: 12px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .header-titles h3 {{ margin: 0; font-size: 26px !important; font-weight: 500; color: white; }}
    .header-titles p {{ margin: 0; font-size: 16px !important; color: #AAA; font-weight: 300; }}
    .header-icons {{ display: flex; gap: 15px; font-size: 20px; opacity: 0.8; }}

    /* CHAT ALIGNMENT */
    [data-testid="stChatMessage"] {{
        font-size: 21px !important;
        background: transparent !important;
        padding: 5px 20px !important;
    }}
    
    /* User: Right Aligned */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
        flex-direction: row-reverse !important;
        text-align: right !important;
    }}
    [data-testid="stChatMessageAvatarUser"] {{ display: none !important; }}

    /* Assistant: Left Aligned */
    .assistant-text {{ font-size: 21px !important; line-height: 1.4; color: #1A1A1A; }}

    /* SUGGESTION CHIPS: Ultra-Compact & Right Above Input */
    .stHorizontalBlock {{
        gap: 8px !important; /* Forces 2-space feel between buttons */
        margin-bottom: -15px !important; /* Pulls it down to the input box */
    }}
    
    div.stButton > button {{
        border-radius: 20px !important;
        border: 1px solid #DDD !important;
        background: white !important;
        padding: 2px 10px !important;
        font-size: 16px !important;
        height: auto !important;
    }}
