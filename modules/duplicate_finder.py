import os
import hashlib

def get_files(folder):
    file_paths = []
    for root, _, files in os.walk(folder):
        for f in files:
            file_paths.append(os.path.join(root, f))
    return file_paths


def file_hash(path):
    h = hashlib.md5()
    with open(path, 'rb') as file:
        while chunk := file.read(8192):
            h.update(chunk)
    return h.hexdigest()


def find_duplicates(folder):

    files = get_files(folder)

    hash_map = {}

    for f in files:
        h = file_hash(f)

        if h in hash_map:
            hash_map[h].append(f)
        else:
            hash_map[h] = [f]

    # keep only duplicate groups
    duplicates = {k: v for k, v in hash_map.items() if len(v) > 1}

    return duplicates


def calculate_savings(duplicates):
    import os
    total_size = 0

    for files in duplicates.values():
        # keep first file, rest are waste
        for f in files[1:]:
            total_size += os.path.getsize(f)

    return total_size / (1024 * 1024)   # MB


def find_duplicates_of_file(target_file, search_root):

    target_hash = file_hash(target_file)
    matches = []

    for root, _, files in os.walk(search_root):
        for f in files:
            path = os.path.join(root, f)
            try:
                if file_hash(path) == target_hash:
                    matches.append(path)
            except:
                pass

    return matches



# test

if __name__ == "__main__":
    folder = "test_folder"

    dups = find_duplicates(folder)

    print("Duplicate groups:", len(dups))

    saved = calculate_savings(dups)
    print("Storage that can be saved:", round(saved, 2), "MB")

