# "Skillsup" PROJECT resume
# Server: http://79.174.93.205/admin/
## Progress

### basic work
- [x] настройка JWT-авторизации (email / password)
- [x] настройка Админки (создание курсов / покупки / избранное) + фильтрация / сортировки
- [x] настройка Загрузки видео и иных файлов в holder и последующим использованием в контенте
- [x] добавление Тегов в курсах для будущего поиска
- [ ] разработка всех необходимых Моделей для БД
  - [x] доступы (проблема доступа к урокам)
  - [x] задания (автоматизированные и не только)
  - [x] описать ответ юзера (сериализатор)
  - [ ] автоматизированная проверка для auto_test=True
  - [ ] реализовать эндпоинты для получения и проверки ответов
- [ ]
- [ ]

### работа с API:
- [x] Вывод списков курсов с учетом аутентификации / авторства
- [x] Перевод курса в избранное / убрать из избранного
- [x] Вывод информации по курсам (как сокращенный список, так и расширенный)
- [x] Вывод дополнительной информации по курсу (куплен / в избранном или создан автором)
- [x] Отправка курса в покупки + изменение статуса (CREATED / COMPLETED и т.д.)
- [x] Настройка вывода Ошибок в Api-стиле
- [x] Настройка Swagger
- [x] Настройка Api для оплат
  - [x] подготовить каркас кода
  - [x] подключить платежный шлюз

---
## Предварительный план работ

- Data base: https://miro.com/app/board/uXjVMn6bPlI=/
- Юзер логинится и видит все свои покупки
   1. api логина (+ подсистема прав)
   2. api для совершения покупок
   3. api добавления/удаления избранного
   4. api для просмотра покупок и избранного
- Каталог курсов для покупки с поиском по тегам и названию
- Подсистема заданий (+ проверка автоматическая и ручная)
- Прогресс прохождения
- Подсистема отзывов
- Открытие уроков по расписанию или по прохождению (опционально)
- Генерация сертификатов по прохождению
- Экспорт и импорт информации
