# Build for production
docker build -t cortex-app:v1 --build-arg MODE=prod .

# Run in production
docker run -e MODE=prod -p 4000:4000 cortex-app:v1
