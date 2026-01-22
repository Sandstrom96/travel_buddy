"""Streamlit main application."""
import streamlit as st


def main():
    """Main Streamlit application."""
    st.set_page_config(page_title="Travel Buddy", layout="wide")
    st.title("🌍 Travel Buddy")
    st.write("AI-powered travel guide and recommendations")


if __name__ == "__main__":
    main()
