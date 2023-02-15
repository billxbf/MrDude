# streamlit application for a chatbot

import os
import streamlit as st
from src.request.openai_api import OpenAI_Completion
from src.request.elevenlabs_api import ElevenLabs_TTS
from src.utils import *
from mutagen.mp3 import MP3
import threading
import time
import base64

if not os.path.exists("/tmp/mrdude"):
    os.makedirs("/tmp/mrdude")



def playResponseAudio(response):
    if response is not None:
        file_path = "/tmp/mrdude/response.mp3"
        tts.saveTTS(response, file_path)
        soundlen = MP3(file_path).info.length
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            sound = st.empty()
            sound.markdown(
                md,
                unsafe_allow_html=True,
            )
            time.sleep(soundlen+0.1)
            sound.empty()


@st.cache_data(show_spinner=False)
def getResponseAndPlayAudio(prompt, isInitial=False):
    if isInitial:
        response = openai.initialResonse()
        playResponseAudio(response)
    else:
        response = openai.getResponse(prompt)
        playResponseAudio(response)

    return response

## Setups
st.session_state["SESSION_STARTED"] = 0 if "SESSION_STARTED" not in st.session_state else st.session_state["SESSION_STARTED"]
st.session_state["RESPONSE_HISTORY"] = [] if "RESPONSE_HISTORY" not in st.session_state else st.session_state["RESPONSE_HISTORY"]
st.session_state["PROMPT_HISTORY"] = [] if "PROMPT_HISTORY" not in st.session_state else st.session_state["PROMPT_HISTORY"]
st.session_state["STEP"] = 0 if "STEP" not in st.session_state else st.session_state["STEP"]

## Set the main UI layout
st.set_page_config(page_title="MrDude", page_icon=":robot:", layout="wide")
_, col1, _, col2 = st.columns([1,3,1,2])

## Sidebar Options
st.sidebar.title("MrDude Options")
character_input = st.sidebar.text_input("Describe your Dude", value='helpful, creative, clever, and very friendly')
os.environ['OPENAI_API_KEY'] = st.sidebar.text_input("OpenAI API Key", value= "",type="password")
os.environ['ELEVENLABS_API_KEY'] = st.sidebar.text_input("ElevenLabs API Key", value="", type="password")
submit = st.sidebar.button("Start Chat", key="start_chat")
if submit:
    st.session_state["SESSION_STARTED"] = 1

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
voice = st.sidebar.selectbox("Voice", ["Adam", "Arnold", "Bella", "Elli", "Josh", "Rachel", "Sam"])
if "CUSTOM_VOICE_ID" not in st.session_state or st.session_state["CUSTOM_VOICE_ID"] is None:
    tts.voice_id = voice_id_flag(voice)
else:
    print(st.session_state["CUSTOM_VOICE_ID"])
    tts.voice_id = st.session_state["CUSTOM_VOICE_ID"]
uploaded_file = st.sidebar.file_uploader("Custom Voice", type=["mp3"])

if st.sidebar.button("Clone", key="clone_voice"):
    if uploaded_file is not None:
        with open("/tmp/mrdude/custom_voice.mp3", "wb") as f:
            f.write(uploaded_file.read())
        voice_id = tts.addVoice("custom_voice", "/tmp/mrdude/custom_voice.mp3")
        tts.useVoice(voice_id)
        st.session_state["CUSTOM_VOICE_ID"] = voice_id
        st.sidebar.success("Voice cloned successfully")
    else:
        st.sidebar.write("No file uploaded")


## Column 1: Chatbot
col1.image("resource/avatar/cheems.gif", use_column_width=True)

if st.session_state["SESSION_STARTED"] == 1:
    response = getResponseAndPlayAudio("", isInitial=True)
    col2.write("MrDude: " + response + "\n")

    prompt = col1.text_input("press Enter to send message", key="chat")
    if prompt:
        st.session_state["STEP"] += 1
        response = getResponseAndPlayAudio(prompt)
        st.session_state["PROMPT_HISTORY"].append(prompt)
        st.session_state["RESPONSE_HISTORY"].append(response)
        
        for i in range(len(st.session_state["PROMPT_HISTORY"])):
            col2.write("You: " + st.session_state["PROMPT_HISTORY"][i])
            col2.write("MrDude: " + st.session_state["RESPONSE_HISTORY"][i])




