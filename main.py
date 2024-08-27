import os
import json
from datetime import date

# Returns the current local date
today = date.today()

import streamlit as st
from groq import Groq

date_context = "Today is " + str(today)

# streamlit page configuration
st.set_page_config(
    page_title="Happy Travels",
    page_icon="🗺️",
    layout="centered"
)

# get working directory of the actual strteamlit environment
working_dir = os.path.dirname(os.path.abspath(__file__))

'''
#read the config file for API Key(s) -- LOCAL MACHINE RUNS
#config_data = json.load(open(f"{working_dir}/config.json"))
#GROQ_API_KEY = config_data["GROQ_API_KEY"]
'''

#read the config file for API Key(s) --- STREAMLIT VERSION
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

#read the prompt files for the prompt texts
file = open(working_dir + "/" + "init_prompt.txt", "r")
base_prompt = file.read()

# save the llm api key to environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# initialize the chat history as streamlit session state of not present already
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# streamlit page title
st.title("🗺️ Happy Travels")
# streamlit page image
st.image(working_dir + "/" + "Media" + "/" + "Travel_bgd.png", use_column_width = "auto")

# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# input field for user's message:
user_prompt = st.chat_input("Ask Jajabor...")

if user_prompt:

    # display user entered message on screen
    st.chat_message("user").markdown(user_prompt)
    # add user entered message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # send user's message to the LLM and get a response
    messages = [
        {"role": "system", "content": date_context + base_prompt},
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        # model="llama-3.1-70b-versatile",
        model="llama-3.1-8b-instant",
        messages=messages
    )

    assistant_response = response.choices[0].message.content

    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # display the LLM's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)