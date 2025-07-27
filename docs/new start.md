
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

```
SELECT user, host FROM mysql.user WHERE user = 'root';
```
You should see something like:

```
+------+-----------+
| user | host      |
+------+-----------+
| root | localhost |
| root | %         |
+------+-----------+
```

If 'root'@'%' exists and has privileges, you're ready to connect remotely.

4. Allow access on your Ubuntu host (firewall):
If using UFW:

```
sudo ufw allow 3306/tcp
```
```
sudo ufw reload
```
```
sudo ufw status
```
status : inactive


# 5 To run a specific Docker Compose file
```
docker compose -f soft-aaran-org.yml up -d
```
```
docker compose -f sukraa-codexsun-com.yml up -d
```
```
docker compose -f flexcon-codexsun-com.yml up -d
```
```
docker compose -f smile-codexsun-com.yml up -d
```
```
docker compose -f ganapathi-codexsun-com.yml up -d
```
```
docker compose -f erp-lifeshoppy-com.yml up -d
```


Here's the direct one-liner bash command to zip and copy the frappe-bench directory to /home/devops/shared:
```
cd /home/devops && zip -r frappe-bench.zip frappe-bench && mkdir -p /home/devops/shared && mv frappe-bench.zip /home/devops/shared/
```


