docker network ls
If it doesn’t show up, create it:

docker network create codexion-network


(venv) root@srv911881:/home/codexion/docker# docker compose down mariadb
no configuration file provided: not found
(venv) root@srv911881:/home/codexion/docker# docker compose -f docker-compose-mariadb.yml down

```
docker run -it --rm --network=host mariadb mariadb -h 127.0.0.1 -u root -p
```
or
```
docker run -it --rm --network=codexion-network mariadb mariadb -h mariadb -u root -p
```

remote access for root user 

```
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

```
docker exec -it mariadb mariadb -u root -p
```


✅ 4. Verify the Config is Active
You can check from inside the container:

```
docker exec -it mariadb mariadb -uroot -pDbPass1@@ -e "SHOW VARIABLES LIKE 'character_set%';"
```

4. Allow access on your Ubuntu host (firewall):
If using UFW:

```
sudo ufw allow 3306/tcp
sudo ufw reload
```
shows

Rules updated
Rules updated (v6)
Firewall not enabled (skipping reload)



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


sudo ufw status

status : inactive