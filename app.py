import streamlit as st
import anthropic

# --- CONFIGURATION ---
st.set_page_config(page_title="formatme", layout="centered")

st.markdown("<style>#MainMenu, footer, header, .stAppDeployButton {visibility: hidden; display:none;}</style>", unsafe_allow_html=True)

try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    trigger_word = st.secrets["TRIGGER_WORD"]
    client = anthropic.Anthropic(api_key=api_key)
except Exception:
    st.error("Config Error")
    st.stop()

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- LAYOUT ---
st.subheader("Format Text app")

chat_area = st.container()

with chat_area:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Input pinned to bottom, clears automatically after submit
user_prompt = st.chat_input("Enter your text to format...")

# --- PROCESS SUBMISSION ---
if user_prompt:
    clean_input = user_prompt.strip()
    st.session_state.messages.append({"role": "user", "content": clean_input})

    if clean_input.lower().startswith(trigger_word.lower()):
        actual_request = clean_input[len(trigger_word):].strip()
        try:
            with st.spinner("Formatting your text..."):
                message = client.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=1024,
                    messages=[{"role": "user", "content": actual_request}]
                )
            response_text = message.content[0].text
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        except anthropic.AuthenticationError:
            st.session_state.messages.append({"role": "assistant", "content": "❌ Invalid API key."})
        except anthropic.PermissionDeniedError:
            st.session_state.messages.append({"role": "assistant", "content": "❌ Permission denied."})
        except anthropic.NotFoundError:
            st.session_state.messages.append({"role": "assistant", "content": "❌ Model not found."})
        except Exception:
            st.session_state.messages.append({"role": "assistant", "content": "❌ System error. Please try again."})
    else:
        st.session_state.messages.append({"role": "assistant", "content": "❌ Sorry, can't format the text entered."})

    st.rerun()