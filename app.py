import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime, timedelta
from streamlit_chat import message

# ---------------------------
# Mock Dataset Generator
# ---------------------------
def generate_mock_data(param="salinity"):
    days = pd.date_range(datetime.now() - timedelta(days=30), datetime.now(), freq="D")
    values = [random.uniform(30, 40) if param=="salinity" else random.uniform(15, 30) for _ in days]
    df = pd.DataFrame({"Date": days, "Value": values})
    return df

# ---------------------------
# Mock ARGO Floats Locations
# ---------------------------
argo_floats = pd.DataFrame({
    "FloatID": ["ARGO-1", "ARGO-2", "ARGO-3"],
    "Lat": [0.5, 15.3, -8.6],
    "Lon": [60.1, 72.5, 80.3],
    "Region": ["Equator", "Arabian Sea", "Indian Ocean"]
})

# ---------------------------
# Query Parser (Simple Keywords)
# ---------------------------
def parse_query(user_input):
    query = user_input.lower()
    if "salinity" in query:
        return "salinity"
    elif "temperature" in query or "temp" in query:
        return "temperature"
    elif "float" in query or "location" in query:
        return "floats"
    else:
        return "unknown"

# ---------------------------
# Streamlit App
# ---------------------------
st.set_page_config(page_title="Ocean AI Chatbot 🌊", layout="wide")
st.title("🌊 Oceanographic AI Chatbot (Prototype)")

# Initialize session state for chat
if "history" not in st.session_state:
    st.session_state.history = []
if "responses" not in st.session_state:
    st.session_state.responses = []
if "queries" not in st.session_state:
    st.session_state.queries = []

# Input field
user_query = st.text_input("Type your question here and press Enter...")

if user_query:
    # Add user query to history
    st.session_state.queries.append(user_query)
    
    query_type = parse_query(user_query)
    response_text = ""
    graph = None
    table = None

    if query_type in ["salinity", "temperature"]:
        df = generate_mock_data(query_type)
        response_text = f"Here is the {query_type} profile you asked for 🌊📊"
        graph = px.line(df, x="Date", y="Value", title=f"{query_type.capitalize()} over Time")

    elif query_type == "floats":
        response_text = "Here are the ARGO floats near your region 🗺️"
        graph = px.scatter_geo(
            argo_floats,
            lat="Lat", lon="Lon",
            hover_name="FloatID",
            text="Region",
            projection="natural earth",
            title="ARGO Floats Map"
        )
        table = argo_floats

    else:
        response_text = "🤔 Sorry, I couldn’t understand that. Try asking about **salinity, temperature, or floats.**"

    st.session_state.responses.append((response_text, graph, table))

# Chat UI
for i in range(len(st.session_state.queries)):
    message(st.session_state.queries[i], is_user=True, key=f"user_{i}")
    resp, graph, table = st.session_state.responses[i]
    message(resp, is_user=False, key=f"bot_{i}")
    if graph:
        st.plotly_chart(graph, use_container_width=True)
    if table is not None:
        st.dataframe(table)
