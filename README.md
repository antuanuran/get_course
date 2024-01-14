# "Get course" PROJECT Uranov Anton

## Idea
MIRO: https://miro.com/app/board/uXjVMn6bPlI=/

1. Юзер логинится и видит все свои покупки
2. Каталог курсов для покупки с поиском по тегам и названию
3. Подсистема заданий (+ проверка автоматическая и ручная)
4. Прогресс прохождения
5. Подсистема отзывов
6. Открытие уроков по расписанию или по прохождению (опционально)
7. Генерация сертификатов по прохождению
8. Экспорт и импорт информации

## Develop

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
6. git remote add origin git@github.com:antuanuran/get_course.git
7. git push -u origin master

### для инфо по Докеру:
1. Проверить порты:  netstat -ntlp | grep 80
2. Остановить порт:  fuser -n tcp -k 8000
3. Остановить nginx: systemctl stop nginx
