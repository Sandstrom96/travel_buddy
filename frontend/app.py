import streamlit as st

if "selected_country" not in st.session_state:
    st.session_state.selected_country = "Japan"

st.sidebar.title("Travel Buddy")
options = ["Japan", "Greece"]
try:
    current_idx = options.index(st.session_state.selected_country)
except ValueError:
    current_idx = 0

selected = st.sidebar.selectbox(
    "Välj Land", 
    options, 
    index=current_idx
)
# Uppdatera session state manuellt
st.session_state.selected_country = selected

home_page = st.Page("pages/home.py", title="Hem", icon="🏠", default=True)
agent_page = st.Page("pages/agent_chat.py", title="Chat", icon="💬")
rec_page = st.Page("pages/recommendations.py", title="Recommendations", icon="📍")


pg = st.navigation([home_page, agent_page, rec_page])
pg.run()