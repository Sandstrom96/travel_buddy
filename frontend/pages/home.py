"""Home page."""
import streamlit as st
from frontend_utils.api_client import BACKEND_URL

def main():
    # --- HERO SEKTION ---
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0rem;">
            <h1 style="font-size: 3rem;">🌍 Travel Buddy</h1>
            <p style="font-size: 1.3rem; color: #555;">
                Din intelligenta reskamrat som hjälper dig att planera, utforska och upptäcka 
                världens mest fascinerande platser med hjälp av AI.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    # --- VAD GÖR APPEN? ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🤖 AI-Guide")
        st.write("Ställ frågor om kultur, mat och praktiska tips direkt till vår expert.")
    with col2:
        st.subheader("📍 Upptäck")
        st.write("Hitta noga utvalda sevärdheter och dolda pärlor i våra favoritländer.")
    with col3:
        st.subheader("🗺️ Planera")
        st.write("Få personliga rekommendationer skräddarsydda efter din resestil.")

    st.divider()

    # --- DESTINATIONER (Grekland & Japan) ---
    st.subheader("Vart vill du resa?")
    
    col_left, col_right = st.columns(2)
    
    # Grekland Section
    with col_left:
        with st.container(border=True):
            st.header("🇬🇷 Grekland")
            st.write("""
                Välkommen till civilisationens vagga. Njut av kristallblått vatten, 
                vitkalkade hus i Kykladerna och historiska skatter i Aten. 
                Grekland är det perfekta valet för både historieälskare och soldyrkare.
            """)
            if st.button("Utforska Grekland", use_container_width=True, type="primary"):
                st.session_state.selected_country = "Greece"
                st.session_state.messages = []
                st.session_state.agent_history = []
                st.switch_page("pages/agent_chat.py")

    # Japan Section
    with col_right:
        with st.container(border=True):
            st.header("🇯🇵 Japan")
            st.write("""
                Från de neonljusa gatorna i Tokyo till Kyotos fridfulla tempel. 
                Japan erbjuder en unik blandning av futuristisk teknik och uråldrig tradition. 
                Upplev världens bästa mat, snabba tåg och enastående natur.
            """)
            if st.button("Utforska Japan", use_container_width=True, type="primary"):
                st.session_state.selected_country = "Japan"
                st.session_state.messages = []
                st.session_state.agent_history = []
                st.switch_page("pages/agent_chat.py")

    st.info("Fler destinationer kommer snart!")
    st.divider()

    # --- FOOTER ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.caption("🤖 **Modell:** Gemini Pro Powered")
    with c2:
        st.caption("⚡ **Svarstid:** < 5s")
    with c3:
        st.caption("📅 **Uppdaterad:** 2026")

if __name__ == "__main__":
    main()