

#### 1. Build Docker and Tag the Image

```
docker build -t codexion-cloud:v2 -f docker/cloud/Dockerfile  docker/cloud
```

### 2. create network for codexion

```
docker network create codexion-network
```

### 3. create container for mariadb

```
 docker compose -f docker/cloud/mariadb-local.yml up -d
```

### 4. Check mariadb is installed

```
docker exec -it mariadb mariadb -u root -p
```

remote access for root user 

```
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

### 5 To run a specific Docker Compose file
```
docker compose -f docker/cloud/dev-software-com.yml up -d
```

### 6 To open soft-aaran-org in bash
```
docker exec -it dev_software_com bash
```