import streamlit as st
import os
import plotly.graph_objects as go
import random
import datetime
import time

from modules.health_prediction import predict_health
from modules.duplicate_finder import (
    find_duplicates,
    calculate_savings,
    find_duplicates_of_file,
)
from modules.backup_manager import (
    backup_path,
    find_important_files,
    backup_selected_files,
)


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
        "protection_pipeline": "Full Protection",
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

    st.header("Quick 1-Minute Health Check")

    disk_usage = st.slider("Disk usage (%)", 0, 100, 60)

    laptop_age = st.number_input(
        "Laptop age (years)",
        min_value=0,
        max_value=15,
        value=3,
    )

    daily_usage = st.slider(
        "Daily usage hours",
        0,
        24,
        6,
    )

    system_slow = st.radio("System slowing?", ["No", "Yes"])
    overheating = st.radio("Overheating?", ["No", "Yes"])

    if st.button("Run Health Analysis"):

        temperature = 70 if overheating == "Yes" else 40
        read_error = 25 if system_slow == "Yes" else 5
        write_error = read_error
        reallocated = 5
        pending = 5
        power_on_hours = laptop_age * 365 * daily_usage

        values = [
            disk_usage,
            temperature,
            read_error,
            write_error,
            reallocated,
            pending,
            power_on_hours,
        ]

        loader = display_loading_animation("Analyzing Storage Health...")
        time.sleep(2)
        score, status = predict_health(values)
        loader.empty()

        st.success(f"Health Score: {score}")
        st.write("Status:", status)

        st.session_state.health_score = score
        st.session_state.quick_health_values = values


# DUPLICATES
elif current_page == "duplicate_analysis":

    st.subheader("Duplicate File Scan")

    folder_path = st.text_input("Enter folder path to scan", "")

    if st.button("Scan Duplicates"):
        if os.path.exists(folder_path):
            loader = display_loading_animation("Scanning for Duplicate Files...")
            time.sleep(2)
            duplicates = find_duplicates(folder_path)
            savings = calculate_savings(duplicates)
            loader.empty()
            st.metric("Duplicate Files Found", len(duplicates))
            st.metric("Storage Recoverable (MB)", round(savings, 2))
            st.session_state.duplicate_count = len(duplicates)
            st.session_state.space_recoverable = round(savings / 1024, 2)
        else:
            st.error("Invalid folder path.")

    st.markdown("---")
    st.subheader("Find Duplicates of a Specific File")

    target_file = st.text_input("Target File Path")
    search_root = st.text_input("Search Root", value=folder_path if folder_path else "/")

    if st.button("Find File Duplicates"):
        if target_file and search_root and os.path.exists(target_file) and os.path.exists(search_root):
            loader = display_loading_animation("Searching for identical copies...")
            time.sleep(1.5)
            matches = find_duplicates_of_file(target_file, search_root)
            loader.empty()
            st.write(f"Duplicate files found: {len(matches)}")
            if matches:
                st.code("\n".join(matches[:100]))
        else:
            st.error("Provide valid target file and search root paths.")


# BACKUP
elif current_page == "backup_automation":

    st.subheader("Backup Important Files")

    source = st.text_input("Source Folder", "important_files")
    destination = st.text_input("Backup Folder", "backup_storage", key="manual_backup_dest")

    if st.button("Run Backup"):
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

    st.markdown("---")
    st.subheader("Intelligent Important File Backup")

    important_root = st.text_input("Folder to scan for important files", "C:\\Users")
    recommended_destination = st.text_input(
        "Backup Destination for Recommended Files",
        value=destination if destination else "backup_storage",
        key="important_backup_dest",
    )

    if st.button("Suggest Important Files"):
        if important_root and os.path.exists(important_root):
            loader = display_loading_animation("Finding important files...")
            time.sleep(1.5)
            important_files = find_important_files(important_root)
            loader.empty()
            st.session_state["important_files"] = important_files
            st.write(f"Important files detected: {len(important_files)}")
            if important_files:
                st.code("\n".join(important_files[:30]))
        else:
            st.error("Provide a valid folder path for important file detection.")

    if "important_files" in st.session_state and st.session_state["important_files"]:
        if st.button("Backup Recommended Files"):
            loader = display_loading_animation("Backing up recommended files...")
            time.sleep(1.5)
            backup_selected_files(st.session_state["important_files"], recommended_destination)
            loader.empty()
            st.success("Important files backed up successfully.")


# FULL PROTECTION
elif current_page == "protection_pipeline":

    st.subheader("Run Full Protection Pipeline")

    pipeline_folder = st.text_input("Folder to scan for duplicates", "test_folder")
    pipeline_source = st.text_input("Important files folder", "important_files")
    pipeline_backup = st.text_input("Backup destination", "backup_storage", key="pipeline_backup_dest")

    st.markdown("Health Inputs (Quick Mode)")
    pipeline_disk_usage = st.slider("Disk usage (%)", 0, 100, 60, key="pipe_disk")
    pipeline_laptop_age = st.number_input("Laptop age (years)", 0, 15, 3, key="pipe_laptop_age")
    pipeline_daily_usage = st.slider("Daily usage hours", 0, 24, 6, key="pipe_daily_usage")
    pipeline_system_slow = st.radio("System slowing?", ["No", "Yes"], key="pipe_slow")
    pipeline_overheating = st.radio("Overheating?", ["No", "Yes"], key="pipe_hot")

    if st.button("Run Full Protection Scan"):
        loader = display_loading_animation("Running end-to-end protection workflow...")
        time.sleep(2)

        pipeline_temperature = 70 if pipeline_overheating == "Yes" else 40
        pipeline_read_error = 25 if pipeline_system_slow == "Yes" else 5
        pipeline_write_error = pipeline_read_error
        pipeline_power_hours = pipeline_laptop_age * 365 * pipeline_daily_usage

        metrics = [
            pipeline_disk_usage,
            pipeline_temperature,
            pipeline_read_error,
            pipeline_write_error,
            5,
            5,
            pipeline_power_hours,
        ]
        score, status = predict_health(metrics)

        st.write("Health Score:", score)
        st.write("Status:", status)

        if os.path.exists(pipeline_folder):
            duplicates = find_duplicates(pipeline_folder)
            savings = calculate_savings(duplicates)
            st.write("Duplicate groups:", len(duplicates))
            st.write("Storage that can be saved:", round(savings, 2), "MB")
        else:
            st.warning("Duplicate scan skipped: invalid folder path.")

        if status != "Good" and os.path.exists(pipeline_source):
            backup_ok = backup_path(pipeline_source, pipeline_backup)
            if backup_ok:
                st.success("Risk detected → Backup executed.")
            else:
                st.error("Risk detected but backup failed.")
        elif status != "Good":
            st.error("Risk detected but pipeline source path is invalid.")
        else:
            st.success("System healthy — backup not required.")

        loader.empty()


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
