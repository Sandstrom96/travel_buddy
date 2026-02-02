import streamlit as st

st.set_page_config(
    page_title="Travel Buddy",
    page_icon="✈️",
    layout="wide"
)


page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "🍦 Recommendations", "💬 Agent Chat"]
)

if page == "🏠 Home":
    st.switch_page("pages/home.py")
elif page == "🍦 Recommendations":
    st.switch_page("pages/recommendations.py")
elif page == "💬 Agent Chat":
    st.switch_page("pages/agent_chat.py")