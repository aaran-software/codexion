 docker ps

CONTAINER ID   IMAGE                    COMMAND                  CREATED              STATUS              PORTS                                                   NAMES
0b245c2d03a5   mariadb:11.7             "docker-entrypoint.s…"   About a minute ago   Up About a minute   0.0.0.0:3306->3306/tcp, [::]:3306->3306/tcp             mariadb-codexion_db
b182450a83f3   erp_techmedia_co_in:v1   "/usr/bin/supervisor…"   2 minutes ago        Up 2 minutes        0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp, 8888/tcp   erp_techmedia_co_in




(venv) root@srv911881:/home/codexion# docker exec -it erp_techmedia_co_in bash

devops@b182450a83f3:~$