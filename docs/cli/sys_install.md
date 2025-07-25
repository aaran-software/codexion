Here’s a **single shell script** that automates the full setup process you described:

---

### ✅ `setup_codexion.sh`

```
#!/bin/bash

set -e  # Exit on error

echo "🔄 Updating system packages..."
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git
sudo apt install -y ca-certificates curl gnupg lsb-release

echo "📦 Cloning codexion repository..."

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "📦 docker version..."
sudo docker version

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

echo "⚙️ Running docker network..."
docker network create codexion-network

echo "✅ Setup complete!"
```

---

### 📦 To Use It:

1. Save the file:

   ```
   nano setup_codexion.sh
   ```

2. Paste the script above, then save (`Ctrl + O`, `Enter`, `Ctrl + X`)

3. Make it executable:

   ```
   chmod +x setup_codexion.sh
   ```

4. Run it:

   ```
   ./setup_codexion.sh
   ```

---
