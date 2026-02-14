from modules.health_prediction import predict_health
from modules.duplicate_finder import find_duplicates, calculate_savings
from modules.backup_manager import backup_path

# Example disk input (later this can come from real system)
disk_input = [95, 65, 40, 42, 80, 60, 40000]   # high-risk values


score, status = predict_health(disk_input)

print("Disk Health:", status)
print("Health Score:", score)

folder = "test_folder"

dups = find_duplicates(folder)
saved = calculate_savings(dups)

print("Duplicate groups:", len(dups))
print("Storage that can be saved:", round(saved, 2), "MB")

# Intelligent decision logic
source_folder = "important_files"
backup_root = "backup_storage"

if status != "Good":
    print("\n⚠ Risk detected:")
    print("→ Cleaning duplicates recommended")
    print("→ Starting automatic backup...")

    backup_path(source_folder, backup_root)
else:
    print("\nSystem healthy — no action required")
