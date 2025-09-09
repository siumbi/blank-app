import streamlit as st
import pandas as pd
import pyodbc

# --- SESSION STATE INIT ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None

# --- DB CONNECTION ---
def get_connection():
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={st.secrets['db_server']};"
        f"DATABASE={st.secrets['db_name']};"
        f"UID={st.secrets['db_user']};"
        f"PWD={st.secrets['db_password']};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )
    return conn

# --- HELPERS ---
def get_table_names():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

def load_table(table_name):
    conn = get_connection()
    query = f"SELECT TOP 50 * FROM {table_name}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --- LOGIN PAGE ---
def login_page():
    st.title("🔑 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = st.secrets["users"]
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# --- MAIN APP ---
def main_app():
    st.sidebar.success(f"Logged in as {st.session_state.username} ({st.session_state.role})")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.rerun()

    st.title("📊 Azure SQL Data Viewer")

    try:
        tables = get_table_names()
        table_name = st.selectbox("Wybierz tabelę", tables)

        if st.button("Load Table"):
            df = load_table(table_name)
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")

# --- ROUTER ---
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
