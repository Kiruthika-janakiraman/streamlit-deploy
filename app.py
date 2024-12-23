import streamlit as st
import openai
import json
import re

# Load Intents
with open("intents.json") as file:
    intents = json.load(file)['intents']

# Set OpenAI API Key
openai.api_key = "YOUR_API_KEY"

# Function to Match Intents
def match_intent(user_input):
    user_input = user_input.lower()
    for intent in intents:
        for pattern in intent['patterns']:
            if re.search(r'\b' + pattern + r'\b', user_input):
                return intent['response']
    return None

# Streamlit App Layout
st.title("LawBot Chatbot 🤖⚖️")
st.write("Your AI-powered legal assistant!")

# User Input
user_input = st.text_input("Ask your legal question:")

if user_input:
    # Check for predefined intents
    intent_response = match_intent(user_input)
    if intent_response:
        st.write("**LawBot:**", intent_response)
    else:
        try:
            # Fallback to OpenAI API if no intent matches
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful legal assistant chatbot."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.write("**LawBot:**", response['choices'][0]['message']['content'])
        except Exception as e:
            st.error(f"Error: {e}")
