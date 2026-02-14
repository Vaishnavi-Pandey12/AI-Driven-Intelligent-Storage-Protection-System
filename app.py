import streamlit as st
import os

from modules.health_prediction import predict_health
from modules.duplicate_finder import find_duplicates
from modules.backup_manager import backup_path


# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="AI Storage Protection System",
    page_icon="💾",
    layout="wide"
)

st.title("AI-Driven Intelligent Storage Protection System")

st.markdown("Monitor storage health, detect duplicates, and trigger automated backup.")

st.markdown("---")


# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Storage Health Monitor", "Duplicate File Finder", "Automated Backup"]
)


# ==========================================================
# 1️⃣ STORAGE HEALTH MONITOR
# ==========================================================
if page == "Storage Health Monitor":

    st.header("Storage Health Monitor")

    col1, col2 = st.columns(2)

    with col1:
        disk_usage = st.number_input("Disk Usage (%)", 0.0, 100.0, 50.0)
        temperature = st.number_input("Temperature (°C)", 0.0, 100.0, 35.0)
        read_error = st.number_input("Read Error Rate", 0.0, 1000.0, 10.0)
        write_error = st.number_input("Write Error Rate", 0.0, 1000.0, 10.0)

    with col2:
        reallocated = st.number_input("Reallocated Sector Count", 0, 1000, 5)
        pending = st.number_input("Pending Sector Count", 0, 1000, 3)
        power_hours = st.number_input("Power-On Hours", 0, 100000, 5000)

    if st.button("Check Health"):

        metrics = [
            disk_usage,
            temperature,
            read_error,
            write_error,
            reallocated,
            pending,
            power_hours
        ]

        health_score, status = predict_health(metrics)

        st.markdown("---")
        st.subheader("Health Analysis Result")

        st.progress(health_score / 100)
        st.metric("Health Score", f"{health_score}/100")

        if status == "Good":
            st.success("Storage Status: Good")
        else:
            st.error("Storage Status: Critical")

        st.session_state["health_score"] = health_score
        st.session_state["status"] = status


# ==========================================================
# 2️⃣ DUPLICATE FILE FINDER
# ==========================================================
elif page == "Duplicate File Finder":

    st.header("Duplicate File Finder")

    folder_path = st.text_input("Enter folder path to scan")

    if st.button("Scan for Duplicates"):

        if os.path.exists(folder_path):

            duplicates = find_duplicates(folder_path)

            st.markdown("---")

            st.write(f"Total duplicate files found: {len(duplicates)}")

            if duplicates:
                st.success("Duplicate files detected")

                for file in duplicates:
                    st.write(file)

            else:
                st.success("No duplicate files found.")

        else:
            st.error("Invalid folder path. Please check and try again.")


# ==========================================================
# 3️⃣ AUTOMATED BACKUP
# ==========================================================
elif page == "Automated Backup":

    st.header("Automated Backup")

    if "health_score" in st.session_state:

        health_score = st.session_state["health_score"]

        st.metric("Current Health Score", f"{health_score}/100")

        if health_score < 40:

            st.warning("Health score is low. Backup recommended.")

            source = st.text_input("Enter file or folder to backup")
            destination = st.text_input("Enter backup destination folder")

            if st.button("Start Backup"):

                if os.path.exists(source):

                    success = backup_path(source, destination)

                    if success:
                        st.success("Backup completed successfully.")
                        st.balloons()
                    else:
                        st.error("Backup failed. Check permissions or path.")

                else:
                    st.error("Source path does not exist.")

        else:
            st.success("Storage health is stable. Backup not required.")

    else:
        st.info("Please check storage health first in the Storage Health Monitor section.")
