"""Agent chat page."""
import streamlit as st
import requests
import pandas as pd
from frontend_utils.api_client import send_chat_message, BACKEND_URL

# Sätt sidlayouten till wide direkt
st.set_page_config(layout="wide")

def reset_chat():
    """Rensar chatten när man byter land manuellt i menyn."""
    st.session_state.messages = []
    st.session_state.agent_history = []
    st.session_state.current_sources = []

def main():
    st.title("Travel Guide Chat")

    # 1. Hämta valt land från det globala minnet (sätts i app.py eller home.py)
    selected_country = st.session_state.get("selected_country", "Japan")
    st.subheader(f"Chatta om {selected_country}")

    # 2. Initiera session_state om det saknas
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent_history" not in st.session_state:
        st.session_state.agent_history = []
    if "current_sources" not in st.session_state:
        st.session_state.current_sources = []
    if "city" not in st.session_state:
        # Standardstad baserat på land
        st.session_state.city = "Athens" if selected_country == "Greece" else "Tokyo"

    # 3. Skapa layout med två kolumner (Chat till vänster, Info till höger)
    chat_col, side_col = st.columns([2, 1])
    city = st.session_state.city

    with chat_col:
        chat_container = st.container(border=True, height=550)
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    with side_col:
        # --- VÄDERSEKTION ---
        st.subheader(f"Väder i {selected_country}")
        with st.container(border=True):
            try:
                response = requests.get(f"{BACKEND_URL}/weather/{selected_country}", timeout=5)
                if response.status_code == 200:
                    w = response.json()
                    c1, c2 = st.columns(2)
                    c1.metric("Temp", f"{w.get('temperature_celsius')} °C")
                    c1.metric("Regnrisk", f"{w.get('precipitation_chance')} %")
                    c2.metric("Väder", f"{w.get('conditions')}")
                    c2.metric("UV Index", f"{w.get('uv_index')}")

                    if w.get("needs_umbrella"):
                        st.warning("Glöm inte paraplyet! ☂️")
                    if w.get("needs_sunscreen"):
                        st.info("Solen steker! Kom ihåg solkräm! 🧴")
                else:
                    st.write("Väderdata kunde inte hämtas.")
            except Exception:
                st.error("Kunde inte ansluta till vädertjänsten.")

        # --- KARTA ---
        with st.container(border=True):
            try:
                res_loc = requests.get(f"{BACKEND_URL}/weather/location/{selected_country}", timeout=5)
                if res_loc.status_code == 200:
                    loc_data = res_loc.json()
                    map_df = pd.DataFrame({"lat": [loc_data.get("lat")], "lon": [loc_data.get("lon")]})
                    st.map(map_df, zoom=10)
            except Exception:
                st.caption("Kartan kunde inte laddas just nu.")

        # --- KÄLLOR ---
        st.subheader("Källor")
        if st.session_state.current_sources:
            for source in st.session_state.current_sources:
                st.info(source)
        else:
            st.caption("Inga källor för denna konversation än.")

    # 4. CHATT-INPUT
    if prompt := st.chat_input("Vad vill du veta?"):
        # Spara och visa användarens meddelande
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

        with st.spinner("Tänker så det knakar..."):
            # Anropa API-klienten med rätt fält (message, country, history)
            result = send_chat_message(
                query=prompt,
                country=selected_country,
                history=st.session_state.agent_history
            )
            
            # Hämta svaret (vi kollar både 'ai' och 'response' för säkerhets skull)
            ai_response = result.get("ai") or result.get("response", "Tyvärr fick jag inget svar.")
            
            # Uppdatera historik, källor och eventuell detekterad stad
            st.session_state.agent_history = result.get("history", [])
            st.session_state.current_sources = result.get("sources", [])
            if result.get("detected_city"):
                st.session_state.city = result.get("detected_city")
            
            # Spara AI-svaret och ladda om sidan för att visa allt
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            st.rerun()

if __name__ == "__main__":
    main()