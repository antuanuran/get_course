1. В корне Проекта должны лежать 2 файла:
- Dockerfile
- run.sh

2. В корне Проекта билдим и пушим в Dockerhub образ:
docker build -t antuanuran/skillsup .
docker push antuanuran/skillsup

3. Заходим на сервер:
ssh root@79.174.93.205
переходим в папку "deploy_skillsup"

4. Делаем pull нового образа, который мы запушили:
docker pull antuanuran/skillsup

5. И перезапускаем контейнеры:
docker-compose down&&docker-compose up -d
