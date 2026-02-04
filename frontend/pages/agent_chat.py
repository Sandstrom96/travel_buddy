"""Agent chat page."""
import streamlit as st
from frontend_utils.api_client import send_chat_message


def main():
    st.title("Travel Guide Chat")
    st.write("Planera din nästa resa med vår AI-Expert!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Vad vill du veta?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Tänker så det knakar!!"):
                ai_response = send_chat_message(prompt)
                st.markdown(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})


if __name__ == "__main__":
    main()
