# prefiq/database/migrations/hashing.py

import hashlib

def compute_file_hash(file_path: str) -> str:
    """
    Compute SHA256 hash of the file content.
    """
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()
