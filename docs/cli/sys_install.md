Here’s a **single shell script** that automates the full setup process you described:

---

### ✅ `setup_codexion.sh`

```bash
#!/bin/bash

set -e  # Exit on error

echo "🔄 Updating system packages..."
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git

echo "📦 Cloning codexion repository..."
git clone https://github.com/AARAN-SOFTWARE/codexion.git
cd codexion

echo "🐍 Creating and activating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📚 Installing Python requirements..."
pip install -r requirements.txt

echo "⚙️ Running prefiq installer..."
python prefiq/install.py

echo "✅ Setup complete!"
```

---

### 📦 To Use It:

1. Save the file:

   ```bash
   nano setup_codexion.sh
   ```

2. Paste the script above, then save (`Ctrl + O`, `Enter`, `Ctrl + X`)

3. Make it executable:

   ```bash
   chmod +x setup_codexion.sh
   ```

4. Run it:

   ```bash
   ./setup_codexion.sh
   ```

---
