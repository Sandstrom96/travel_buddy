import streamlit as st
from frontend.frontend_utils.api_client import APIClient

def main():
    st.title("💬 Travel Guide Chat")
    st.markdown("Ask your AI travel guide anything about traveling to Japan!")

    if "api_client" not in st.session_state:
        st.session_state.api_client = APIClient()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "example_questions" not in st.session_state:
        try:
            examples = st.session_state.api_client.get_example_questions()
            st.session_state.example_questions = examples.get("example_questions", [])
        except:
            st.session_state.example_questions = []

    with st.sidebar:
        st.subheader("🎯 Filter by Destination")
        destination_filter = st.selectbox(
            "Destination (optional)",
            options=[None, "Tokyo", "Kyoto", "Osaka"],
            format_func=lambda x: "All destinations" if x is None else x
        )

        st.divider()

        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

        st.divider()

        if st.session_state.example_questions:
            st.subheader("💡 Example Questions")
            for example in st.session_state.example_questions:
                if st.button(f"💭 {example}", key=f"example_{example}", use_container_width=True):
                    st.session_state.pending_message = example
                    st.rerun()

    st.subheader("📝 Conversation")

    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.markdown(message["content"])

                    if "sources" in message and message["sources"]:
                        with st.expander(f"📚 Sources ({len(message['sources'])} references)"):
                            for i, source in enumerate(message["sources"], 1):
                                st.markdown(f"**Source {i}:**")
                                st.markdown(f"*{source.get('text', 'N/A')}*")
                                if source.get('destination'):
                                    st.markdown(f"📍 **Destination:** {source['destination']}")
                                if source.get('url'):
                                    st.markdown(f"🔗 [Learn more]({source['url']})")
                                st.divider()

                    if "context_used" in message:
                        st.caption(f"ℹ️ Used {message['context_used']} context sources")    
                        
    if "pending_message" in st.session_state:
        user_message = st.session_state.pending_message
        del st.session_state.pending_message

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_message
        })

        with st.spinner("🤔 Thinking..."):
            try:
                response = st.session_state.api_client.chat_with_agent(
                    message=user_message,
                    destination=destination_filter
                )

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response["response"],
                    "sources": response.get("sources", []),
                    "context_used": response.get("context_used", 0)
                })

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

            st.rerun()

    user_input = st.chat_input("Ask me anything about traveling to Japan...")

    if user_input:
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        with st.spinner("🤔 Thinking..."):
            try:
                response = st.session_state.api_client.chat_with_agent(
                    message=user_input,
                    destination=destination_filter
                )

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response["response"],
                    "sources": response.get("sources", []),
                    "context_used": response.get("context_used", 0)
                })

            except Exception as e: 
                st.error(f"❌ Error: {str(e)}")

        st.rerun()

    if not st.session_state.chat_history:
        st.info("👋 Welcome! Ask me anything about traveling to Japan, or click on an example question to get started.")