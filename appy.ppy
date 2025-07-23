import streamlit as st
import requests
from io import BytesIO
from pydub import AudioSegment

# === YOUR API KEY HERE ===
API_KEY = "sk_079e3e853ca2e92309cef079e2a3adbb36d55c845cc36712"

# === VOICE OPTIONS ===
voice_options = {
    "Rachel (female, natural)": "21m00Tcm4TlvDq8ikWAM",
    "Bella (female, energetic)": "EXAVITQu4vr4xnSDxMaL",
    "Antoni (male, calm)": "ErXwobaYiN019PkySvjV",
    "Elli (child-like, high)": "MF3mGyEYCl7XYWbV9V6O",
    "Josh (male, narrator)": "TxGEqnHWrfWFTfGW9XjX",
}

# === Streamlit Interface ===
st.title("📖 Audiobook TTS Reader")

# Text content (you can add more chapters here)
chapter_text = """
Once upon a time in a land far, far away, there was a curious fox who wanted to explore the world beyond the forest...
"""

# Dropdown to select voice
selected_voice = st.selectbox("🎤 Choose a voice", list(voice_options.keys()))
voice_id = voice_options[selected_voice]

# Button to trigger TTS
if st.button("🔊 Play with ElevenLabs Voice"):
    with st.spinner("Generating audio..."):
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers={
                "xi-api-key": API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "text": chapter_text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.4,
                    "similarity_boost": 0.7
                }
            }
        )
        if response.status_code == 200:
            audio = AudioSegment.from_file(BytesIO(response.content), format="mp3")
            audio.export("output.mp3", format="mp3")
            audio_bytes = BytesIO()
            audio.export(audio_bytes, format='mp3')
            st.audio(audio_bytes, format='audio/mp3')
        else:
            st.error(f"⚠️ Failed to generate audio: {response.status_code} - {response.text}")
