import streamlit as st
import sys
sys.path.append('.')

from views import home, recommendations, agent_chat

st.set_page_config(
    page_title="Travel Buddy",
    page_icon="✈️",
    layout="wide"
)

st.markdown("""
<style>
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        font-size: 1.4rem !important;
    }
    [data-testid="stSidebar"] .row-widget label {
        font-size: 1.4rem !important;
    }
    [data-testid="stSidebar"] .row-widget p {
        font-size: 1.4rem !important;
    }
    /* Add spacing between radio buttons */
    [data-testid="stSidebar"] .row-widget label {
        margin-bottom: 1rem !important;
        padding: 0.5rem 0 !important;
    }
    [data-testid="stSidebar"] [role="radiogroup"] label {
        margin-bottom: 1.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("## Navigation")
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "🍦 Recommendations", "💬 Agent Chat"],
    label_visibility="collapsed"
)

if page == "🏠 Home":
    home.main()
elif page == "🍦 Recommendations":
    recommendations.main()
elif page == "💬 Agent Chat":
    agent_chat.main()