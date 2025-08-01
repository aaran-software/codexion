
🧱 1. Build Docker and Tag the Image
Even though you named the stage codexion-cloud, Docker won’t tag it by default. You need to build and tag it manually:

if not in root folder

```
docker build -t codexion-cloud:v1 -f docker/frappe/Dockerfile  docker/frappe
```

```
docker network create codexion-network
```

```
 docker compose -f mariadb.yml up -d
```
```
docker exec -it mariadb mariadb -u root -p
```

remote access for root user 

```
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

# 5 To run a specific Docker Compose file
```
docker compose -f soft-aaran-org.yml up -d
```

# 6 To open soft-aaran-org in bash
```
docker exec -it soft_aaran_org bash
```