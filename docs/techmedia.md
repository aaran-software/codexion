
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
docker compose -f erp-tmnext-in.yml up -d
```
```
docker compose -f erp-logicx-in.yml up -d
```
```
docker compose -f erp-techmedia-co-in.yml up -d
```

# 6 To open soft-aaran-org in bash
```
docker exec -it erp_tmnext_in bash
```

```
docker exec -it erp_logicx_in bash
```

```
docker exec -it erp_techmedia_co_in bash
```

# Step 1: Install SSL with Certbot (Recommended for Nginx)
Step 1: Install Certbot and Nginx plugin


```
sudo apt update
sudo apt install certbot python3-certbot-nginx -y
```
```
sudo systemctl status nginx
```
```
sudo ufw allow 'Nginx Full'
sudo ufw reload
```
```
sudo certbot --nginx
```


sudo ln -s /etc/nginx/sites-available/soft.aaran.org /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/sukraa.codexsun.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/flexcon.codexsun.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/smile.codexsun.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/ganapathi.codexsun.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/erp.lifeshoppy.com /etc/nginx/sites-enabled/



sudo ln -s /etc/nginx/sites-available/software.aaran.org /etc/nginx/sites-enabled/

sudo nginx -t
sudo systemctl reload nginx



# tmnext.in
```
sudo nano tmnext.in
```

```
server {
    listen 80;
    server_name tmnext.in;

    location / {
        proxy_pass http://127.0.0.1:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

# erp.tmnext.in

```
sudo nano erp.tmnext.in
```

```
server {
    listen 80;
    server_name erp.tmnext.in;

    location / {
        proxy_pass http://127.0.0.1:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```



# logicx.in



```
sudo nano logicx.in
```

```
server {
    listen 80;
    server_name logicx.in;

    location / {
        proxy_pass http://127.0.0.1:3003;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```


# erp.logicx.in



```
sudo nano erp.logicx.in
```

```
server {
    listen 80;
    server_name erp.logicx.in;

    location / {
        proxy_pass http://127.0.0.1:8003;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```


sudo ln -s /etc/nginx/sites-available/tmnext.in /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/erp.tmnext.in /etc/nginx/sites-enabled/

sudo ln -s /etc/nginx/sites-available/logicx.in /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/erp.logicx.in /etc/nginx/sites-enabled/

sudo nginx -t
sudo systemctl reload nginx



# 5 To run a specific Docker Compose file

```
docker compose -f tmnext-in.yml up -d
```

```
docker compose -f logicx-in.yml up -d
```

# 6 To open soft-aaran-org in bash

```
docker exec -it tmnext_in bash
```

```
docker exec -it logicx_in bash
```
