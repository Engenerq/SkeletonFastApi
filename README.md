# Тестовое задание

----


Написать приложение, которое по REST принимает запрос вида<br>
``` json
POST api/v1/wallets/<WALLET_UUID>/operation
{
    operationType: DEPOSIT or WITHDRAW,
    amount: 1000
}
```
после выполнять логику по изменению счета в базе данных
также есть возможность получить баланс кошелька
``` json
GET api/v1/wallets/{WALLET_UUID}
```
Cтек:
1. Фреймворк(любой на выбор)
   1. FastAPI
   2. Flask
   3. Django
2. База данных - Postgresql


Должны быть написаны миграции для базы данных с помощью liquibase (по желанию)<br>
Обратите особое внимание проблемам при работе в конкурентной среде (1000 RPS по одному кошельку).<br>
Ни один запрос не должен быть не обработан (50Х error)<br>
Предусмотреть соблюдение формата ответа для заведомо неверных запросов:
1. Когда кошелька не существует
2. Не валидный json
3. Недостаточно средств


Приложение должно запускаться в докер контейнере, база данных тоже, вся система должна подниматься с помощью
docker-compose
предусмотрите возможность настраивать различные параметры приложения и базы данных без пересборки контейнеров.<br>

Эндпоинты должны быть покрыты тестами.<br>
