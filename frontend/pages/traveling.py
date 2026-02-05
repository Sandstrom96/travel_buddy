import streamlit as st
import pandas as pd
from frontend_utils.api_client import APIClient


def main():
    st.title("✈️ Travel Planning")
    st.write("Find airports and plan transport to your hotel")


    st.subheader("Select city")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🏙️ Osaka", use_container_width=True):
            st.session_state.selected_city = "osaka"
    with col2:
        if st.button("🗼 Tokyo", use_container_width=True):
            st.session_state.selected_city = "tokyo"
    with col3:
        if st.button("⛩️ Kyoto", use_container_width=True):
            st.session_state.selected_city = "kyoto"

    
    if "selected_city" not in st.session_state:
        st.session_state.selected_city = "osaka"

    city = st.session_state.selected_city
    st.info(f"Showing information for: **{city.title()}**")

    st.divider()

    airports = APIClient.get_airports(city)
    hotel_areas = APIClient.get_hotels_areas(city)

    if not airports or not hotel_areas:
        st.error("Could not fetch data from server. Check that backend is running.")
        return
        
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📍 Airports")
        for airport in airports:
            with st.container(border=True):
                st.markdown(f"**{airport['code']}** - {airport['name']}")
                st.caption(f"Distance to city center: {airport['distance_to_city_center_km']} km")

    with col_right:
        st.subheader("🏨 Hotel Areas")
        for area in hotel_areas:
            with st.container(border=True):
                st.markdown(f"**{area['name']}**")
                st.caption(area.get('description', ''))
    
    st.divider()

    st.subheader("🚆 Calculate Transport")

    col_select1, col_select2 = st.columns(2)

    with col_select1:
        selected_airport = st.selectbox(
            "Select airport",
            options=airports,
            format_func=lambda x: f"{x['code']} - {x['name']}"
        )

    with col_select2:
        selected_hotel = st.selectbox(
            "Select hotel area",
            options=hotel_areas,
            format_func=lambda x: x['name']
        )

    if st.button("🔍 Calculate transport", type="primary", use_container_width=True):
        with st.spinner("Calculating transport options..."):
            transport_options = APIClient.get_transport_route(
                selected_airport['latitude'],
                selected_airport['longitude'],
                selected_hotel['latitude'],
                selected_hotel['longitude']
            )

            if transport_options:
                st.success(f"Found {len(transport_options)} transport options")

                for option in transport_options:
                    with st.container(border=True):
                        col_icon, col_info = st.columns([1, 4])

                        with col_icon:
                            icons = {"train": "🚆", "bus": "🚌", "taxi": "🚕", "metro": "🚇"}
                            st.markdown(f"## {icons.get(option['mode'], '🚗')}")

                        with col_info:
                            st.markdown(f"**{option.get('route_name', option['mode'].title())}**")

                            col_time, col_price, col_dist = st.columns(3)
                            with col_time:
                                st.metric("Time", f"{option['duration_minutes']} min")
                            with col_price:
                                st.metric("Price", f"¥{option['price_jpy']}")
                            with col_dist:
                                st.metric("Distance", f"{option.get('distance_km', 0):.1f} km")
                            
                            if option.get('instructions'):
                                st.caption(option['instructions'])
            else:
                st.warning("No transport options found")
    
    st.divider()
    st.subheader("🗺️ Map")

    map_data = []
    for airport in airports:
        map_data.append({
            "lat": airport['latitude'],
            "lon": airport['longitude']
        })
    for area in hotel_areas:
        map_data.append({
            "lat": area['latitude'],
            "lon": area['longitude']
        })

    if map_data:
        st.map(pd.DataFrame(map_data))

if __name__ == "__main__":
    main()
