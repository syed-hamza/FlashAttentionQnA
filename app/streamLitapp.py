import streamlit as st

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Function to handle user input
def handle_user_input():
    user_input = st.text_input("You:", key='user_input')
    if user_input:
        # Simulate bot response (replace this with actual chatbot logic)
        bot_response = f"Bot: You said '{user_input}'"
        # Update chat history
        st.session_state.chat_history.append(f"You: {user_input}")
        st.session_state.chat_history.append(bot_response)
        # Clear the input box
        st.session_state.user_input = ""

st.sidebar.title("Chat History")
# Display chat history in the sidebar
for message in st.session_state.chat_history:
    st.sidebar.write(message)

st.title("Chatbot")

# Main chat interface
handle_user_input()
