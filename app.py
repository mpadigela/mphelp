import streamlit as st
from google import genai
from google.genai import errors

# --- CONFIGURATION ---
st.set_page_config(page_title="formatme", layout="centered")

# Stealth UI
st.markdown("<style>#MainMenu, footer, header, .stAppDeployButton {visibility: hidden; display:none;}</style>", unsafe_allow_html=True)

try:
    api_key = st.secrets["GEMINI_API_KEY"]
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
        
        if clean_input.lower().startswith(trigger_word.lower()):
            actual_request = clean_input[len(trigger_word):].strip()
            
            with st.spinner(""):
                try:
                    # UPDATED: Use the stable GA model for 2026
                    # If this still fails, try "gemini-1.5-flash" (legacy fallback)
                    response = client.models.generate_content(
                        model="gemini-2.5-flash", 
                        contents=actual_request
                    )
                    
                    if response.text:
                        st.divider()
                        st.markdown(response.text)
                    else:
                        st.warning("No output generated.")
                        
                except errors.ClientError as e:
                    # Specific handling for paid tier error codes
                    if e.code == 404:
                        st.error("Model not found. Try 'gemini-1.5-flash'.")
                    elif e.code == 403:
                        st.error("Permission denied. Check API key status.")
                    else:
                        st.error(f"Error {e.code}: Try again.")
                except Exception:
                    st.error("System error. Please try again.")
        else:
            st.error("Sorry, cant format the text entered")