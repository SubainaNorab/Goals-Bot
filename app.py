import streamlit as st
import together

# ==== TOGETHER AI SETUP ====
together.api_key = "9b5fdbfe6e161ca597bbdcda5d7892b41dce8932d1ce02a2504b0cbd5f9bd400"
LLM_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"

def get_bot_response(message):
    # Handle stuck message manually
   if any(phrase in message.lower() for phrase in ["i am stuck", "i am feeling stuck", "stuck in this task"]):
    return "It’s okay to feel stuck sometimes! 😊 Try taking a short break and doing something you enjoy, like reading, watching a movie, or going for a walk."


   try:
        prompt = f"You are a helpful assistant.\nUser: {message}\nAssistant:"
        response = together.Complete.create(
            prompt=prompt,
            model=LLM_MODEL,
            max_tokens=1500,
            temperature=0.7,
            top_k=50,
            top_p=0.7,
            repetition_penalty=1.1
        )
        return response['choices'][0]['text'].strip()
   except Exception as e:
        return "Good to know!  I ran into an issue while thinking. Please try again shortly."

# ==== STREAMLIT UI SETUP ====
st.set_page_config(
    page_title="Goals Bot",
    page_icon="🌟",  # Emoji as favicon
    layout="centered"
)
st.markdown("""
    <style>
        :root {
            --user-bubble-bg: linear-gradient(to right, #4a90e2, #1e3c72);
            --bot-bubble-bg-light: #f5f5f5;
            --bot-bubble-bg-dark: #2a2a2a;
            --text-color-light: #000;
            --text-color-dark: #fff;
        }

        @media (prefers-color-scheme: dark) {
            body, .stApp {
                background: linear-gradient(135deg, #1a1a1a, #2e2e2e) !important;
                color: var(--text-color-dark) !important;
            }
            .bot-bubble {
                background: var(--bot-bubble-bg-dark) !important;
                color: var(--text-color-dark) !important;
                border: 1px solid #444;
            }
        }

        @media (prefers-color-scheme: light) {
            body, .stApp {
                background: linear-gradient(135deg, #fafbfc, #dee7f0) !important;
                color: var(--text-color-light) !important;
            }
            .bot-bubble {
                background: var(--bot-bubble-bg-light) !important;
                color: var(--text-color-light) !important;
                border: 1px solid #ccc;
            }
        }

        .chat-bubble {
            max-width: 75%;
            padding: 1rem 1.5rem;
            border-radius: 18px;
            margin: 0.5rem 0;
            font-size: 1rem;
            line-height: 1.5;
            word-wrap: break-word;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .user-bubble {
            background: var(--user-bubble-bg) !important;
            color: #fff !important;
            margin-left: auto;
        }

        #MainMenu, header, footer {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)



st.title("Goals Bot")
st.markdown("#### Let’s work on a dream or build a roadmap.")


# ==== SESSION STATE ====
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==== HANDLE INPUT ====
user_input = st.chat_input("Let's turn your goal into roadmap...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.spinner("🤔 Thinking..."):
        bot_reply = get_bot_response(user_input)
    st.session_state.chat_history.append(("bot", bot_reply))

# ==== SHOW CHAT ====
for role, msg in st.session_state.chat_history:
    bubble_class = "user-bubble" if role == "user" else "bot-bubble"
    st.markdown(f"<div class='chat-bubble {bubble_class}'>{msg}</div>", unsafe_allow_html=True)
