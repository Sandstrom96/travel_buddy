import streamlit as st
from frontend_utils.api_client import APIClient

st.set_page_config(page_title="Recommendations - Travel Buddy", page_icon="🍦", layout="wide")

st.title("🍦 Activity Recommendations")
st.markdown("Get personalized recommendations for ice cream, restaurants, cafes, and temples in Osaka!")

if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient()

st.subheader("📍 Choose  Location")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📍 Dotonbori", use_container_width=True):
        st.session_state.user_lat = 34.6686
        st.session_state.user_lon = 135.5023

with col2:
    if st.button("📍 Osaka Station", use_container_width=True):
        st.session_state.user_lat = 34.6618
        st.session_state.user_lon = 135.4959

with col3:
    if st.button("📍 Namba", use_container_width=True):
        st.session_state.user_lat = 34.6618
        st.session_state.user_lon = 135.5012

# Manual coordinate input
with st.expander(" Enter Custom Coordinates"):
    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input("Latitude", value=34.6937, format="%.4f")
    with col2:
        lon = st.number_input("Longitude", value=135.5023, format="%.4f")
    
    if st.button("Use Custom Location"):
        st.session_state.user_lat = lat
        st.session_state.user_lon = lon
    
if "user_lat" in st.session_state:
    st.info(f"📍 Current location:  {st.session_state.user_lat:.4f}, {st.session_state.user_lon:.4f}")


st.subheader("🎯 What are you looking for?")
activity_type = st.selectbox(
    "Activity Type",
    options=["ice_cream", "restaurant", "cafe", "temple"],
    format_func=lambda x: {
        "ice_cream": "🍦 Ice cream",
        "restaurant": "🍜 Restaurant",
        "cafe": "☕ Cafe",
        "temple": "⛩️ Temple"
    }[x]
)

max_results = st.slider("Number of recommendations", 1, 5, 3)


if st.button("🔍 Get Recommendations", type="primary", use_container_width=True):
    if "user_lat" not in st.session_state:
        st.error("⚠️ Please select a location first!")
    else:
        with st.spinner("Finding the best places for you..."):
            try:
                recommendations = st.session_state.api_client.get_recommendations(
                    user_lat=st.session_state.user_lat,
                    user_lon=st.session_state.user_lon,
                    activity_type=activity_type,
                    max_results=max_results
                )
                st.session_state.recommendations = recommendations
                st.success(f"✅ Found {len(recommendations)} recommendations!")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


if "recommendations" in st.session_state and st.session_state.recommendations:
    st.divider()
    st.subheader("🎯 Your Recommendations")


    if st.session_state.recommendations:
        weather = st.session_state.recommendations[0]["weather"]
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🌡️ Temperature", f"{weather['temperature_celsius']:.1f}°C")
        with col2:
            st.metric("☁️ Conditions", weather['conditions'])
        with col3:
            st.metric("💧 Humidity", f"{weather['humidity']}%")
        with col4:
            st.metric("🌧️ Rain Chance", f"{weather['precipitation_chance']}%")

    st.divider()

    
    for i, rec in enumerate(st.session_state.recommendations, 1):
        place = rec["place"]
        transport = rec["transport_options"]
        score = rec["recommendation_score"]
        reason = rec["reason"]

        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {i}. {place['name']}")
                st.markdown(f"⭐ **Rating:** {place['rating']}/5 | 💰 **Price:** {'¥' * place['price_level']}")
            with col2:
                score_color = "🟢" if score > 0.7 else "🟡" if score > 0.5 else "🔴"
                st.metric("Score", f"{score_color} {score:.2f}")

            st.markdown(f"📍 {place['address']}")
            st.markdown(f"📏 **Distance:** {place['distance_km']} km")
            if place.get('description'):
                st.markdown(f"*{place['description']}*")
            st.info(f"💡 **Why recommended:** {reason}")

            if place.get('menu_items'):
                with st.expander("🍽️ Menu"):
                    for item in place['menu_items']:
                        st.markdown(f"- {item}")

            st.markdown("**🚇 How to get there:**")
            transport_data = []
            for t in transport:
                transport_data.append({
                    "Mode": t['mode'].title(),
                    "Duration": f"{t['duration_minutes']} min",
                    "Price": f"¥{t['price_jpy']}" if t['price_jpy'] > 0 else "Free",
                    "Details": t.get('instructions', 'N/A')
                })
            st.table(transport_data)

            st.divider()

    st.subheader("🗺️ Map View")
    map_data = []
    for rec in st.session_state.recommendations:
        place = rec["place"]
        map_data.append({
            "lat": place["latitude"],
            "lon": place["longitude"]
        })
    st.map(map_data)