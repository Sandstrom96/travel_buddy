import streamlit as st

st.set_page_config(
    page_title="Travel Buddy",
    page_icon="✈️",
    layout="wide",
)

home_page = st.Page(
    "pages/home.py",
    title="Hem",
    icon="🏠",
    default=True
)

agent_page = st.Page(
    "pages/agent_chat.py",
    title="Chat",
    icon="💬"
)
rec_page = st.Page("pages/recommendations.py", title= "Rekommendationer", icon="📍")

pg = st.navigation(
    {
        "Meny": [home_page, agent_page, rec_page]
    }
)

st.sidebar.title("Travel Buddy")
st.sidebar.info ("Din personliga AI-guide")


pg.run()
