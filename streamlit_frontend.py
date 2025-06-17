# streamlit_app.py

import streamlit as st
import requests
import time

API_URL = "http://localhost:5001"  # adjust if running Flask elsewhere

st.title("🎶 Sound Message Encoder/Decoder")

tab1, tab2 = st.tabs(["step 1, 🔊 Encode Message", "step 2, 🎧 Decode from Microphone"])

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
                st.download_button("Download Encoded Song", response.content, file_name="encoded_song.wav")
                st.audio(response.content, format="audio/wav")
                st.markdown("click play and then nagivate to step 2")
            else:
                st.error(f"Error: {response.text}")
        else:
            st.warning("Please upload a song and enter a message.")

with tab2:
    st.header("Decode a Hidden Message")
    
if st.button("Listen and Decode"):
    with st.spinner("Decoding message..."):
        try:
            response = requests.post(f"{API_URL}/decode")
            if response.status_code == 200:
                decoded = response.text.strip()
                st.success("✅ Decoded Message:")
                st.code(decoded, language="text")
            else:
                st.error(f"Error: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Could not reach Flask API: {e}")


            
