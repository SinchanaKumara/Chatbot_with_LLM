import streamlit as st
import requests
import json

# Function to call the local LLM service
def get_response(prompt):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "llama3",
        "prompt": prompt,
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            response_text = ""
            # Split response content by newline and process each JSON object
            for line in response.iter_lines():
                if line:
                    try:
                        response_data = json.loads(line)
                        response_text += response_data.get('response', '') + " "
                    except json.JSONDecodeError as e:
                        response_text += f"Error decoding JSON: {str(e)} "
            return response_text.strip()
        else:
            return f"Error: {response.status_code} - {response.reason}"
    except requests.exceptions.RequestException as e:
        return f"Request error: {str(e)}"

st.title("Local LLM Chatbot")

if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Sidebar
st.sidebar.header("Chatbot Options")
user_input = st.sidebar.text_area("You:", key="user_input", height=100)

if st.sidebar.button("Send"):
    if user_input:
        # Add user input to conversation
        st.session_state.conversation.append({"role": "user", "text": user_input})

        # Generate model response
        with st.spinner("Generating response..."):
            response_text = get_response(user_input)

        # Add model response to conversation
        st.session_state.conversation.append({"role": "bot", "text": response_text})

# Display conversation
st.subheader("Conversation")
for message in st.session_state.conversation:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['text']}")
    else:
        st.markdown(f"**Bot:** {message['text']}")

# Clear conversation
if st.sidebar.button("Clear Conversation"):
    st.session_state.conversation = []
