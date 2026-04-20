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

# Input pinned to bottom
user_prompt = st.chat_input("Enter your text to format...")

# New Request button below chat input, aligned right
_, btn_col = st.columns([4, 1])
with btn_col:
    if st.button("New Request", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- PROCESS SUBMISSION ---
if user_prompt:
    clean_input = user_prompt.strip()
    st.session_state.messages.append({"role": "user", "content": clean_input})

    if clean_input.lower().startswith(trigger_word.lower()):
        actual_request = clean_input[len(trigger_word):].strip()

        # Replace the last user message with the trigger-stripped version
        st.session_state.messages[-1] = {"role": "user", "content": actual_request}

        try:
            with st.spinner("Formatting your text..."):
                # Only send last 10 messages to keep costs down
                recent_history = st.session_state.messages[-10:]
                message = client.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=1024,
                    messages=recent_history
                )
            response_text = message.content[0].text
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        except anthropic.AuthenticationError:
            st.session_state.messages.append({"role": "assistant", "content": "❌ Invalid API key."})
        except anthropic.PermissionDeniedError:
            st.session_state.messages.append({"role": "assistant", "content": "❌ Permission denied."})
        except anthropic.NotFoundError:
            st.session_state.messages.append({"role": "assistant", "content": "❌ Model not found."})
        # except Exception:
        #     st.session_state.messages.append({"role": "assistant", "content": "❌ System error. Please try again."})
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "content": f"❌ Error: {str(e)}"})
    else:
        st.session_state.messages.append({"role": "assistant", "content": "❌ Sorry, can't format the text entered."})

    st.rerun()