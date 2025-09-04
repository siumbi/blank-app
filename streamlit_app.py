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

# --- LOGIN PAGE ---
def login_page():
    st.title("🔑 Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if username in users and users[username]["password"] == password:
                # ustawiamy stan sesji
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = users[username]["role"]
                # natychmiast przebudowujemy aplikację
                st.experimental_rerun()
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

    if role == "admin":
        menu = ["Home", "Admin Dashboard", "Manage Users"]
    else:
        menu = ["Home", "Payments"]

    choice = st.sidebar.radio("Navigation", menu)

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.experimental_rerun()

    # ROUTING
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
