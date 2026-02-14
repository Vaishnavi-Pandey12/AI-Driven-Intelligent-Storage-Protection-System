import streamlit as st
from modules.health_prediction import predict_health
from modules.duplicate_finder import find_duplicates, calculate_savings
from modules.backup_manager import backup_path


st.title("AI‑Driven Intelligent Storage Protection System")

st.header("Storage Health Check")

disk_usage = st.slider("Disk Usage (%)", 0, 100, 70)
temperature = st.slider("Temperature (°C)", 20, 80, 40)
read_error = st.number_input("Read Error Rate", 0, 100, 10)
write_error = st.number_input("Write Error Rate", 0, 100, 10)
reallocated = st.number_input("Reallocated Sector Count", 0, 500, 5)
pending = st.number_input("Pending Sector Count", 0, 500, 5)
power_hours = st.number_input("Power On Hours", 0, 100000, 10000)

if st.button("Check Health"):
    values = [
        disk_usage,
        temperature,
        read_error,
        write_error,
        reallocated,
        pending,
        power_hours
    ]

    score, status = predict_health(values)

    st.success(f"Health Score: {score}")
    st.write("Status:", status)


st.header("Duplicate File Scan")

folder = st.text_input(
    "Enter folder path to scan (example: C:\\Users\\YourName\\Documents)",
    ""
)

if st.button("Scan Duplicates"):
    if folder:
        dups = find_duplicates(folder)
        saved = calculate_savings(dups)

        st.write("Duplicate groups:", len(dups))
        st.write("Storage that can be saved:", round(saved, 2), "MB")
    else:
        st.warning("Please enter a folder path.")


st.header("Backup Important Files")

source = st.text_input("Source Folder", "important_files")
backup = st.text_input("Backup Folder", "backup_storage")

if st.button("Run Backup"):
    backup_path(source, backup)
    st.success("Backup completed.")



st.header("Run Full Protection Pipeline")

pipeline_folder = st.text_input("Folder to scan for duplicates", "test_folder")
pipeline_source = st.text_input("Important files folder", "important_files")
pipeline_backup = st.text_input("Backup destination", "backup_storage")

if st.button("Run Full Protection Scan"):

    # Health check
    values = [
        disk_usage,
        temperature,
        read_error,
        write_error,
        reallocated,
        pending,
        power_hours
    ]

    score, status = predict_health(values)

    st.write("Health Score:", score)
    st.write("Status:", status)

    # Duplicate scan
    dups = find_duplicates(pipeline_folder)
    saved = calculate_savings(dups)

    st.write("Duplicate groups:", len(dups))
    st.write("Storage that can be saved:", round(saved, 2), "MB")

    # Backup decision
    if status != "Good":
        backup_path(pipeline_source, pipeline_backup)
        st.success("Risk detected → Backup executed.")
    else:
        st.success("System healthy — backup not required.")