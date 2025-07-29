# Stop and remove running container (if exists)
docker compose -f docker/core/cortex.yml down --remove-orphans

# Remove old image (if exists)
docker rmi -f cortex-app:v1 || true

# Rebuild image from Dockerfile
docker build -t cortex-app:v1 -f docker/core/Dockerfile .

# Start services using docker compose
docker compose -f docker/core/cortex.yml up -d
