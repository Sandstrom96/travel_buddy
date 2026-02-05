import streamlit as st
from frontend_utils.api_client import get_backend_health

if "selected_country" not in st.session_state:
    st.session_state.selected_country = "Japan"

st.sidebar.title("Travel Buddy")
st.session_state.selected_country = st.sidebar.selectbox(
    "Välj Land", ["Japan", "Greece"], index=0
)

home_page = st.Page("pages/home.py", title="Hem", icon="🏠", default=True)
agent_page = st.Page("pages/agent_chat.py", title="Chat", icon="💬")
rec_page = st.Page("pages/recommendations.py", title="Recommendations")


pg = st.navigation([home_page, agent_page])

st.sidebar.divider()
st.sidebar.write("Systemstatus")


pg.run()
