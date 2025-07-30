
🧱 1. Build Docker and Tag the Image
Even though you named the stage codexion-cloud, Docker won’t tag it by default. You need to build and tag it manually:

if in root folder

```
docker build -t cortex-app:v1 -f docker/core/Dockerfile .
```

if in root folder

```
cd docker/core
```

```
docker build -t cortex-app:v1 .
```

Now, codexion-cloud:v1 is a full Docker image that you can use anywhere.


# 5 To run a specific Docker Compose file
```
docker compose -f docker/core/cortex.yml up -d
```

# 6 To open soft-aaran-org in bash
```
docker exec -it cortex_app bash
```
