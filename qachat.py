from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from google.generativeai import GenerativeModel


# Load environment variables from .env file
load_dotenv()  

# Configure the Gemini AI API
genai.configure(api_key=os.getenv("AIzaSyCgtNipG70IL7cMFgC4pqNTMKq0JtQt3wY"))

# Function to load the Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-1.5-pro") 
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize the Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input field for the user's question
user_input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# Handle user input and get a response from the Gemini model
if submit and user_input:
    response = get_gemini_response(user_input)
    
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", user_input))
    st.subheader("The Response is")
    
    # Display the response chunks
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

# Display the chat history
st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
