## "Skillsup" PROJECT
#### BD:     https://miro.com/app/board/uXjVMn6bPlI=/

### Technical requirement

### Работа в ADMIN:
- [x] Создание и редактирование Курса+Уроков+Заданий+Тегов (может Куратор/Автор курса)
- [x] Добавление Куратора (проверяющего) на курс с настройкой прав доступа. Назначает куратора - Суперюзер (Админ)
- [x] Задания могут быть 2-х видов: с автоматической проверкой + вариантами ответов (тест) и с индивидуальной проверкой куратора
- [x] Результаты ответов приходят автоматически в Админку. Либо статус - "success" ставится автоматически / либо куратором
- [x] После оплаты курса, студент может оставить Отзыв на свой курс. Отзыв приходит в Админку на утверждение и публикацию куратору
- [x] Загрузка запрещенных слов (для отзывов и комментариев) и дальнейшая автоматическая модерация текста по данным стоп-словам
- [x] Возможность отправки/получение ссылки на оплату с Платежной системой (доп. API). При оформлении Заказа, статус: "Created". После оплаты - "completed".
- [x] Дополнительное API в Админке (кнопки активации / переключатели)
- [x] Ручное изменение статусов Покупки (CREATED, COMPLETED, FAILED и т.д.)
- [x] Работа с Холдером (загрузка ссылок, видео и фото - файлов) для дальнейшего использования в Курсах/Комментариях/Отзывах
- [x] Возможность добавлять в любом порядке и изменять порядок Уроков внутри Курса
- [x] Возможность генерации Сертификатов (PDF) при завершении курса (celery)



### Работа с API (Django REST Framework):
- [x] Создание User (email / password) / Token через **JWT**-авторизацию
- [x] Работа с Get-запросами через **Dynamic REST** (сокращенный / расширенный вывод информации)
- [x] Работа с "переключателем" (добавить в избранное / убрать из избранного)
- [x] Настроить аутентификацию для вывода информации по соотвествующим правам (автор или куратор курса / оплачен курс / нет прав)
- [x] Настройка дополнительных boolean для Курса (активный / купленный / избранный)
- [x] Покупка Курса (неоплаченного) с автоматическим созданием статуса (CREATED)
- [x] Настройка Оплаты на стороннем сервисе:
  - [x] подготовить каркас кода перед подключением Сервиса для дальнейшей интеграции любой платежной системы
  - [x] подключить платежный шлюз (в нашем случае - https://app.leadpay.ru/)
  - [x] настроить псевдо-ответ от Шлюза с отправкой статуса "success" (имитация успешной оплаты). Далее статус переводится в "completed"
- [x] Работа с Заданиями к Урокам
  - [x] отправка ответа с автоматической проверкой
  - [x] отправка индивидуального ответа с проверкой Куратора
- [x] загрузка фото/видео/ссылок через API в Холдер и присвоение uuid для дальнейшего использования в Отзывах, Комментариях и Ответах к Заданиям
- [x] Подсистема отзывов
  - [x] создание отзыва в соответствии с правами и доступом (доступ при оплате курса / куратор согласовывает публикацию отзыва)
  - [x] первоначальная автоматическая проверка на стоп-слова
  - [x] загрузка фото в отзыв через отправку уникального - uuid
  - [x] модерация (публикация) Куратором через админку
- [x] Комментарии к урокам
  - [x] создание комментария в соответствии с правами и доступом (зарегистрированный пользователь / куратор)
  - [x] автоматическая проверка на стоп-слова
  - [x] загрузка фото в комментарий с учетом уникального uuid
  - [x] публикация комментария происходит автоматически (без дополнительного согласования)
- [x] куратор/автор Курса может комментировать и удалять комментарии
- [x] Автоматическая генерация Сертификатов (PDF) при завершении курса (celery)
- [x] Настройка вывода Ошибок в Api-формате
- [x] Настройка Swagger

### Main features
- [x] Настройка Загрузки видео и иных файлов в holder и последующим использованием в контенте
- [x] Добавление Тегов в Курсах для будущего поиска
- [x] Возможность загрузки (Load) данных (напрямую / через csv-файлы)
- [x] Реализация всех необходимых Моделей БД с определенными доступами:
  - [x] доступы к Урокам и Заданиям имеют Пользователи, которые оплатили Курс
- [x] Работа с Заданиями к урокам
  - [x] автоматизированная проверка (выбор правильных ответов)
  - [x] индивидуальная проверка (проверяет Админ)
  - [x] результаты всех ответов пользователей формируются в Админке
- [x] Добавить кураторов на курс для проверки и помощи студентам
- [x] Реализовать разные политики открытия Уроков в Курсах
  - [x] купил и сразу открыто
  - [x] уроки открываются по расписанию
  - [x] уроки открываются после прохождения тестов
- [x] Автоматическая генерация Сертификатов (PDF) при завершении курса (celery)
- [x] Отправка Сертификата по email (celery) + настроить redis в deploy
- [x] Добавить pytests в CI/CD
- [ ] Добавить Rabbit в Celery в CI/CD
- [ ] Настроить CORS
- [ ] Оптимизация запросов / Рефакторинг

- [ ] Dop. Project: scrapy для анализа средней цены на hh по конкретному курсу

### Deploy
- [x] Автоматический Checkout, Build, Deploy через **cicd**
  - [x] Подключение СУБД - PostgreSQL (Docker-container)
  - [x] Checkout black / isort / flake8
  - [x] Building - образа на Dockerhub
  - [x] Развертывание Проекта на удаленном Ubuntu-сервере
- [x] Server:  http://api.skillsup.fun/admin/
- [x] Swagger: http://api.skillsup.fun/docs/swagger/
- [x] postman: https://skills-up.postman.co/workspace/skills-up~532ccf51-bc2b-4914-ac2d-6ad0831f096c/folder/9556154-0563bf17-166c-4694-9b5c-70911ca4a506

#### Login Admin User:
- "email": "python@admin.org",
- "password": "develop12345"

#### Login Admin SuperUser:
- "email": "*****",
- "password": "******"
