import streamlit as st
from google import genai
from google.genai import errors
import logging

# Set up basic logging to see the real error in your terminal/cloud logs
logging.basicConfig(level=logging.INFO)

# --- DISCREET CONFIGURATION ---
st.set_page_config(page_title="mplogic", layout="centered")

# Enhanced CSS  + Reliable Hourglass
st.markdown("""
    <style>
    /* Hide standard UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display:none;}
    
    /* Force hourglass cursor globally when Streamlit is 'busy' */
    .stApp[data-testscript-state="running"] {
        cursor: wait !important;
    }
    .stApp[data-testscript-state="running"] * {
        cursor: wait !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOAD SECRETS ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("Config Error")
    st.stop()

# --- INTERFACE ---
client = genai.Client(api_key=api_key)

user_prompt = st.text_area(
    label="Input", 
    label_visibility="collapsed", 
    placeholder="", 
    height=300
)

if st.button("OK"):
    if user_prompt:
        try:
            # Note: If this fails, try "gemini-2.0-flash" as a fallback
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=user_prompt
            )
            
            if response.text:
                st.divider()
                st.markdown(response.text)
            else:
                st.warning("No output.")

        except errors.ClientError as e:
            logging.error(f"Client Error: {e}")
            st.error("Busy" if e.code == 429 else "Error")
        
        except Exception as e:
            # This logs the REAL error to your console/logs so you can see it
            logging.error(f"Actual Error: {e}") 
            st.error("System error")