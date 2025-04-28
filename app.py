import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('firebase_key.json')  
firebase_admin.initialize_app(cred)
db = firestore.client()

# Streamlit App
st.title("✈️ Travel Booking Chatbot")

# Initialize session
if 'messages' not in st.session_state:
    st.session_state.messages = []

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

# Input from user
user_name = st.text_input("Enter your name:")

user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_name and user_input:
        # Get bot reply
        bot_reply = chatbot_response(user_input)

        # Display conversation
        st.session_state.messages.append(("You", user_input))
        st.session_state.messages.append(("Bot", bot_reply))

        # Store in Firebase
        chat_entry = {
            'name': user_name,
            'question': user_input,
            'bot_response': bot_reply
        }
        db.collection('chat_data').add(chat_entry)

# Display chat history
st.subheader("Conversation History:")
for sender, message in st.session_state.messages:
    if sender == "You":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**Bot:** {message}")
