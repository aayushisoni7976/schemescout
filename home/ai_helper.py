import google.generativeai as genai

# Apni Nayi API Key yahan dalo
API_KEY = "AIzaSyB8z_hwf1ryhhvczq6xAqewsHY11I8l4T8" 
genai.configure(api_key=API_KEY)

def get_scheme_recommendations(profile):
    try:
        # Sabse stable model name
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
You are a government scheme expert for India.
Based on this user profile, suggest exactly 4 most relevant schemes.

User Profile:
- State: {profile.state}
- Category: {profile.category}
- Income: {profile.annual_income}
- Age: {profile.current_age}
- Occupation: {profile.occupation}

  Strictly response in plain text only. Do NOT use markdown code blocks like ```json. Do NOT use any brackets [ ].


  Strictly provide only the official Government of India portal links. Crucially: If you are not 100% sure about the direct deep-link to a scheme, ONLY provide the main landing page URL (e.g., provide 'https://www.myscheme.gov.in/' or 'https://scholarships.gov.in/' instead of a long broken sub-link). Do not hallucinate or guess URL paths.

Return ONLY in this format — no extra text nothing extra:

  
    "name": "Scheme Name",
    "benefit": "Benefit description",
    "amount": 25000,
    "description": "Short description",
    "documents": ["Aadhaar", "Income Certificate"],
    "apply_link": "Direct official application URL or portal link",
    "deadline": "31 Oct 2026",
    "match_score": 94

    REMEMBER: You MUST write [END_SCHEME] after EVERY scheme. Total 3 times.
  
"""
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI is resting. Error: {str(e)}"