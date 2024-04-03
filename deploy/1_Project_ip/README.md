1. В корне Проекта должны лежать 2 файла:
- Dockerfile
- run.sh

2. В корне Проекта билдим и пушим в Dockerhub образ:
docker build -t antuanuran/skillsup .
docker push antuanuran/skillsup

3. Заходим на сервер:
ssh root@79.174.93.205
переходим в папку с файлами "deploy", в которой должны лежать 3 файла (docker-compose, nginx, .env)

4. Делаем pull нового образа, который мы запушили:
docker pull antuanuran/skillsup

5. И перезапускаем контейнеры:
docker-compose down&&docker-compose up -d

6. Cicd
Перед запуском нужно в Проекте прописать 2 секретных ключа:
PASSWORD_HUB - это пароль от DockerHub
SSH_KEY - это непубличный ssh-ключ от удаленного сервера

И теперь последний штрих - нам нужно настроить право компьютера размещать на сервере проект, для этого нам нужно:
- зайти на сервер
и в файле authorization_keys разместить 2 публичных ключа:
- от компьютера.pub
- от сервера.pub
