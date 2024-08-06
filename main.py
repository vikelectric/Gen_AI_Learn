import os
import json

import streamlit as st
from groq import Groq


# streamlit page configuration
st.set_page_config(
    page_title="Happy Travels",
    page_icon="🗺️",
    layout="centered"
)

working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

GROQ_API_KEY = config_data["GROQ_API_KEY"]

# save the api key to environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# initialize the chat history as streamlit session state of not present already
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# streamlit page title
st.title("🗺️ Happy Travels")

# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# input field for user's message:
user_prompt = st.chat_input("Ask Jajabor...")

if user_prompt:

    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # sens user's message to the LLM and get a response
    messages = [
        {"role": "system", "content": "For the rest of this conversation act like a human travel agent Nancy for agency Happy Travels. You should interact with a traveller, listen to his or her requirements and help to plan a trip. You should take your time to consider your response so that it is short and relevant. Ask questions one by one to simulate a real conversation. Find out by way of casual conversation all the key details needed to plan a trip like budget, number of travelers, compositon of group, timeline etc. Then after a set of 5 to 7 questions you should provide a preliminary itinerary tease to the traveler to guage his/her interest and whether you are on the right track. Iterate the process till the traveller is satisfied with the interacton."},
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # display the LLM's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
