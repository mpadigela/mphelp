import streamlit as st
from google import genai

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Custom Gemini Interface", layout="centered")
st.title("🚀 Personal AI Assistant")

# --- LOAD SECRETS ---
# Streamlit will look for 'GEMINI_API_KEY' in .streamlit/secrets.toml
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("Missing API Key! Please add GEMINI_API_KEY to your .streamlit/secrets.toml file.")
    st.stop()

# --- MAIN INTERFACE ---
client = genai.Client(api_key=api_key)

user_prompt = st.text_area(
    "Enter your request:",
    placeholder="e.g., 'Rewrite this email...' or 'Generate SQL for...'",
    height=200
)

if st.button("Generate Response"):
    if user_prompt:
        with st.spinner("Thinking..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=user_prompt
                )
                
                st.subheader("Result:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a prompt first.")