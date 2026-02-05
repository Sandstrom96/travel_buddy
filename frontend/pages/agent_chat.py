import streamlit as st
import requests
import pandas as pd
from frontend_utils.settings import settings

if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_history" not in st.session_state:
    st.session_state.agent_history = []
if "current_sources" not in st.session_state:
    st.session_state.current_sources = []
if "city" not in st.session_state:
    st.session_state.city = "Göteborg"


st.set_page_config(layout="wide")

st.title("Travel Buddy Chat")

# Skapa kolumner 2 delar till vänster, 1 del till höger
chat_col, side_col = st.columns([2, 1])
city = st.session_state.city

with chat_col:
    st.subheader("Chat")

    chat_container = st.container(border=True, height=500)

    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])


with side_col:

    st.subheader(f"Weather in {city}")
    with st.container(border=True):

        try:
            response = requests.get(f"{settings.BACKEND_URL}/weather/{city}")

            if response.status_code == 200:
                weather_data = response.json()

                col1, col2 = st.columns(2)
                col1.metric(
                    "Temperature", f"{weather_data.get('temperature_celsius')} °C"
                )
                col2.metric("condition", f"{weather_data.get('conditions')}")

                col1.metric(
                    "Min Temp", f"{weather_data.get('daily_min_temperature')} °C"
                )
                col2.metric(
                    "Max Temp", f"{weather_data.get('daily_max_temperature')} °C"
                )

                col1.metric(
                    "Precipitation Chance",
                    f"{weather_data.get('precipitation_chance')} %",
                )
                col2.metric("UV Index", f"{weather_data.get('uv_index')}")

                if weather_data.get("needs_umbrella"):
                    st.warning("Don't forget to bring an umbrella! ☂️")

                if weather_data.get("needs_sunscreen"):
                    st.info("It's sunny outside! Remember to apply sunscreen! 🧴")

            else:
                st.error("Failed to fetch weather data.")

        except Exception as e:
            st.error("Weather API connection failed.")

    try:
        response = requests.get(f"{settings.BACKEND_URL}/weather/location/{city}")

        with st.container(border=True):
            if response.status_code == 200:
                data = response.json()

                map_data = pd.DataFrame(
                    {"lat": [data.get("lat")], "lon": [data.get("lon")]}
                )
                st.map(map_data, zoom=10, width="stretch")
            else:
                st.error("Failed to fetch map data.")

    except Exception as e:
        st.error("Coordinates API connection failed.")

    st.subheader("Sources")
    if st.session_state.current_sources:
        for source in st.session_state.current_sources:
            st.info(source)
    else:
        st.write("No sources for the current conversation yet.")

if user_input := st.chat_input("Your Question:"):
    with chat_col:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)

            payload = {
                "message": user_input,
                "country": st.session_state.selected_country,
                "history": st.session_state.agent_history,
            }

            with st.spinner("Searching..."):
                response = requests.post(
                    f"{settings.BACKEND_URL}/agent/chat", json=payload
                )

            if response.status_code == 200:
                data = response.json()
                ai_response = data["ai"]

                st.session_state.agent_history = data["history"]
                st.session_state.current_sources = data.get("sources", [])
                st.session_state.city = data.get("detected_city", st.session_state.city)
                st.session_state.messages.append(
                    {"role": "assistant", "content": ai_response}
                )

                with st.chat_message("assistant"):
                    st.markdown(ai_response)

    st.rerun()
