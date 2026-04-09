import streamlit as st
from google import genai
from google.genai import errors
import logging

# --- DISCREET CONFIGURATION ---
st.set_page_config(page_title="mplogic", layout="centered")

# Stealth UI CSS
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "processing" not in st.session_state:
    st.session_state.processing = False

def start_processing():
    st.session_state.processing = True

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
    height=300,
    disabled=st.session_state.processing
)

# Button remains disabled while processing to prevent double-clicks
if st.button("OK", on_click=start_processing, disabled=st.session_state.processing):
    if user_prompt:
        # Spinner provides visual feedback during wait
        with st.spinner(""): 
            try:
                # UPDATED TO STABLE 2.5 FLASH
                response = client.models.generate_content(
                    model="gemini-2.5-flash", 
                    contents=user_prompt
                )
                
                if response.text:
                    st.divider()
                    st.markdown(response.text)
                else:
                    st.warning("No output.")

            except errors.ClientError as e:
                # 429 is common on free tier for high-frequency use
                st.error("Busy" if e.code == 429 else "Error")
            except Exception as e:
                logging.error(f"DEBUG: {e}")
                st.error("System error")
        
        # Reset state to re-enable the button
        st.session_state.processing = False
        st.rerun()