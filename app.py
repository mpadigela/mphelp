import streamlit as st
import anthropic

# --- CONFIGURATION ---
st.set_page_config(page_title="formatme", layout="centered")

# Stealth UI
st.markdown("<style>#MainMenu, footer, header, .stAppDeployButton {visibility: hidden; display:none;}</style>", unsafe_allow_html=True)

try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    trigger_word = st.secrets["TRIGGER_WORD"]
    client = anthropic.Anthropic(api_key=api_key)
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
                    message = client.messages.create(
                        model="claude-sonnet-4-5",
                        max_tokens=1024,
                        messages=[
                            {"role": "user", "content": actual_request}
                        ]
                    )

                    response_text = message.content[0].text
                    if response_text:
                        st.divider()
                        st.markdown(response_text)
                    else:
                        st.warning("No output generated.")

                except anthropic.AuthenticationError:
                    st.error("Invalid API key. Check your ANTHROPIC_API_KEY.")
                except anthropic.PermissionDeniedError:
                    st.error("Permission denied. Check your API key status.")
                except anthropic.NotFoundError:
                    st.error("Model not found. Check the model name.")
                except anthropic.APIError:
                    st.error("API error. Please try again.")
                except Exception:
                    st.error("System error. Please try again.")
        else:
            st.error("Sorry, cant format the text entered")