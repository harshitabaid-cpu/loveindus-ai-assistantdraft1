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
# 2. DESIGN EXPERT CSS
# ---------------------------------------------------------
st.set_page_config(page_title=f"{BRAND_NAME} Concierge", layout="centered")

# Standard string used for CSS to avoid f-string curly brace errors
st.markdown("""
<style>
    /* Main Widget Container */
    [data-testid="stVerticalBlock"] > div:has(div.luxury-widget) {
        max-width: 480px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: auto;
        overflow: hidden;
        border: 1px solid #EDEDED;
        display: flex;
        flex-direction: column;
    }

    /* SLIM HEADER */
    .rep-header {
        background-color: #000000;
        color: white;
        padding: 12px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .header-titles h3 { margin: 0; font-size: 26px !important; font-weight: 500; color: white; }
    .header-titles p { margin: 0; font-size: 16px !important; color: #AAA; font-weight: 300; }
    .header-icons { display: flex; gap: 15px; font-size: 20px; opacity: 0.8; }

    /* CHAT ALIGNMENT */
    [data-testid="stChatMessage"] {
        font-size: 21px !important;
        background: transparent !important;
        padding: 5px 20px !important;
    }
    
    /* User: Right Aligned Content */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
        flex-direction: row-reverse !important;
        text-align: right !important;
    }
    [data-testid="stChatMessageAvatarUser"] { display: none !important; }

    /* Assistant: Left Aligned Text */
    .assistant-text { font-size: 21px !important; line-height: 1.4; color: #1A1A1A; }

    /* SUGGESTION CHIPS: Ultra-Compact & Right Above Input */
    [data-testid="column"] {
        width: fit-content !important;
        flex: unset !important;
        min-width: unset !important;
        padding: 0 !important;
    }
    
    .stHorizontalBlock {
        gap: 4px !important; 
        margin-bottom: -28px !important; /* Pulls them tight to the input box */
        padding: 0 20px !important;
        justify-content: flex-start !important;
    }
    
    div.stButton > button {
        border-radius: 20px !
    
