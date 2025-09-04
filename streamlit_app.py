import streamlit as st

# --- USERS from secrets ---
users = {
    st.secrets["users"]["alice_username"]: {
        "password": st.secrets["users"]["alice_password"],
        "role": st.secrets["users"]["alice_role"]
    },
    st.secrets["users"]["bob_username"]: {
        "password": st.secrets["users"]["bob_password"],
        "role": st.secrets["users"]["bob_role"]
    },
    st.secrets["users"]["charlie_username"]: {
        "password": st.secrets["users"]["charlie_password"],
        "role": st.secrets["users"]["charlie_role"]
    }
}

# --- INIT SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.page = "login"

# --- LOGIN PAGE ---
def login_page():
    st.title("🔑 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.session_state.page = "home"
            st.experimental_rerun()
        else:
            st.error("❌ Invalid username or password")

# --- reszta Twojego kodu pozostaje bez zmian ---
