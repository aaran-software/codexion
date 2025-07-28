To install **Nginx** on Ubuntu, follow these simple steps:

---

### ✅ **Step-by-Step: Install Nginx**

#### 1. **Update System Packages**

```bash
sudo apt update
sudo apt upgrade -y
```

#### 2. **Install Nginx**

```bash
sudo apt install nginx -y
```

#### 3. **Start and Enable Nginx**

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

#### 4. **Check Nginx Status**

```bash
sudo systemctl status nginx
```

You should see something like: `active (running)`

---

### ✅ **Test Installation**

Open your browser and go to:

```
http://localhost
```

You should see the **Nginx Welcome Page**.

---

### 🔥 Optional: Allow Nginx Through Firewall (if UFW is enabled)

```bash
sudo ufw allow 'Nginx Full'
sudo ufw reload
```

---

### 📁 Nginx Config Paths (Important)

| Purpose             | Path                          |
| ------------------- | ----------------------------- |
| Default config      | `/etc/nginx/nginx.conf`       |
| Site configs        | `/etc/nginx/sites-available/` |
| Enabled sites       | `/etc/nginx/sites-enabled/`   |
| HTML root           | `/var/www/html/`              |
| Test config syntax  | `sudo nginx -t`               |
| Reload after change | `sudo systemctl reload nginx` |

---

Would you like a sample site config for `example.com` or to reverse-proxy to a container (e.g., `localhost:8000`)?
