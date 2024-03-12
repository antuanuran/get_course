## "Skillsup" PROJECT
#### Server: http://79.174.93.205/admin/
#### BD:     https://miro.com/app/board/uXjVMn6bPlI=/

### Technical requirement

### работа в ADMIN:
- [x] Загрузка (Load) данных (напрямую / через csv-файлы)
- [x] Реализация доп.API (кнопки активации / переключатели / отправки данных) напрямую в Админке
- [x] Ручное подтверждение публикации Отзыва к Курсу
- [x] Загрузка запрещенных слов (в отзывах и комментариях) и дальнейшая автоматическая модерация текста
- [x] Изменение статусов Покупки (CREATED, COMPLETED, FAILED и т.д.)
- [x] Работа с Холдером (загрузка видео и фото - файлов) для дальнейшего использования в Моделях


### работа с API (Django REST Framework):
- [x] Создание User (email / password) / Token через **JWT**-авторизацию
- [x] Работа с Get-запросами через **Dynamic REST** (сокращенный / расширенный вывод информации)
- [x] Работа с "переключателем" (добавить в избранное / убрать из избранного)
- [x] Настроить аутентификацию для вывода информации по соотвествующим правам (автор курса / оплачен курс / нет прав)
- [x] Настройка дополнительных boolean для Курса (активный / купленный / избранный)
- [x] Покупка Курса (неоплаченного) с автоматическим созданием статуса (CREATED)
- [x] Настройка Оплаты на стороннем сервисе:
  - [x] подготовить каркас кода перед подключением Сервиса для дальнейшей интеграции любой платежной системы
  - [x] подключить платежный шлюз (в нашем случае - https://app.leadpay.ru/)
  - [x] настроить псевдо-ответ от Шлюза с отправкой статуса "success" (имитация успешной оплаты)
- [x] Работа с Заданиями к Урокам
  - [x] отправка ответа с автоматической проверкой
  - [x] отправка индивидуального ответа с проверкой Админа
- [x] загрузка фото через через API в Холдер и присвоение uuid для дальнейшего использования в Отзывах и Комментариях
- [x] Подсистема отзывов
  - [x] создание отзыва в соответствии с правами и доступом (курс оплачен - отзыв разрешен)
  - [x] первоначальная автоматическая проверка на стоп-слова
  - [x] загрузка фото в отзыв с учетом уникального uuid
  - [x] модерация (публикация) через админку
- [x] Комментарии к урокам
  - [x] создание комментария в соответствии с правами и доступом
  - [x] автоматическая проверка на стоп-слова
  - [x] загрузка фото в комментарий с учетом уникального uuid

- [x] Настройка вывода Ошибок в Api-формате
- [x] Настройка Swagger

### Main features
- [x] Настройка Загрузки видео и иных файлов в holder и последующим использованием в контенте
- [x] Добавление Тегов в Курсах для будущего поиска
- [x] Реализация всех необходимых Моделей БД с определенными доступами:
  - [x] доступы к Урокам и Заданиям имеют Пользователи, которые оплатили Курс
- [x] Работа с Заданиями к урокам
  - [x] автоматизированная проверка (выбор правильных ответов)
  - [x] индивидуальная проверка (проверяет Админ)
  - [x] результаты всех ответов пользователей формируются в Админке
- [ ] Добавить кураторов на курс для проверки и помощи студентам
- [ ] Настроить CORS
- [x] Реализовать разные политики открытия Уроков в Курсах
  - [x] купил и сразу открыто
  - [x] уроки открываются по расписанию
  - [x] уроки открываются после прохождения тестов
- [ ] Генерация сертификатов для завершенного курса + email (celery)
- [ ] IDEA: scrapy для анализа средней цены на hh, если пройти этот курс
- [ ] оптимизация запросов

### Deploy
- [x] Автоматический Checkout, Build, Deploy через **cicd**
  - [x] Подключение СУБД - PostgreSQL (Docker-container)
  - [x] Checkout black / isort / flake8
  - [x] Building - образа на Dockerhub
  - [x] Развертывание Проекта на удаленном Ubuntu-сервере
- [x] Server: http://79.174.93.205/admin/
- [x] Swagger: http://79.174.93.205/docs/swagger/
- [x] postman: https://skills-up.postman.co/workspace/skills-up~532ccf51-bc2b-4914-ac2d-6ad0831f096c/folder/9556154-0563bf17-166c-4694-9b5c-70911ca4a506
