import streamlit as st
from google import genai

# --- DISCREET CONFIGURATION ---
st.set_page_config(page_title="mplogic", layout="centered")

# Stealth UI: Hides all Streamlit branding
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

# --- LOAD SECRETS ---
try:
    # Ensure this matches exactly what is in your .streamlit/secrets.toml
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("Config Error: Check secrets.toml")
    st.stop()

# --- INTERFACE ---
user_prompt = st.text_area(label="Input", label_visibility="collapsed", height=300)

if st.button("OK"):
    if user_prompt:
        # Simple spinner for feedback
        with st.spinner(""):
            try:
                # Using the latest 2026 stable workhorse model
                response = client.models.generate_content(
                    model="gemini-3.1-flash-lite-preview", 
                    contents=user_prompt
                )
                
                if response.text:
                    st.divider()
                    st.markdown(response.text)
                else:
                    st.warning("No output.")
                    
            except Exception as e:
                # This will show you the REAL error if it fails again
                st.error(f"System error: {str(e)[:50]}")