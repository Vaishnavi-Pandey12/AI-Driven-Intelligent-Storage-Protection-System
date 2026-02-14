import streamlit as st
import os
import plotly.graph_objects as go
import random
import datetime
import time

from modules.health_prediction import predict_health
from modules.duplicate_finder import find_duplicates
from modules.backup_manager import backup_path


# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="StorageGuard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# GLOBAL STYLING
# =====================================================
st.markdown("""
<style>

.stApp {
    background-color: #FADCDC;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #E5BEA0;
    padding-top: 20px;
}

/* Brand Card */
.brand-card {
    background:#FADCDC;
    padding:20px;
    border-radius:20px;
    text-align:center;
    margin-bottom:20px;
}

/* Sidebar Buttons */
section[data-testid="stSidebar"] button {
    width: 100%;
    text-align: left;
    background-color: transparent;
    color: #743930;
    border: none;
    padding: 12px 15px;
    border-radius: 12px;
    margin-bottom: 8px;
    font-size: 15px;
    font-weight: 500;
}

section[data-testid="stSidebar"] button:hover {
    background-color: #FADCDC;
}

/* Active Nav */
.nav-active {
    background:#FADCDC;
    padding:12px 15px;
    border-radius:12px;
    margin-bottom:8px;
    font-weight:600;
}

/* Metric Cards */
div[data-testid="metric-container"] {
    background-color: #E5BEA0;
    padding: 15px;
    border-radius: 12px;
}

/* Buttons */
.stButton>button {
    background-color: #996350;
    color: white;
    border-radius: 8px;
    padding: 8px 20px;
}

/* Loader */
.loader {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 6px solid #E5BEA0;
  border-top: 6px solid #743930;
  animation: spin 1s linear infinite;
  margin: auto;
}

@keyframes spin {
  100% { transform: rotate(360deg); }
}

.loader-text {
  text-align:center;
  color:#743930;
  font-weight:600;
  margin-top:10px;
}

/* Hero */
.hero-container {
    background-color:#E5BEA0;
    padding:30px;
    border-radius:20px;
    margin-bottom:30px;
}

.hero-title {
    margin:0;
    font-size:42px;
    font-weight:700;
    color:#743930;
    text-transform:uppercase;
    letter-spacing:3px;
}

.hero-sub {
    margin-top:8px;
    font-size:16px;
    color:#743930;
    opacity:0.8;
}

.status-badge {
    background-color:#996350;
    color:white;
    padding:6px 14px;
    border-radius:20px;
    font-size:13px;
    font-weight:500;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# LOADER FUNCTION
# =====================================================
def display_loading_animation(message: str):
    placeholder = st.empty()
    placeholder.markdown(f"""
    <div style="text-align:center; padding:40px;">
        <div class="loader"></div>
        <div class="loader-text">{message}</div>
    </div>
    """, unsafe_allow_html=True)
    return placeholder


# =====================================================
# SESSION STATE INIT
# =====================================================
if "current_page" not in st.session_state:
    st.session_state.current_page = "dashboard"

if "health_score" not in st.session_state:
    st.session_state.health_score = random.randint(70, 95)

if "duplicate_count" not in st.session_state:
    st.session_state.duplicate_count = random.randint(5, 20)

if "space_recoverable" not in st.session_state:
    st.session_state.space_recoverable = round(random.uniform(0.5, 2.5), 2)

if "last_backup_time" not in st.session_state:
    st.session_state.last_backup_time = "2 hours ago"


# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:

    st.markdown("""
    <div class="brand-card">
        <h3 style="margin:0;">StorageGuard</h3>
        <p style="margin-top:5px;">AI Storage Monitoring</p>
    </div>
    """, unsafe_allow_html=True)

    pages = {
        "dashboard": "Dashboard",
        "health_monitor": "Health Monitoring",
        "duplicate_analysis": "Duplicate Detection",
        "backup_automation": "Backup Management",
        "notifications": "Notifications",
        "settings": "Settings"
    }

    for key, label in pages.items():
        if st.session_state.current_page == key:
            st.markdown(f'<div class="nav-active">{label}</div>', unsafe_allow_html=True)
        else:
            if st.button(label):
                st.session_state.current_page = key

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("System Version 1.0")
    st.markdown("© 2026 StorageGuard")

current_page = st.session_state.current_page


# =====================================================
# HERO HEADER
# =====================================================
today = datetime.date.today().strftime("%B %d, %Y")

col1, col2 = st.columns([3,1])

with col1:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">HELLO, WELCOME</div>
        <div class="hero-sub">
            Intelligent Storage Monitoring & Automated Protection
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="text-align:right;">
        <div class="status-badge">System Stable</div>
        <div style="margin-top:10px; font-size:14px; color:#743930;">
            {today}
        </div>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# PAGE ROUTING
# =====================================================

# DASHBOARD
if current_page == "dashboard":

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Health Score", f"{st.session_state.health_score}/100")

    with col2:
        risk_level = "Low" if st.session_state.health_score > 70 else "High"
        st.metric("Risk Level", risk_level)

    with col3:
        st.metric("Duplicate Files", st.session_state.duplicate_count)

    with col4:
        st.metric("Space Recoverable (GB)", st.session_state.space_recoverable)

    st.markdown("---")

    left, right = st.columns([2,1])

    with left:
        st.subheader("Health Trend (7 Days)")
        dates = [datetime.date.today() - datetime.timedelta(days=i) for i in range(7)]
        dates.reverse()
        values = [random.randint(60, 95) for _ in range(7)]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=values, mode='lines+markers'))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("System Indicators")
        st.progress(st.session_state.health_score / 100)
        st.progress(0.85)


# HEALTH
elif current_page == "health_monitor":

    st.subheader("Health Monitoring")

    disk_usage = st.number_input("Disk Usage (%)", 0.0, 100.0, 50.0)

    if st.button("Run Health Analysis"):
        loader = display_loading_animation("Analyzing Storage Health...")
        time.sleep(2)
        metrics = [disk_usage, 35, 10, 10, 5, 3, 5000]
        score, status = predict_health(metrics)
        loader.empty()
        st.metric("Health Score", f"{score}/100")
        st.metric("Risk Status", status)


# DUPLICATES
elif current_page == "duplicate_analysis":

    st.subheader("Duplicate Detection")

    folder_path = st.text_input("Folder Path")

    if st.button("Scan for Duplicates"):
        if os.path.exists(folder_path):
            loader = display_loading_animation("Scanning for Duplicate Files...")
            time.sleep(2)
            duplicates = find_duplicates(folder_path)
            loader.empty()
            st.metric("Duplicate Files Found", len(duplicates))
        else:
            st.error("Invalid folder path.")


# BACKUP
elif current_page == "backup_automation":

    st.subheader("Backup Management")

    source = st.text_input("Source File / Folder")
    destination = st.text_input("Backup Destination")

    if st.button("Initiate Backup"):
        if os.path.exists(source):
            loader = display_loading_animation("Backup in Progress...")
            time.sleep(2)
            success = backup_path(source, destination)
            loader.empty()
            if success:
                st.success("Backup Completed Successfully.")
            else:
                st.error("Backup Failed.")
        else:
            st.error("Source path does not exist.")


# NOTIFICATIONS
elif current_page == "notifications":

    st.subheader("Notifications Center")
    st.info("Health scan completed.")
    st.warning("High disk usage detected.")
    st.success("Backup completed successfully.")


# SETTINGS
elif current_page == "settings":

    st.subheader("System Settings")
    st.checkbox("Enable Auto Backup")
    st.checkbox("Enable Duplicate Alerts")
    st.slider("Health Alert Threshold", 50, 100, 75)
    st.success("Settings Saved")
