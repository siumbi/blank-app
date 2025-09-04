import streamlit as st

# --- USERS from secrets ---
users = {}
for user_key, user_data in st.secrets["users"].items():
    users[user_data["username"]] = {
        "password": user_data["password"],
        "role": user_data["role"]
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

# --- reszta Twojego kodu (app_pages, routing) pozostaje bez zmian ---

if st.session_state.page == "login":
    login_page()
else:
    if st.session_state.logged_in:
        app_pages()
    else:
        st.session_state.page = "login"
        st.experimental_rerun()
