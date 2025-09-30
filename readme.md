## Инструкция по запуску

Задать секреты в `Settings -> Secrets and variables -> Actions`, запустить деплой `Actions -> CD -> Run workflow`.

В консоли приложения применить миграции
```
python manage.py makemigrations ddsmgr
python manage.py migrate
```
и создать суперпользователя:
```
python manage.py createsuperuser
```