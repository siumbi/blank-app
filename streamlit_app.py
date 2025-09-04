import streamlit as st
from streamlit_autorefresh import st_autorefresh

# --- USERS (demo; w prawdziwej aplikacji lepiej z secrets/DB) ---
users = {
    "alice": {"password": "123", "role": "admin"},
    "bob": {"password": "abc", "role": "admin"},
    "charlie": {"password": "xyz", "role": "user"}
}

# --- INIT SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.login_submitted = False

# --- AUTO REFRESH WHEN LOGIN ---
if st.session_state.logged_in and st.session_state.login_submitted:
    # przebuduj tylko raz po zalogowaniu, żeby od razu przejść do strony właściwej
    st_autorefresh(interval=500, limit=1, key="refresh_once")
    st.session_state.login_submitted = False

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
            st.session_state.login_submitted = True
        else:
            st.error("❌ Invalid username or password")

# --- ADMIN PAGES ---
def admin_dashboard():
    st.title("📊 Admin Dashboard")
    st.write("Full access to reports and management tools.")

def manage_users():
    st.title("👥 Manage Users")
    st.write("Here admin could add/remove/edit users (demo placeholder).")

# --- USER PAGES ---
def user_home():
    st.title("👤 User Home")
    st.write("Basic information available for regular users.")

def payments():
    st.title("💳 Payments")
    st.write("Here the user can see their payment status (demo placeholder).")

# --- MAIN APP WITH NAVIGATION ---
def app_pages():
    role = st.session_state.role
    username = st.session_state.username

    st.sidebar.success(f"Logged in as {username} ({role})")

    # Menu zależne od roli
    menu = ["Home", "Admin Dashboard", "Manage Users"] if role == "admin" else ["Home", "Payments"]
    choice = st.sidebar.radio("Navigation", menu)

    # Logout
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.session_state.login_submitted = False

    # Routing
    if choice == "Home":
        if role == "user":
            user_home()
        else:
            st.write(f"Welcome back, {username}!")
    elif choice == "Admin Dashboard":
        admin_dashboard()
    elif choice == "Manage Users":
        manage_users()
    elif choice == "Payments":
        payments()

# --- ROUTER ---
if st.session_state.logged_in:
    app_pages()
else:
    login_page()
