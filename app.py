import streamlit as st
import random
import matplotlib.pyplot as plt
import pandas as pd
import sys

# --- TTS Setup ---
try:
    import pyttsx3
    tts_mode = "local"
except ImportError:
    from gtts import gTTS
    import os
    tts_mode = "cloud"

def speak(text):
    if tts_mode == "local":
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    else:
        tts = gTTS(text=text, lang='en')
        tts.save("temp.mp3")
        if sys.platform.startswith("win"):
            os.system("start temp.mp3")
        elif sys.platform.startswith("linux"):
            os.system("mpg321 temp.mp3")
        elif sys.platform.startswith("darwin"):
            os.system("afplay temp.mp3")

# --- Streamlit Page Setup ---
st.set_page_config(page_title="🌊 Oceanographic AI Assistant", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

st.title("🌊 Oceanographic AI Assistant")
st.caption("Ask about **salinity**, **temperature**, or **ARGO floats** using voice 🎤 or text ⌨️.")

# --- Voice Input using streamlit-webrtc ---
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import speech_recognition as sr
import numpy as np

query_text = ""

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.r = sr.Recognizer()
        self.query = None

    def recv(self, frame):
        audio = frame.to_ndarray()
        return frame

def get_voice_input():
    webrtc_ctx = webrtc_streamer(key="voice_input")
    st.info("Click **Start** to record, speak your query, then stop.")
    if webrtc_ctx.state.playing:
        st.warning("Recording in progress...")
    if st.button("Transcribe Last Recording"):
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                st.info("Listening for 5 seconds...")
                audio_data = r.listen(source, timeout=5)
                query = r.recognize_google(audio_data)
                st.success(f"🎤 You said: {query}")
                return query
        except Exception as e:
            st.error(f"Could not recognize speech: {e}")
    return None

voice_query = get_voice_input()

# --- Text input fallback ---
user_query = st.text_input("Type your query or use voice input:", value=voice_query if voice_query else "")

# --- Handle query ---
def process_query(query):
    response = ""

    if "salinity" in query.lower():
        st.subheader("📈 Salinity Profile")
        data = [random.uniform(30, 40) for _ in range(12)]
        plt.figure()
        plt.plot(range(1, 13), data, marker="o")
        plt.xlabel("Month")
        plt.ylabel("Salinity (PSU)")
        plt.title("Salinity Profile")
        st.pyplot(plt)
        response = "Here is the salinity profile for the selected region."
        speak(response)

    elif "temperature" in query.lower():
        st.subheader("🌡️ Temperature Profile")
        data = [random.uniform(20, 30) for _ in range(12)]
        plt.figure()
        plt.plot(range(1, 13), data, marker="o", color="red")
        plt.xlabel("Month")
        plt.ylabel("Temperature (°C)")
        plt.title("Temperature Profile")
        st.pyplot(plt)
        response = "Here is the temperature profile for the selected region."
        speak(response)

    elif "float" in query.lower():
        st.subheader("🌍 ARGO Floats Near Your Region")
        df = pd.DataFrame({"lat": [10.0, 12.5, 15.0], "lon": [72.0, 75.5, 78.0]})
        st.map(df)
        response = "Here are the nearby ARGO floats on the map."
        speak(response)

    else:
        response = "🤔 Sorry, I couldn’t understand that. Try asking about salinity, temperature, or floats."
        st.warning(response)
        speak(response)

    st.session_state.history.append({"query": query, "response": response})

# --- Run query if entered ---
if user_query:
    process_query(user_query)

# --- Chat history panel ---
st.sidebar.title("💬 Chat History")
if st.session_state.history:
    for chat in st.session_state.history:
        st.sidebar.markdown(f"**You:** {chat['query']}")
        st.sidebar.markdown(f"**Bot:** {chat['response']}")
else:
    st.sidebar.info("No queries yet. Try asking something!")
