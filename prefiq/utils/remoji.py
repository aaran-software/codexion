# prefiq/utils/remoji.py

import os
import re

# Emoji ➝ ASCII replacements
EMOJI_REPLACEMENTS = {
    "✅": "[OK]",
    "❌": "[ERROR]",
    "🔄": "[UPDATE]",
    "🗑️": "[DELETE]",
    "⚠️": "[WARN]",
    "🔁": "[REINSTALL]",
    "📦": "[PACKAGE]",
    "📭": "[INBOX]",
    "📄": "[FILE]",
    "🔍": "[SCAN]",
    "🐳": "[DOCKER]",
    "🐬": "[MARIADB]",
    "🛠️": "[BUILD]",
    "📁": "[VOLUME]",
    "🧱": "[LAYER]",
    "🧰": "[TOOLBOX]",
    "🧩": "[PLUGIN]",
    "🌀": "[NETWORK]",
    "🚢": "[DEPLOY]",
    "⛴️": "[SHIP]",
    "🧼": "[CLEANUP]",
    "🪝": "[HOOK]",
    "🧿": "[WATCHER]",
    "🐍": "[PYTHON]",
    "🔷": "[PYFEATURE]",
    "📚": "[DOCS]",
    "🧪": "[TEST]",
    "🚀": "[LAUNCH]",
    "⚙️": "[CONFIG]",
    "🧵": "[THREAD]",
    "🧠": "[AI]",
    "📈": "[STATS]",
}

# Compile regex pattern
EMOJI_PATTERN = re.compile("|".join(map(re.escape, EMOJI_REPLACEMENTS.keys())))


def scan_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    matches = list(EMOJI_PATTERN.finditer(content))
    if not matches:
        return False

    print(f"\n📄 Found emojis in: {file_path}")
    for match in matches:
        emoji = match.group(0)
        replacement = EMOJI_REPLACEMENTS.get(emoji)
        print(f" - {emoji}  ➝  {replacement}")

    confirm = input("Replace these emojis with ASCII equivalents? [y/N]: ").strip().lower()
    if confirm != "y":
        print("[SKIP] Skipping.")
        return False

    new_content = EMOJI_PATTERN.sub(lambda m: EMOJI_REPLACEMENTS[m.group(0)], content)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("✅ Replaced successfully.")
    return True


def scan_folder(folder):
    abs_folder = os.path.abspath(folder)
    print(f"🔍 Scanning folder: {abs_folder}")
    for root, _, files in os.walk(abs_folder):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    scan_file(file_path)
                except UnicodeDecodeError:
                    print(f"[WARN] Skipping (encoding error): {file_path}")


if __name__ == "__main__":
    target = input("Enter the folder to scan (e.g., ./prefiq): ").strip()
    folder_path = os.path.abspath(target)

    if not os.path.isdir(folder_path):
        print(f"❌ Invalid folder path: {folder_path}")
    else:
        scan_folder(folder_path)

# Compile regex pattern to match any emoji key
EMOJI_PATTERN = re.compile("|".join(map(re.escape, EMOJI_REPLACEMENTS.keys())))

def scan_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    matches = list(EMOJI_PATTERN.finditer(content))
    if not matches:
        return False

    print(f"\n[FILE] Found emojis in: {file_path}")
    for match in matches:
        emoji = match.group(0)
        replacement = EMOJI_REPLACEMENTS.get(emoji)
        print(f" - {emoji}  ➝  {replacement}")

    confirm = input("Replace these emojis with ASCII equivalents? [y/N]: ").strip().lower()
    if confirm != "y":
        print("[SKIP] Skipping.")
        return False

    new_content = EMOJI_PATTERN.sub(lambda m: EMOJI_REPLACEMENTS[m.group(0)], content)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("[DONE] Replaced successfully.")
    return True

def scan_folder(folder):
    print(f"[SCAN] Scanning folder: {folder}")
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    scan_file(file_path)
                except UnicodeDecodeError:
                    print(f"[WARN] Skipping (encoding error): {file_path}")

if __name__ == "__main__":
    target = input("Enter the folder to scan (e.g., ./prefiq): ").strip()
    if not os.path.isdir(target):
        print("[ERROR] Invalid folder path.")
    else:
        scan_folder(target)
