import streamlit as st
import os
import shutil
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
from modules.system_monitor import get_system_metrics
# Initialize notifications list
if "notifications" not in st.session_state:
    st.session_state.notifications = []

# Safe notification function (prevents duplicates)
def add_notification(note_type, message):
    notification = {"type": note_type, "message": message}
    if notification not in st.session_state.notifications:
        st.session_state.notifications.append(notification)


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
# PAGE ROUTING
# =====================================================

# DASHBOARD
if current_page == "dashboard":
    # HERO HEADER
    today = datetime.date.today().strftime("%B %d, %Y")

    col_h1, col_h2 = st.columns([3,1])

    with col_h1:
        st.markdown("""
        <div class="hero-container">
            <div class="hero-title">HELLO, WELCOME</div>
            <div class="hero-sub">
                Intelligent Storage Monitoring & Automated Protection
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_h2:
        st.markdown(f"""
        <div style="text-align:right;">
            <div class="status-badge">System Stable</div>
            <div style="margin-top:10px; font-size:14px;">
                {today}
            </div>
        </div>
        """, unsafe_allow_html=True)

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

    import psutil
    import time

    # Auto-detected values
    disk = psutil.disk_usage('/')
    auto_disk_usage = disk.percent

    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent

    boot_time = psutil.boot_time()
    uptime_hours = int((time.time() - boot_time) / 3600)

    st.info(f"Disk Usage: {auto_disk_usage}%")
    st.info(f"CPU Usage: {cpu_usage}%")
    st.info(f"RAM Usage: {ram_usage}%")
    st.info(f"System Uptime: {uptime_hours} hours")

    laptop_age = st.number_input(
        "Laptop age (years)",
        min_value=0,
        max_value=15,
        value=3,
    )

    daily_usage = st.slider(
        "Average daily usage (hours)",
        0,
        24,
        6,
    )

    if st.button("Run Health Analysis"):

        risk = 0

        if auto_disk_usage > 85:
            risk += 20

        if cpu_usage > 85:
            risk += 15

        if ram_usage > 85:
            risk += 15

        if uptime_hours > 200:
            risk += 10

        if laptop_age > 4:
            risk += 20

        if daily_usage > 8:
            risk += 10

        health_score = max(0, 100 - risk)

        if health_score > 70:
            status = "Good"
        elif health_score > 40:
            status = "Warning"
        else:
            status = "Critical"

        st.success(f"Health Score: {health_score}")
        st.write("Status:", status)

        st.session_state.health_score = health_score

        # -----------------
        # Notifications
        # -----------------

        add_notification("info", "Health scan completed.")

        if status == "Critical":
            add_notification("error", "System health is critical.")
        elif status == "Warning":
            add_notification("warning", "System health warning detected.")
        else:
            add_notification("success", "System health is good.")

        if auto_disk_usage > 85:
            add_notification("warning", "High disk usage detected.")

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

            # Notifications
            if len(duplicates) > 0:
                st.session_state.notifications.append(
                    {"type": "warning", "message": f"{len(duplicates)} duplicate files found."}
                )
            else:
                st.session_state.notifications.append(
                    {"type": "success", "message": "No duplicate files found."}
                )

        else:
            st.error("Invalid folder path.")
            st.session_state.notifications.append(
                {"type": "error", "message": "Duplicate scan failed. Invalid folder path."}
            )

    st.markdown("---")
    st.subheader("Find Duplicates of a Specific File")

    target_file = st.text_input("Target File Path")
    search_root = st.text_input("Search Root", value=folder_path if folder_path else "/")

    if st.button("Find File Duplicates"):

        if (
            target_file
            and search_root
            and os.path.exists(target_file)
            and os.path.exists(search_root)
        ):

            loader = display_loading_animation("Searching for identical copies...")
            time.sleep(1.5)

            matches = find_duplicates_of_file(target_file, search_root)

            loader.empty()

            st.write(f"Duplicate files found: {len(matches)}")

            if matches:
                st.code("\n".join(matches[:100]))
                st.session_state.notifications.append(
                    {"type": "warning", "message": f"{len(matches)} copies of selected file found."}
                )
            else:
                st.session_state.notifications.append(
                    {"type": "success", "message": "No duplicate copies of selected file found."}
                )

        else:
            st.error("Provide valid target file and search root paths.")


# BACKUP
elif current_page == "backup_automation":

    st.subheader("Backup Important Files")

    source = st.text_input("Source Folder", "important_files")
    destination = st.text_input(
        "Backup Folder",
        "backup_storage",
        key="manual_backup_dest"
    )

    if st.button("Run Backup"):

        if os.path.exists(source):

            loader = display_loading_animation("Backup in Progress...")
            time.sleep(2)

            success = backup_path(source, destination)

            loader.empty()

            if success:
                st.success("Backup Completed Successfully.")
                st.session_state.notifications.append(
                    {"type": "success", "message": "Manual backup completed successfully."}
                )
            else:
                st.error("Backup Failed.")
                st.session_state.notifications.append(
                    {"type": "error", "message": "Manual backup failed."}
                )

        else:
            st.error("Source path does not exist.")
            st.session_state.notifications.append(
                {"type": "error", "message": "Backup failed. Source path invalid."}
            )

    st.markdown("---")
    st.subheader("Intelligent Important File Backup")

    important_root = st.text_input(
        "Folder to scan for important files",
        value=source if source else ""
    )

    recommended_destination = st.text_input(
        "Backup Destination for Recommended Files",
        value=destination if destination else "backup_storage",
        key="important_backup_dest"
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
                st.session_state.notifications.append(
                    {"type": "info", "message": f"{len(important_files)} important files detected."}
                )
            else:
                st.session_state.notifications.append(
                    {"type": "success", "message": "No important files detected."}
                )

        else:
            st.error("Provide a valid folder path for important file detection.")

    if "important_files" in st.session_state and st.session_state["important_files"]:

        if st.button("Backup Recommended Files"):

            loader = display_loading_animation("Backing up recommended files...")
            time.sleep(1.5)

            backup_selected_files(
                st.session_state["important_files"],
                recommended_destination
            )

            loader.empty()

            st.success("Important files backed up successfully.")
            st.session_state.notifications.append(
                {"type": "success", "message": "Recommended important files backed up."}
            )


# NOTIFICATIONS
elif current_page == "notifications":

    st.subheader("Notifications Center")

    if st.button("Clear Notifications"):
        st.session_state.notifications = []
        st.success("Notifications cleared.")

    if st.session_state.notifications:

        for note in reversed(st.session_state.notifications):

            if note["type"] == "info":
                st.info(note["message"])

            elif note["type"] == "warning":
                st.warning(note["message"])

            elif note["type"] == "success":
                st.success(note["message"])

            elif note["type"] == "error":
                st.error(note["message"])

    else:
        st.info("No notifications yet.")


# SETTINGS
elif current_page == "settings":

    st.subheader("System Settings")
    st.checkbox("Enable Auto Backup")
    st.checkbox("Enable Duplicate Alerts")
    st.slider("Health Alert Threshold", 50, 100, 75)
    st.success("Settings Saved")
