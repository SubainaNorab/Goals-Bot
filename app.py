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
        .stApp {
            background: linear-gradient(135deg, #f0f4f8, #e6f2ff);
            font-family: 'Inter', sans-serif;
        }
        .chat-bubble {
            max-width: 80%;
            padding: 1rem 1.5rem;
            border-radius: 16px;
            margin-bottom: 1rem;
            font-size: 1rem;
            line-height: 1.6;
            word-wrap: break-word;
        }
        .bot-bubble {
            background: #f1f1f1;
            border: 1px solid #e0e0e0;
            color: #333;
            margin-right: auto;
        }
        .user-bubble {
            background: linear-gradient(135deg, #4a90e2, #357abd);
            color: white;
            margin-left: auto;
        }
        #MainMenu, header, footer {
            visibility: hidden;
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
