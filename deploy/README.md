## Process deploy

1. Устанавливаем Docker:
- curl -fsSL https://get.docker.com -o get-docker.sh
- sh get-docker.sh
- systemctl start docker
- docker version

2. Устанавливаем Docker-compose:
- curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
- chmod +x /usr/local/bin/docker-compose
- docker-compose --version

3. Заходим в /srv/ и
- git clone https://github.com/antuanuran/deploy

4. заходим в server_nginx и запускаем (заглушка - если один домен. Если разные, то прописываем)
- docker-compose up -d

5. Заходим в server_project и меняем:
- .env:       добавляем в allowed_hosts - доменное имя, которое связываем с ip-сервера. Если хотим доступ с ip - то и его добавляем

6. Заходим на сервер в папку .ssh и создаем ssh-ключи внутри нее:
- ssh-keygen -t ed25519 -f github
- и затем НЕ вводим пароль 2 раза (просто энтер и энтер)

7. Копируем НЕпубличный ключ (github) и вставляем его в Github - SSH_KEY

8. Копируем публичный ключ и вставляем его в файл authorized_keys а также копируем публичный ключ с нашего компьютера и вставляем его туда же
