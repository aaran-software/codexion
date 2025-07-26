docker network ls
If it doesn’t show up, create it:

bash
Copy
Edit
docker network create codexion-network


(venv) root@srv911881:/home/codexion/docker# docker compose down mariadb
no configuration file provided: not found
(venv) root@srv911881:/home/codexion/docker# docker compose -f docker-compose-mariadb.yml down


docker run -it --rm --network=host mariadb mariadb -h 127.0.0.1 -u root -p

or

docker run -it --rm --network=codexion-network mariadb mariadb -h mariadb -u root -p



GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;


docker exec -it mariadb mariadb -u root -p
