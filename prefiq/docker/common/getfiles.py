import os
import shutil

# 🔧 Config
FILES_TO_COPY = [
    "init_frappe.py",
    "supervisord.conf",
    "cloud-nginx.conf"

]

# Set paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(BASE_DIR, "prefiq", "templates")
TARGET_DIR = os.path.join(BASE_DIR, "docker")

def copy_files_to_docker():
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        print(f"📁 Created target folder: {TARGET_DIR}")

    for filename in FILES_TO_COPY:
        src = os.path.join(SOURCE_DIR, filename)
        dst = os.path.join(TARGET_DIR, filename)

        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"✅ Copied: {filename}")
        else:
            print(f"❌ Not found: {filename}")
