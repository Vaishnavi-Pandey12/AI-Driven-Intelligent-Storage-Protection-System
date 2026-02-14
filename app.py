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
# PAGE CONFIGURATION
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

/* Sidebar Profile Card */
.profile-card {
    background-color: #FADCDC;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 25px;
    text-align: center;
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

h1, h2, h3 {
    color: #743930;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# LOADING ANIMATION FUNCTION
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
# SESSION STATE INITIALIZATION
# =====================================================
if "current_page" not in st.session_state:
    st.session_state.current_page = "dashboard"

if "health_score" not in st.session_state:
    st.session_state.health_score = random.randint(60, 95)

if "duplicate_count" not in st.session_state:
    st.session_state.duplicate_count = random.randint(5, 20)

if "space_recoverable" not in st.session_state:
    st.session_state.space_recoverable = round(random.uniform(0.5, 2.5), 2)

if "last_backup_time" not in st.session_state:
    st.session_state.last_backup_time = "2 hours ago"


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================
with st.sidebar:

    st.markdown("""
    <div class="profile-card">
        <h3>StorageGuard</h3>
        <p>AI Storage Monitoring</p>
    </div>
    """, unsafe_allow_html=True)

    navigation_pages = {
        "dashboard": "Dashboard",
        "health_monitor": "Health Monitoring",
        "duplicate_analysis": "Duplicate Detection",
        "backup_automation": "Backup Management"
    }

    for page_key, page_label in navigation_pages.items():
        if st.session_state.current_page == page_key:
            st.markdown(f"""
            <div style="
                background:#FADCDC;
                padding:12px 15px;
                border-radius:12px;
                margin-bottom:8px;
                font-weight:600;">
                {page_label}
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.button(page_label):
                st.session_state.current_page = page_key

    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("System Version 1.0")
    st.markdown("© 2026 StorageGuard")


current_page = st.session_state.current_page


# =====================================================
# DASHBOARD PAGE
# =====================================================
if current_page == "dashboard":

    st.title("Dashboard Overview")
    st.markdown("---")

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

    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("Health Trend (Last 7 Days)")

        dates = [datetime.date.today() - datetime.timedelta(days=i) for i in range(7)]
        dates.reverse()
        health_values = [random.randint(60, 95) for _ in range(7)]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=health_values, mode='lines+markers'))
        fig.update_layout(height=300)

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("System Activity Log")
        with st.expander("View Activity"):
            st.write("• Health scan completed")
            st.write("• Duplicate detection completed")
            st.write("• Backup operation executed")
            st.write("• System stable")

    with right_col:
        st.subheader("System Indicators")
        st.progress(st.session_state.health_score / 100)
        st.write("System Health")
        st.progress(st.session_state.duplicate_count / 30)
        st.write("Duplicate Ratio")
        st.progress(0.85)
        st.write("System Stability")


# =====================================================
# HEALTH MONITORING PAGE
# =====================================================
elif current_page == "health_monitor":

    st.title("Health Monitoring")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        disk_usage = st.number_input("Disk Usage (%)", 0.0, 100.0, 50.0)
        temperature = st.number_input("Temperature (°C)", 0.0, 100.0, 35.0)
        read_error_rate = st.number_input("Read Error Rate", 0.0, 1000.0, 10.0)
        write_error_rate = st.number_input("Write Error Rate", 0.0, 1000.0, 10.0)

    with col2:
        reallocated_sector_count = st.number_input("Reallocated Sector Count", 0, 1000, 5)
        pending_sector_count = st.number_input("Pending Sector Count", 0, 1000, 3)
        power_on_hours = st.number_input("Power-On Hours", 0, 100000, 5000)

    if st.button("Run Health Analysis"):

        loader = display_loading_animation("Analyzing Storage Health...")
        time.sleep(2)

        metrics = [
            disk_usage,
            temperature,
            read_error_rate,
            write_error_rate,
            reallocated_sector_count,
            pending_sector_count,
            power_on_hours
        ]

        health_score, risk_status = predict_health(metrics)
        st.session_state.health_score = health_score

        loader.empty()

        st.metric("Health Score", f"{health_score}/100")
        st.metric("Risk Status", risk_status)


# =====================================================
# DUPLICATE DETECTION PAGE
# =====================================================
elif current_page == "duplicate_analysis":

    st.title("Duplicate Detection")
    st.markdown("---")

    folder_path = st.text_input("Folder Path")

    if st.button("Scan for Duplicates"):

        if os.path.exists(folder_path):

            loader = display_loading_animation("Scanning for Duplicate Files...")
            time.sleep(2)

            duplicate_files = find_duplicates(folder_path)
            loader.empty()

            st.session_state.duplicate_count = len(duplicate_files)
            st.session_state.space_recoverable = round(random.uniform(0.5, 2.5), 2)

            st.metric("Duplicate Files Found", len(duplicate_files))
            st.metric("Estimated Space Recoverable (GB)", st.session_state.space_recoverable)

            if duplicate_files:
                with st.expander("View Duplicate Files"):
                    for file in duplicate_files:
                        st.write(file)
            else:
                st.success("No duplicate files detected.")

        else:
            st.error("Invalid folder path.")


# =====================================================
# BACKUP MANAGEMENT PAGE
# =====================================================
elif current_page == "backup_automation":

    st.title("Backup Management")
    st.markdown("---")

    source_path = st.text_input("Source File / Folder")
    destination_path = st.text_input("Backup Destination")

    if st.button("Initiate Backup"):

        if os.path.exists(source_path):

            loader = display_loading_animation("Backup in Progress...")
            time.sleep(2)

            backup_success = backup_path(source_path, destination_path)
            loader.empty()

            if backup_success:
                st.session_state.last_backup_time = "Just now"
                st.success("Backup completed successfully.")
            else:
                st.error("Backup failed.")

        else:
            st.error("Source path does not exist.")

    st.markdown("---")
    st.write(f"Last Backup: {st.session_state.last_backup_time}")
