"""Home page."""
import streamlit as st
import requests

def fetch_destinations():
    try:
        response =requests.get("http://backend:8000/destinations", timeout=10)
        if response.status_code == 200:
            return response.json().get("destinations", [])
        else:
            st.error(f"Servern svarade med statuskod: {response.status_code}")
            return []
    except requests.exceptions.ConnectionError:
        st.error("Kunde inte ansluta till backend. är servern igång?")
        return []
    except Exception as e:
        st.error(f"Ett okänt fel uppstod: {e}")
        return []

def main():
    st.title("Upptäck Världen på rätt sätt")
    st.write("Välkommen till Travel Buddy!")
    st.divider()

    destinations = fetch_destinations()

    if not destinations:
        st.info("Inga destinationer kunde laddas just nu.")
        return
    
    for desti in destinations:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])

            with col1:
                name = desti.get("name", "Okänd plats")
                country = desti.get("country", "")
                region = desti.get("region", "")
                desc =desti.get("description", "Ingen beskrivning tillgänglig.")

                location_str = f"{country}"
                if region:
                    location_str += f", {region}"
                
                st.subheader(name)
                st.caption(location_str)
                st.write(desc)
            
            with col2:
                st.write("")
                st.write("")
                st.button("Utforska", key=f"btn_{desti.get('id')}", use_container_width=True)

if __name__ == "__main__":
    main()