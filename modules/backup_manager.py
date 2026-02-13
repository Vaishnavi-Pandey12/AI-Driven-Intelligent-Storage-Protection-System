import os
import shutil
from datetime import datetime


def backup_path(source_path, backup_root):
    """
    Backup a file or folder into backup_root with timestamp.
    Returns True if successful, False otherwise.
    """

    print("\n--- Backup Process Started ---")

    if not os.path.exists(source_path):
        print("❌ Source path does not exist.")
        return False

    os.makedirs(backup_root, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:
        if os.path.isdir(source_path):
            # Backup folder
            backup_path = os.path.join(backup_root, f"backup_folder_{timestamp}")
            shutil.copytree(source_path, backup_path)

        else:
            # Backup single file
            backup_path = os.path.join(backup_root, f"backup_file_{timestamp}")
            os.makedirs(backup_path, exist_ok=True)
            shutil.copy2(source_path, backup_path)

        print("✅ Backup completed successfully.")
        print("Backup location:", backup_path)

        return True

    except PermissionError:
        print("❌ Permission denied while copying.")
        return False

    except Exception as e:
        print("❌ Backup failed:")
        print(e)
        return False


# Test mode
if __name__ == "__main__":
    print("=== Backup Manager Test Mode ===")
    source = input("Enter source file/folder path: ")
    destination = input("Enter backup root folder path: ")

    success = backup_path(source, destination)

    if success:
        print("Backup test successful.")
    else:
        print("Backup test failed.")
