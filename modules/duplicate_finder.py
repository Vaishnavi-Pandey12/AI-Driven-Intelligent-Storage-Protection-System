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
    duplicates = []

    for f in files:
        h = file_hash(f)
        if h in hash_map:
            duplicates.append(f)
        else:
            hash_map[h] = f

    return duplicates




# test

if __name__ == "__main__":
    folder = "test_folder"
    dups = find_duplicates(folder)

    print("Duplicate files:")
    for f in dups:
        print(f)
