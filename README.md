# "Get course" PROJECT Uranov Anton

### Настройка (for linux):
1. Переходим в корень Проекта и создаем вортуальное окружение: **python3 -m venv .venv**
2. Активируем виртуальное окружение: **source .venv/bin/activate**
3. **pip install -r requirements.txt**
4. **pip install -r requirements-dev.txt**
5. **.env.template -> .env**


### Git settings:
1. git clone https://github.com/antuanuran/get_course
2. git pull
3. git branch -M master
4. git add --all
5. git commit -m " text "
4. git remote add origin git@github.com:antuanuran/get_course.git 
5. git push -u origin master

### для инфо по Докеру:
1. Проверить порты:  netstat -ntlp | grep 80
2. Остановить порт:  fuser -n tcp -k 8000
3. Остановить nginx: systemctl stop nginx
