import streamlit as st
from frontend_utils.api_client import get_backend_health

st.set_page_config(page_title="Travel Buddy")


with st.sidebar:
    st.title("Travel Buddy")
    health_status = get_backend_health()
    if health_status.get("status") == "healthy":
        st.success("Backend is healthy")
    else:
        st.error(f"Backend is unhealthy: {health_status.get('detail')}")

    st.divider()

home_page = st.Page("pages/home.py", title="Home", default=True)
agent_page = st.Page("pages/agent_chat.py", title="Agent")

pg = st.navigation([home_page, agent_page])

pg.run()
