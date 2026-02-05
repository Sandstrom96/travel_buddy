"""Home page."""

import streamlit as st
import requests
from frontend_utils.settings import settings

BACKEND_URL = settings.BACKEND_URL


def fetch_destinations():

    try:
        response = requests.get(f"{BACKEND_URL}/destinations", timeout=10)
        url = f"{BACKEND_URL}/destinations"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return response.json().get("destinations", [])
        else:
            st.warning(
                f"Kunde inte hämta destinationer (statuskod: {response.status_code})"
            )
            return []
    except requests.exceptions.ConnectionError:
        st.warning(
            "Backend är inte tillgänglig just nu. Starta servern för att se destinationer."
        )
        st.error(f"Kunde inte ansluta till backend på {BACKEND_URL}. Är servern igång?")
        return []
    except Exception as e:
        st.warning(f"Ett fel uppstod: {e}")
        return []


def main():
    st.title("🌍 Upptäck Världen med Travel Buddy")
    st.markdown(
        """
        Välkommen! Här hittar du handplockade destinationer för ditt nästa äventyr. 
        Välj ett land i menyn till vänster för att börja chatta med din personliga guide.
    """
    )
    st.divider()

    destinations = fetch_destinations()

    if not destinations:
        st.info("Hittade inga sparade destinationer. Har du kört din ingestion?")
        return

    cols = st.columns(2)
    for idx, desti in enumerate(destinations):

        with cols[idx % 2]:
            with st.container(border=True):
                name = desti.get("name", "Okänd plats")
                country = desti.get("country", "")
                region = desti.get("region", "")
                desc = desti.get("description", "Ingen beskrivning tillgänglig.")

                location_icon = "📍"
                st.subheader(f"{name}")
                st.caption(
                    f"{location_icon} {country}{f' • {region}' if region else ''}"
                )

                short_desc = (desc[:120] + "...") if len(desc) > 120 else desc
                st.write(short_desc)

                st.button(
                    "Utforska resmål",
                    key=f"btn_{desti.get('id', idx)}",
                    use_container_width=True,
                    type="secondary",
                )


if __name__ == "__main__":
    main()
