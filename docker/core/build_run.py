import subprocess
import os
import shutil

IMAGE_NAME = "codexion"
CONTAINER_NAME = "codexion_app"

def run_cmd(command, check=True):
    print(f"\n🔧 Running: {command}")
    result = subprocess.run(command, shell=True)
    if check and result.returncode != 0:
        print("❌ Command failed!")
        exit(1)

def main():
    # Step 1: Copy .env.sample to .env if not present
    if not os.path.exists(".env"):
        print("📁 Creating .env from .env.sample...")
        shutil.copy(".env.sample", ".env")

    # Step 2: Build the Docker image
    print("🐳 Building Docker image...")
    run_cmd(f"docker build -t {IMAGE_NAME} .")

    # Step 3: Stop and remove existing container (if exists)
    print("🧹 Cleaning up old container...")
    subprocess.run(f"docker rm -f {CONTAINER_NAME}", shell=True)

    # Step 4: Run the Docker container
    print("🚀 Running Docker container...")
    run_cmd(f"docker run -d -p 4000:4000 --name {CONTAINER_NAME} {IMAGE_NAME}")

    print("\n✅ Codexion backend is running at http://localhost:4000")

if __name__ == "__main__":
    main()
