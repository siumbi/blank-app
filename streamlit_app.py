import streamlit as st
import pandas as pd
import pyodbc
from st_aggrid import AgGrid, GridOptionsBuilder

# --- SESSION STATE INIT ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.page = "Login"

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
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

def load_table(table_name):
    conn = get_connection()
    query = f"SELECT TOP 200 * FROM {table_name}"  # zwiększona liczba wierszy
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def show_table(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(sortable=True, filter=True, resizable=True)
    grid_options = gb.build()
    AgGrid(df, gridOptions=grid_options, height=600, fit_columns_on_grid_load=True)

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
            st.session_state.page = "Home"
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# --- PAGE 1: SQL TABLE VIEWER ---
def page_home():
    st.sidebar.success(f"Logged in as {st.session_state.username} ({st.session_state.role})")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.session_state.page = "Login"
        st.rerun()

    st.title("📊 Azure SQL Data Viewer")

    try:
        tables = get_table_names()
        table_name = st.selectbox("Wybierz tabelę", tables, key="table_select")

        # --- automatyczne ładowanie po zmianie wyboru ---
        if table_name:
            df = load_table(table_name)
            # wyświetlanie z AgGrid, wysokość 600, dopasowanie szerokości do kolumn, przewijanie poziome
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_default_column(sortable=True, filter=True, resizable=True)
            gb.configure_grid_options(domLayout='normal')  # pozwala na poziomy scroll
            grid_options = gb.build()
            AgGrid(df, gridOptions=grid_options, height=600, fit_columns_on_grid_load=False)
    except Exception as e:
        st.error(f"Error: {e}")

# --- PAGE 2: BUTTONS PAGE ---
def page_buttons():
    st.title("⚡ Buttons Page")
    if st.button("Button 1"):
        st.success("You clicked Button 1!")
    if st.button("Button 2"):
        st.info("You clicked Button 2!")

# --- ROUTER ---
if not st.session_state.logged_in:
    login_page()
else:
    page = st.sidebar.radio("Navigation", ["Home", "Buttons Page"])
    if page == "Home":
        page_home()
    elif page == "Buttons Page":
        page_buttons()
