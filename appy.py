import streamlit as st
import requests
from io import BytesIO
from pydub import AudioSegment
from docx import Document

# === ElevenLabs API Key ===
API_KEY = "sk_079e3e853ca2e92309cef079e2a3adbb36d55c845cc36712"

# === Voice Options ===
voice_options = {
    "Rachel (female, natural)": "21m00Tcm4TlvDq8ikWAM",
    "Bella (female, energetic)": "EXAVITQu4vr4xnSDxMaL",
    "Antoni (male, calm)": "ErXwobaYiN019PkySvjV",
    "Elli (child-like, high)": "MF3mGyEYCl7XYWbV9V6O",
    "Josh (male, narrator)": "TxGEqnHWrfWFTfGW9XjX",
}

st.set_page_config(page_title="Audiobook TTS", layout="centered")
st.title("📖 Upload & Listen to Any Text")

# === File Upload ===
uploaded_file = st.file_uploader("📂 Upload a .txt or .docx file", type=["txt", "docx"])

text = ""

if uploaded_file:
    if uploaded_file.type == "text/plain":
        text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
    else:
        st.warning("⚠️ Unsupported file type.")

# Show extracted text
if text:
    st.subheader("📄 Extracted Text")
    st.text_area("Text from file", text, height=300)

# Select voice
selected_voice = st.selectbox("🎤 Choose a voice", list(voice_options.keys()))
voice_id = voice_options[selected_voice]

# Play button
if st.button("🔊 Generate Audio"):
    if not text.strip():
        st.warning("⚠️ Please upload a file or enter text.")
    else:
        with st.spinner("Generating audio..."):
            response = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                headers={
                    "xi-api-key": API_KEY,
                    "Content-Type": "application/json"
                },
                json={
                    "text": text[:2500],  # ElevenLabs limit: 2500 characters
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {
                        "stability": 0.4,
                        "similarity_boost": 0.7
                    }
                }
            )
            if response.status_code == 200:
                audio = AudioSegment.from_file(BytesIO(response.content), format="mp3")
                audio_bytes = BytesIO()
                audio.export(audio_bytes, format='mp3')
                st.audio(audio_bytes, format='audio/mp3')
                st.success("✅ Audio generated!")
            else:
                st.error(f"⚠️ Failed to generate audio: {response.status_code} - {response.text}")
