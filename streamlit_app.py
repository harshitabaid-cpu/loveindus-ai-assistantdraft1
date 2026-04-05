# -------------------------
# Gemini AI response
# -------------------------
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
        # 1. Initialize the correct Gemini model 
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # 2. Call generate_content with the correct config syntax
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                max_output_tokens=500
            )
        )
        return response.text if response.text else "⚠️ No response generated."
        
    except Exception as e:
        return f"""
⚠️ AI error occurred.

Quick recommendations:
- Glowing skin: Amrutini Luminosity Dewdrops
- Dry skin: Hydrating oils/serums
- Radiance: Vitamin C products

(Error: {str(e)})
"""
