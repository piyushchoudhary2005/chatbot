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

# --- Custom CSS for floating mic button ---
st.markdown("""
    <style>
    .mic-button {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background-color: #0078ff;
        border-radius: 50%;
        width: 70px;
        height: 70px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        cursor: pointer;
        z-index: 9999;
    }
    .mic-button:hover { background-color: #0056b3; }
    .mic-button i { color: white; font-size: 30px; line-height: 70px; }
    </style>
    <div class="mic-button" onclick="startRecognition()">
        <i>🎤</i>
    </div>
    <script>
    function startRecognition() {
        var recognition = new webkitSpeechRecognition();
        recognition.lang = "en-US";
        recognition.onresult = function(event) {
            var userSpeech = event.results[0][0].transcript;
            var inputBox = window.parent.document.querySelector('input[type="text"]');
            inputBox.value = userSpeech;
            inputBox.dispatchEvent(new Event('input', { bubbles: true }));
        }
        recognition.start();
    }
    </script>
""", unsafe_allow_html=True)

# --- Title ---
st.title("🌊 Oceanographic AI Assistant")
st.caption("Ask about **salinity**, **temperature**, or **ARGO floats** using voice 🎤 or text ⌨️.")

# --- Text input fallback ---
user_query = st.text_input("Type your query or click the 🎤 button:")

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





