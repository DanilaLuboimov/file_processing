# File processing
![](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&color=05f) 
![](https://img.shields.io/badge/PostgresSQL-15.1-blue?style=flat-square&color=05f) 
![](https://img.shields.io/badge/Redis-5.0.0-blue?style=flat-square&color=423d45) 
![](https://img.shields.io/badge/Django-4.2.4-blue?style=flat-square&color=004f0d) 
![](https://img.shields.io/badge/DRF-3.14.0-blue?style=flat-square&color=red) 
![](https://img.shields.io/badge/Celery-5.3.3-blue?style=flat-square&color=1ab04c) 
![](https://img.shields.io/badge/Pillow-10.0.0-blue?style=flat-square&color=004f4f) 
![](https://img.shields.io/badge/Docker--compose-3.8-blue?style=flat-square&color=05f) 
![](https://img.shields.io/badge/Gunicorn-21.2.0-blue?style=flat-square&color=004f4f) 
![](https://img.shields.io/badge/Nginx-blue?style=flat-square&color=05f) 


## Description

Проект реализует функционал загрузки файлов на сервер и обработки файлов по 
средствам celery<br>
Для повышения производительности подключен nginx и gunicorn с несколькими 
рабочими (2 * количество ядер + 1)<br>
Существует два docker-compose для запуска проекта и тестов

### Запуск проекта
1. Создать папку pg_data для базы данных
2. Ввести команду в корневой папке проекта
~~~
docker-compose -f ./docker/file_processing_production/docker-compose.yaml --env-file .env up
~~~

### Запуск тестов
1. Ввести команду в корневой папке проекта
~~~
docker-compose -f ./docker/file_processing_tests/docker-compose.yaml --env-file .env up --abort-on-container-exit
~~~


### Requests per second

~~~
loadtest -c 10 --rps 200 http://127.0.0.1/api/files/
~~~
![img.png](img.png)


~~~
loadtest -c 10 --rps 200 http://127.0.0.1/
~~~
![img_1.png](img_1.png)


### Оптимизация 

1. Использовать пакетные вставки в базу, чтобы снизить число подключений
2. Добавить кэширование
3. Линейно масштабировать приложение
