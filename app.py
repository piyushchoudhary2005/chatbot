import streamlit as st
import random
import matplotlib.pyplot as plt
import pandas as pd
import sys
from gtts import gTTS
import io

# --- Streamlit Page Setup ---
st.set_page_config(page_title="🌊 Oceanographic AI Assistant", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

st.title("🌊 Oceanographic AI Assistant")
st.caption("Ask about **salinity**, **temperature**, or **ARGO floats** using text or voice input 🎤.")

# --- Browser-safe TTS ---
def speak(text):
    """
    Convert text to speech and play in browser using Streamlit audio
    """
    tts = gTTS(text=text, lang='en')
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    st.audio(mp3_fp, format="audio/mp3")

# --- Voice Input using microphone ---
voice_query = None
if st.button("🎤 Speak your query"):
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening for 5 seconds...")
            audio_data = r.listen(source, timeout=5)
            voice_query = r.recognize_google(audio_data)
            st.success(f"🎤 You said: {voice_query}")
    except Exception as e:
        st.error(f"Could not recognize speech: {e}")

# --- User Input ---
user_query = st.text_input("Type your query here:", value=voice_query if voice_query else "")

# --- Process Query ---
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
        # Mock map data
        df = pd.DataFrame({
            "lat": [10.0, 12.5, 15.0],
            "lon": [72.0, 75.5, 78.0],
            "ID": ["ARGO-001", "ARGO-002", "ARGO-003"],
            "Region": ["Arabian Sea", "Arabian Sea", "Arabian Sea"]
        })
        st.map(df[["lat", "lon"]])
        st.table(df[["ID", "Region"]])
        response = "Here are the nearby ARGO floats on the map with IDs and regions."
        speak(response)

    else:
        response = "🤔 Sorry, I couldn’t understand that. Try asking about salinity, temperature, or floats."
        st.warning(response)
        speak(response)

    # Save to chat history
    st.session_state.history.append({"query": query, "response": response})

# --- Run query if submitted ---
if user_query:
    process_query(user_query)

# --- Display Chat History ---
st.subheader("💬 Chat History")
for chat in st.session_state.history:
    st.markdown(f"**You:** {chat['query']}")
    st.markdown(f"**Bot:** {chat['response']}")
    st.markdown("---")







