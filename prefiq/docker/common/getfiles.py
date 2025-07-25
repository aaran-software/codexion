import os
import shutil

from prefiq import CPATH

# 🔧 Config
FILES_TO_COPY = [
    "init_frappe.py",
    "supervisord.conf",
    "cloud-nginx.conf"

]

# Set paths
SOURCE_DIR = CPATH.PREFIQ_TEMPLATE
TARGET_DIR = CPATH.DOCKER_DIR

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
