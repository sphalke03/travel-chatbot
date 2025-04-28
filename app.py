import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate(r'C:\Users\thesa\OneDrive\Desktop\firebase_key.json')  # <-- Correct path
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Streamlit App
st.title("✈️ Travel Booking Chatbot")

# Initialize session
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# Chatbot logic
def chatbot_response(user_input):
    user_input_lower = user_input.lower()

    if "book" in user_input_lower or "tour" in user_input_lower:
        return "Great! I can help you book a tour. Which destination are you interested in?"
    elif "paris" in user_input_lower:
        return "Paris is beautiful! We have a 5-day Paris package starting at $999. Would you like to proceed?"
    elif "goa" in user_input_lower:
        return "Goa is fantastic for beaches! 4 days/3 nights at ₹14,999. Should I book it for you?"
    elif "budget" in user_input_lower:
        return "Our budget packages start from ₹9,999 onwards. Which month are you planning to travel?"
    elif "hello" in user_input_lower or "hi" in user_input_lower:
        return "Hello! I'm your travel assistant. How can I help you today?"
    elif "thank you" in user_input_lower or "thanks" in user_input_lower:
        return "You're welcome! Happy to assist you anytime."
    else:
        return "I'm here to help with travel packages, bookings, and destinations. Could you please rephrase?"

# Ask for user's name (only once)
if not st.session_state.user_name:
    name_input = st.text_input("Enter your name to start chatting:")
    if st.button("Start Chatting"):
        if name_input.strip():
            st.session_state.user_name = name_input.strip()
        else:
            st.warning("Please enter a valid name.")

# Once name is entered, continue with chat
if st.session_state.user_name:
    st.success(f"Hello {st.session_state.user_name}! 👋 Start chatting below:")

    st.text_input("You:", key="user_input")

    if st.button("Send"):
        if st.session_state.user_input.strip():
            # Bot reply
            bot_reply = chatbot_response(st.session_state.user_input)

            # Update chat history
            st.session_state.messages.append(("You", st.session_state.user_input))
            st.session_state.messages.append(("Bot", bot_reply))

            # Store in Firebase
            chat_entry = {
                'name': st.session_state.user_name,
                'question': st.session_state.user_input,
                'bot_response': bot_reply
            }
            db.collection('chat_data').add(chat_entry)

            # Clear input after sending
            st.session_state.user_input = ""

# Display chat history
if st.session_state.messages:
    st.subheader("Conversation History:")
    for sender, message in st.session_state.messages:
        if sender == "You":
            st.markdown(f"**You:** {message}")
        else:
            st.markdown(f"**Bot:** {message}")
