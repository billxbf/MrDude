# streamlit application for a chatbot

import os
import streamlit as st
from src.request.openai_api import OpenAI_Completion
from src.request.elevenlabs_api import ElevenLabs_TTS
from src.utils import *
import time
import base64

if not os.path.exists("/tmp/mrdude"):
    os.makedirs("/tmp/mrdude")


def playResponseAudio(response):
    if response is not None:
        file_path = "/tmp/mrdude/response.mp3"
        tts.saveTTS(response, file_path)
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(
                md,
                unsafe_allow_html=True,
            )

## Setups
if "SESSION_STARTED" not in os.environ:
    os.environ["SESSION_STARTED"] = "0"

## Set the main UI layout
st.set_page_config(page_title="MrDude", page_icon=":robot:", layout="wide")
_, col1, _, col2 = st.columns([1,3,1,2])

## Sidebar Options
st.sidebar.title("MrDude Options")
character_input = st.sidebar.text_input("Describe your Dude", value='helpful, creative, clever, and very friendly')
os.environ['OPENAI_API_KEY'] = st.sidebar.text_input("OpenAI API Key", value= "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",type="password")
os.environ['ELEVENLABS_API_KEY'] = st.sidebar.text_input("ElevenLabs API Key", value="cf9348f2189c5fefaa0b2dc9779aa561", type="password")
submit = st.sidebar.button("Start Chat", key="start_chat")
if submit:
    os.environ["SESSION_STARTED"] = "1"

openai = OpenAI_Completion(character=character_input)
tts = ElevenLabs_TTS()

st.sidebar.title("GPT-3 Options")
openai.model = st.sidebar.selectbox("Model", ["text-davinci-003", "text-curie-001", "text-babbage-001", "text-ada-001"])
openai.max_tokens = st.sidebar.slider("Max Tokens", 1, 1000, 100)
openai.temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.5)
openai.top_p = st.sidebar.slider("Top P", 0.0, 1.0, 1.0)
openai.frequency_penalty = st.sidebar.slider("Frequency Penalty", -2.0, 2.0, 0.0)
openai.presence_penalty = st.sidebar.slider("Presence Penalty", -2.0, 2.0, 0.0)

st.sidebar.title("Voice Options")
tts.voice = st.sidebar.selectbox("Voice", ["Adam", "Arnold", "Bella", "Elli", "Josh", "Rachel", "Sam"])
uploaded_file = st.sidebar.file_uploader("Custom Voice", type=["mp3"])

if st.sidebar.button("Clone", key="clone_voice"):
    if uploaded_file is not None:
        with open("/tmp/mrdude/custom_voice.mp3", "wb") as f:
            f.write(uploaded_file.read())
        voice_id = tts.addVoice("custom_voice", "/tmp/mrdude/custom_voice.mp3")
        tts.useVoice(voice_id)
        st.sidebar.success("Voice cloned successfully")
    else:
        st.sidebar.write("No file uploaded")


## Column 1: Chatbot
col1.image("resource/avatar/cheems.gif", use_column_width=True)

if os.environ["SESSION_STARTED"] == "1":
    response = openai.initialResonse()
    playResponseAudio(response)
    col2.write("MrDude: " + response + "\n")


    inputbox = col1.empty()
    while True:
        prompt = inputbox.text_input("press Enter to send message", key="chat")
        if prompt:
            col2.write("You: " + prompt + "\n")
            response = openai.getResponse(prompt)
            playResponseAudio(response)
            col2.write("MrDude: " + response + "\n")
        inputbox.empty()



# # Add the user-input box
# prompt = st.text_input("Ask me anything!")

# # Add the button to send the user-input
# if st.button("Submit"):
#     response = "HI"
#     st.write("Bot:", response)


