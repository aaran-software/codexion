#!/usr/bin/env python3

import os
import subprocess

FRAPPE_BRANCH = "develop"
SITE_NAME = "sukraa.codexsun.com"
ADMIN_PASS = "admin"
DB_USER = "root"
DB_PASS = "DbPass1@@"
DB_HOST = "mariadb"
DB_NAME = "sukraa_db"
BENCH_DIR = "/home/devops/frappe-bench"
SUPERVISOR_CONF = "/etc/supervisor/conf.d/frappe.conf"
EMAIL = f"admin@{SITE_NAME}"
LOG_DIR = "/home/devops/logs"


# ------------------
# COLOR LOGGING
# ------------------
class Log:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    CYAN = '\033[0;36m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'

    @staticmethod
    def print(msg): print(f"{Log.CYAN}{msg}{Log.NC}")

    @staticmethod
    def success(msg): print(f"{Log.GREEN}{msg}{Log.NC}")

    @staticmethod
    def error(msg): print(f"{Log.RED}{msg}{Log.NC}")

    @staticmethod
    def warn(msg): print(f"{Log.YELLOW}{msg}{Log.NC}")


# ------------------
# UTILITIES
# ------------------
def run(cmd, cwd=None, check=True):
    try:
        subprocess.run(cmd, shell=True, cwd=cwd, check=check)
    except subprocess.CalledProcessError:
        Log.error(f"❌ Command failed: {cmd}")
        if check:
            exit(1)


def confirm(msg):
    return input(f"{msg} (y/N): ").strip().lower() == 'y'


def bench_running():
    return subprocess.run("pgrep -f 'bench start'", shell=True, stdout=subprocess.DEVNULL).returncode == 0


def confirm_bench_running():
    while not bench_running():
        Log.warn("⚠️ Bench is not running!")
        input("📣 Please run 'bench start' in another terminal. Press ENTER once it's running... ")
    Log.success("✅ stop Bench - then restart , check it is running!")


# ------------------
# SETUP FUNCTIONS
# ------------------
def setup_bench():
    if os.path.exists(BENCH_DIR):
        Log.warn("⚠️ Bench already exists.")
        if not confirm("🔁 Reinstall bench? This will delete existing one."):
            return
        run(f"rm -rf {BENCH_DIR}")
    Log.print("🌀 Installing Frappe Bench...")
    run(f"bench init frappe-bench --frappe-branch {FRAPPE_BRANCH}", cwd="/home/devops")


def create_site():
    site_path = os.path.join(BENCH_DIR, "sites", SITE_NAME)
    if os.path.exists(site_path):
        Log.warn(f"⚠️ Site {SITE_NAME} already exists.")
        if not confirm("🔁 Reinstall site? This will erase existing site data."):
            return
        run(f"bench drop-site {SITE_NAME} --force", cwd=BENCH_DIR)
    Log.print(f"🌐 Creating site: {SITE_NAME}")

    # run(f"bench new-site {SITE_NAME} --admin-password {ADMIN_PASS} --mariadb-root-username {DB_USER} --mariadb-root-password {DB_PASS} --db-host {DB_HOST} --mariadb-user-host-login-scope='%'",
    #     cwd=BENCH_DIR)

    run(
        f"bench new-site {SITE_NAME} "
        f"--admin-password {ADMIN_PASS} "
        f"--mariadb-root-username {DB_USER} "
        f"--mariadb-root-password {DB_PASS} "
        f"--db-host {DB_HOST} "
        f"--db-name {DB_NAME} "
        f"--mariadb-user-host-login-scope='%'",
        cwd=BENCH_DIR
    )

    run(f"bench use {SITE_NAME}", cwd=BENCH_DIR)


def install_erpnext():
    _install_app("ERPNext", "erpnext", f"https://github.com/frappe/erpnext")


def install_crm():
    _install_app("CRM", "crm", f"https://github.com/frappe/crm")


def install_hrms():
    _install_app("HRMS", "hrms", f"https://github.com/frappe/hrms")


def install_india_compliance():
    _install_app("India Compliance", "india_compliance", f"https://github.com/resilient-tech/india-compliance")


def _install_app(name, folder, repo):
    app_path = os.path.join(BENCH_DIR, "apps", folder)
    if os.path.exists(app_path):
        Log.warn(f"⚠️ {name} already cloned.")
        if confirm(f"🔁 Re-clone {name}? This will delete and clone again."):
            run(f"rm -rf apps/{folder}", cwd=BENCH_DIR)
            run(f"bench get-app --branch {FRAPPE_BRANCH} {folder} {repo}", cwd=BENCH_DIR)
    else:
        if confirm(f"📥 Install {name}?"):
            run(f"bench get-app --branch {FRAPPE_BRANCH} {folder} {repo}", cwd=BENCH_DIR)
        else:
            return

    confirm_bench_running()
    Log.warn("⚠️ Check Bench is running!")
    if confirm(f"🔧 Install {name} to {SITE_NAME}?"):
        run(f"bench --site {SITE_NAME} install-app {folder}", cwd=BENCH_DIR)


# ------------------
# BUILD + CONFIG
# ------------------
def build_and_config():
    Log.print("⚙️ Building assets and setting configuration...")
    run("bench build --force", cwd=BENCH_DIR)
    run("bench set-config -g developer_mode 1", cwd=BENCH_DIR)
    run("bench set-config -g host_name http://0.0.0.0:8000", cwd=BENCH_DIR)
    run(f"bench set-nginx-port {SITE_NAME} 8000", cwd=BENCH_DIR)
    run("bench setup nginx", cwd=BENCH_DIR)


# ------------------
# SUPERVISOR
# ------------------
def setup_supervisor():
    Log.print("🧩 Setting up Supervisor...")
    os.makedirs(LOG_DIR, exist_ok=True)
    config = f"""
[program:frappe]
command=/bin/bash -c \"cd {BENCH_DIR} && bench start\"
directory={BENCH_DIR}
autostart=true
autorestart=true
stdout_logfile={LOG_DIR}/bench.log
stderr_logfile={LOG_DIR}/bench.err.log
user=devops
"""
    with open("/tmp/frappe_supervisor.conf", "w") as f:
        f.write(config)
    run(f"sudo mv /tmp/frappe_supervisor.conf {SUPERVISOR_CONF}")
    run("sudo supervisorctl reread")
    run("sudo supervisorctl update")
    run("sudo supervisorctl start frappe")


# ------------------
# MAIN
# ------------------
if __name__ == '__main__':
    setup_bench()
    create_site()

    install_erpnext()
    install_crm()
    install_hrms()
    install_india_compliance()

    build_and_config()
    setup_supervisor()

    Log.success("✅ Frappe setup complete!")
    Log.print(f"🌐 Access your site at http://{SITE_NAME}")
