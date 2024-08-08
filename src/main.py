import streamlit as st
import requests
import base64
from translator_utils import translate


st.set_page_config(
    page_title="Translator.AI",
    page_icon="🈶",
    layout="centered"
)

# Streamlit page title
st.title("🈶 Translator App  - GPT-4o")

col1, col2 = st.columns(2)

with col1:
    input_languages_list = ["English", "Sanskrit"]
    input_language = st.selectbox(label="Input Language", options=input_languages_list)

with col2:
    output_languages_list = [x for x in input_languages_list if x != input_language]
    output_language = st.selectbox(label="Output Language", options=output_languages_list)

input_text = st.text_area("Type the text to be translated")

if st.button("Translate"):
    translated_text = translate(input_language, output_language, input_text)
    st.success(translated_text)

# Adding Text-to-Speech Functionality
st.header("Text-to-Speech")
text_for_speech = st.text_input("Enter text for speech synthesis:")

def text_to_speech(text):
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }
    
    data = {
        'model': 'tts-1',
        'input': text,
        'voice': 'alloy',
    }

    response = requests.post('https://api.openai.com/v1/audio/speech', headers=headers, json=data, stream=True)
    
    if response.status_code == 200:
        return base64.b64encode(response.content).decode('utf-8')
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

if st.button("Generate Speech"):
    if text_for_speech:
        audio_base64 = text_to_speech(text_for_speech)
        if audio_base64:
            audio_bytes = base64.b64decode(audio_base64)
            st.audio(audio_bytes, format='audio/mpeg')
        else:
            st.error("Failed to generate speech.")
    else:
        st.error("Please provide the text for speech synthesis.")
