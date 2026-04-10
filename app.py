import streamlit as st
from google import genai

# --- CONFIGURATION ---
st.set_page_config(page_title="formatme", layout="centered")

# Stealth UI CSS
st.markdown("""
    <style>
    #MainMenu, footer, header, .stAppDeployButton {visibility: hidden; display:none;}
    </style>
""", unsafe_allow_html=True)

# --- LOAD SECRETS ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
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

if st.button("Submit"):
    if user_prompt:
        with st.spinner(""):
            try:
                # STABLE PAID-TIER MODEL FOR APRIL 2026
                response = client.models.generate_content(
                    model="gemini-3.1-flash-lite-preview", 
                    contents=user_prompt
                )
                
                if response.text:
                    st.divider()
                    st.markdown(response.text)
                else:
                    st.warning("No output generated.")
                    
            except Exception as e:
                # Paid tier gives more detailed error codes; this logs them
                st.error("System error. Please try again.")