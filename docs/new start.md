
🧱 1. Build Docker and Tag the Image
Even though you named the stage codexion-cloud, Docker won’t tag it by default. You need to build and tag it manually:

```
docker build -t codexion-cloud:v1 .
```

if not in root folder

```
docker build -t codexion-cloud:v1 -f docker/Dockerfile  docker/
```

Now, codexion-cloud:v1 is a full Docker image that you can use anywhere.



### Step 2 : To create custom network to share between containers 
```
docker network create codexion-network
```

To run a specific Docker Compose file
```
docker compose -f docker-compose-soft_aaran_org.yml up -d
```

Here's the direct one-liner bash command to zip and copy the frappe-bench directory to /home/devops/shared:
```
cd /home/devops && zip -r frappe-bench.zip frappe-bench && mkdir -p /home/devops/shared && mv frappe-bench.zip /home/devops/shared/
```


