docker network ls
If it doesn’t show up, create it:

bash
Copy
Edit
docker network create codexion-network


(venv) root@srv911881:/home/codexion/docker# docker compose down mariadb
no configuration file provided: not found
(venv) root@srv911881:/home/codexion/docker# docker compose -f docker-compose-mariadb.yml down