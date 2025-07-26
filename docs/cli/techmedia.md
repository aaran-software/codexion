 docker ps

CONTAINER ID   IMAGE                    COMMAND                  CREATED              STATUS              PORTS                                                   NAMES
0b245c2d03a5   mariadb:11.7             "docker-entrypoint.s…"   About a minute ago   Up About a minute   0.0.0.0:3306->3306/tcp, [::]:3306->3306/tcp             mariadb-codexion_db
b182450a83f3   erp_techmedia_co_in:v1   "/usr/bin/supervisor…"   2 minutes ago        Up 2 minutes        0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp, 8888/tcp   erp_techmedia_co_in




(venv) root@srv911881:/home/codexion#

```
docker exec -it erp_techmedia_co_in bash
```


devops@b182450a83f3:~$


for file folder permission

 sudo chown -R $USER:$USER .
 

bench init frappe --frappe-branch version-15

cd frappe/
```
bench start
```
```
bench new-site erp.techmedia.co.in
```

bench new-site erp.techmedia.co.in \
  --admin-password admin123 \
  --mariadb-root-username root \
  --mariadb-root-password DbPass1@@ \
  --db-host mariadb \
  --mariadb-user-host-login-scope='%'





```
bench --site erp.techmedia.co.in add-to-hosts
```
```
bench get-app erpnext --branch version-15
```
```
bench --site erp.techmedia.co.in install-app erpnext
```

```sh
bench start
```
```sh
npm install frappe-ui
```
```sh
bench get-app payments
```
```sh
bench --site erp.techmedia.co.in install-app payments
```
```sh
bench get-app hrms
```
```sh
bench --site erp.techmedia.co.in install-app hrms
```
```sh
```sh
bench get-app crm
```
```sh
bench --site erp.techmedia.co.in install-app crm
```
```sh
bench get-app builder
```
```sh
bench --site erp.techmedia.co.in install-app builder
```
```sh
bench get-app --branch version-15 https://github.com/resilient-tech/india-compliance.git
```
```sh
bench --site erp.techmedia.co.in install-app india_compliance
```
```sh
bench use erp.techmedia.co.in
```


sudo nano /etc/nginx/sites-available/erp.techmedia.co.in



server {
    listen 80;
    server_name erp.techmedia.co.in, 93.127.185.50;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Optional: support websocket if needed
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Optional static files caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 7d;
        log_not_found off;
    }
}


sudo ln -s /etc/nginx/sites-available/erp.techmedia.co.in /etc/nginx/sites-enabled/


sudo nginx -t
sudo systemctl reload nginx

 curl -I http://127.0.0.1:8000

result in side

HTTP/1.1 200 OK
Server: Werkzeug/3.0.6 Python/3.12.3
Date: Fri, 25 Jul 2025 13:16:53 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 346703
X-Page-Name: login
X-From-Cache: False
Link: </assets/frappe/dist/css/website.bundle.LY4S6Q3V.css>; rel=preload; as=style,</assets/erpnext/dist/css/erpnext-web.bundle.7VC5EUW7.css>; rel=preload; as=style,</assets/frappe/dist/css/login.bundle.2RW7DNMH.css>; rel=preload; as=style,</assets/frappe/dist/js/frappe-web.bundle.4XKJFVOE.js>; rel=preload; as=script,</website_script.js>; rel=preload; as=script,</assets/erpnext/dist/js/erpnext-web.bundle.253I7LT4.js>; rel=preload; as=script
Set-Cookie: sid=Guest; Expires=Fri, 01 Aug 2025 15:16:53 GMT; Max-Age=612000; HttpOnly; Path=/; SameSite=Lax
Set-Cookie: system_user=no; Path=/; SameSite=Lax
Set-Cookie: full_name=Guest; Path=/; SameSite=Lax
Set-Cookie: user_id=Guest; Path=/; SameSite=Lax
Set-Cookie: user_image=; Path=/; SameSite=Lax
Connection: close

server {
    listen 80;
    server_name erp.techmedia.co.in;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}


sudo certbot --nginx -d erp.techmedia.co.in