import streamlit as st
from frontend_utils.api_client import get_backend_health

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
rec_page = st.Page("pages/recommendations.py", title="Karta & Rekommendationer", icon="📍")

pg = st.navigation(
    {
        "Meny": [home_page, agent_page, rec_page]
    }
)

st.sidebar.title("Travel Buddy")
st.sidebar.info ("Din personliga AI-guide")

st.sidebar.divider()
st.sidebar.write("Systemstatus")

health_status = get_backend_health()

if health_status.get("status") == "healthy":
    st.sidebar.success("Backend: Online")
else:
    st.sidebar.error(f"Backend: Offline - {health_status.get('detail')}")


pg.run()
