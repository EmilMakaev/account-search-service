## Результат
Посмотреть результат можно тут: [http://185.43.5.174/](http://185.43.5.174/)

## Инструкция
Для теста нужно добавить файл `hosts.ini` с адресом для подключения к серверу и добавить `.env` файл в этот путь: `./ansible/roles/web_app/files/.env`

## Пример переменных:
```plaintext
MYSQL_ROOT_PASSWORD=root_password
MYSQL_DATABASE=test_db
MYSQL_USER=test_user
MYSQL_PASSWORD=test_password
```

# Задание 2

## Запуск:

1. docker-compose up --build -d
2. cd app && python3 -m venv venv && source venv/bin/activate && pip install --no-cache-dir -r requirements.txt && python3 app.py
3. docker-compose exec clickhouse-server clickhouse-client --port 9000
4. SELECT ipv4, mac FROM default.user_list_table
   Сохраняем ipv4 и mac для использования в Redis
5. docker exec -it redis_container redis-cli
   Добавляем задачи в Redis из сохраненных ipv4 и mac. Добавляем ещё ipv4 и mac которые существующие в базе данных пример ниже
   RPUSH queue:search_task '{"ipv4":"255.11.247.0","mac":"FF0BF70000:FF0BF70000:FF0BF70000:FF0BF70000:FF0BF70000:FF0BF70000"}'
6. python3 app.py

## Уточнения, по необходимости могу исправить:

1. Данные на pastebin.com уходят, но настройки API я не делал, поэтому будет 400 ошибка
2. BD таблица создается и заполняется через Python, но есть ещё script ./not-used/create_table.sh
3. Python код сильно не структурировал, оставил более менее читаемым
4. Есть ещё пример в папке not-used, там мы бесконечно слушаем задачи с Redis
5. Redix задачи на уровне Python кода читаются, но не удаляются

# Задание 1

## Создаем следующие контейнеры:

1. Redis: один контейнер для Redis. Репликация Redis может быть настроена с использованием встроенного механизма репликации Redis.
2. MySQL (master-master): два контейнера MySQL для реализации master-master репликации.
3. MySQL Proxy: один контейнер для MySQL Proxy для балансировки нагрузки между MySQL контейнерами.
4. Apache и Nginx: один контейнер для Apache и один контейнер для Nginx для обработки запросов и взаимодействия с Python.
5. Python 2.7: создание Docker образа с Python 2.7 и установкой необходимых зависимостей.

### Образы в моем понимание используем все официальные и наш собственный созданные который содержит Python 2.7.

## Шаги развертывания:

1. Установка Docker на новый хост
2. Скачивание необходимых Docker образов Redis, MySQL, Apache, Nginx
3. Запуск контейнера Redis с необходимыми параметрами и настройками
4. Запуск двух контейнеров MySQL для реализации master-master репликации
5. Запуск контейнера MySQL Proxy для балансировки нагрузки
6. Запуск контейнеров Apache и Nginx для обработки запросов
7. Запуск контейнера с Python 2.7 с вашим сервисом
8. Настройка сетевых связей между контейнерами для обеспечения их взаимодействия
9. Проверка работоспособности сервиса внутри контейнеров
