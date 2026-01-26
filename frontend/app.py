import streamlit as st

st.set_page_config(page_title="Travel Buddy")

home_page = st.Page("pages/home.py", title="Home", default=True)
agent_page = st.Page("pages/agent_chat.py", title="Agent")

pg = st.navigation([home_page, agent_page])

pg.run()
