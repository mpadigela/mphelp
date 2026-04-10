import streamlit as st
from google import genai

# --- DISCREET CONFIGURATION ---
st.set_page_config(page_title="formatme", layout="centered")

# Stealth UI
st.markdown("""
    <style>
    #MainMenu, footer, header, .stAppDeployButton {visibility: hidden; display:none;}
    </style>
""", unsafe_allow_html=True)

# --- LOAD SECRETS ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    # Retrieve the secret keyword from secrets.toml
    trigger_word = st.secrets["TRIGGER_WORD"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("Config Error")
    st.stop()

# --- INTERFACE ---
st.subheader("Format Text app")

user_prompt = st.text_area(
    label="Input Data", 
    label_visibility="collapsed", 
    placeholder="Enter your text to format....", 
    height=300
)

if st.button("Format text"):
    if user_prompt:
        clean_input = user_prompt.strip()
        
        # Check against the secret keyword from your config
        if clean_input.lower().startswith(trigger_word.lower()):
            # Strip the keyword from the prompt before sending to Gemini
            actual_request = clean_input[len(trigger_word):].strip()
            
            with st.spinner(""):
                try:
                    # Using the latest stable 2026 workhorse
                    response = client.models.generate_content(
                        model="gemini-3.1-flash-lite-preview", 
                        contents=actual_request
                    )
                    
                    if response.text:
                        st.divider()
                        st.markdown(response.text)
                    else:
                        st.warning("No output generated.")
                        
                except Exception:
                    st.error("System error. Please try again.")
        else:
            # Discreet unauthorized message
            st.error("Sorry, cant format the text entered")