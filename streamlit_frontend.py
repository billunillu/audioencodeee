# streamlit_app.py

import streamlit as st
import requests
#import time
#import pyaudio
#import wave
#import threading 
from audio_recorder_streamlit import audio_recorder
from io import BytesIO


API_URL = "https://audiofun-187499103525.us-central1.run.app"  # adjust if running Flask elsewhere
#API_URL = "http://127.0.0.1:5000"

st.title("🎶 Hidden Message Encoder/Decoder")

tab1, tab2, tab3 = st.tabs(["step 1, 🔊 Encode Message", "step 2 OPTIONAL!!! 🎤 Record Song","step 3, 🎧 Decode from Microphone"])

with tab1:
    st.header("Encode a Message into a Song")
    uploaded_song = st.file_uploader("Upload a song (WAV or MP3)", type=["wav", "mp3"])
    message = st.text_input("Enter the message to encode [keep it to letters and numbers, no special characters/punctuation]")

    if st.button("Encode"):
        if uploaded_song and message:
            files = {"song": uploaded_song}
            data = {"message": message}
            with st.spinner("Encoding..."):
                response = requests.post(f"{API_URL}/encode", files=files, data=data)
            if response.status_code == 200:
                st.success("✅ Encoded successfully!")
                encoded_bytes = BytesIO(response.content)
                st.download_button("Download Encoded Song", encoded_bytes, file_name="encoded_song.wav")
                st.audio(response.content, format="audio/wav")
                st.markdown("download and then nagivate to step 2")
            else:
                st.error(f"Error: {response.text}")
        else:
            st.warning("Please upload a song and enter a message.")
    
   
with tab2:
    st.title("OPTIONAL 🎙️ Mic Recorder")
    with st.expander("📋 Instructions", expanded=True):
        st.markdown("""
        **How to Record and Proceed:**

        1. 🎤 Click the **microphone icon** to start recording.  
        2. 📁 Navigate to and **play the newly downloaded `.wav` file** to verify your recording.  
        3. ⏹️ Click the **microphone icon again** to stop recording.  
        4. 💾 Click **Download** to save your recording.  
        5. ➡️ Proceed to **Step 3** to upload and decode the audio.
                    
        ---         
        """)

    audio_bytes = audio_recorder()

    if audio_bytes:

        #st.success("Recording complete!")
        st.download_button("Download Encoded Song", audio_bytes, file_name="recording.wav")
        st.audio(audio_bytes, format="audio/wav")
        st.markdown("download and then nagivate to step 3")

with tab3:
    st.header("Decode Song in a Message")
    uploaded_audio = st.file_uploader("Upload an audio file to decode (WAV)", type=["wav"])
    if st.button("Decode Audio"):
        if uploaded_audio is not None:
            files = {
                "file": (uploaded_audio.name, uploaded_audio, "audio/wav")
            }

            flask_url = f"{API_URL}/decode2"

            try:
                response = requests.post(flask_url, files=files)
                if response.status_code == 200:
                    decoded_message = response.json().get("decoded_message", "")
                    st.success(f"Decoded message: {decoded_message}")
                else:
                    st.error(f"Error from server: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Failed to connect to server: {e}")
        else:
            st.warning("Please upload an audio file to decode.")
