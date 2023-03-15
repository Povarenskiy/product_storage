# Product Storage

## 1 Установка 

Клонировать репозиторий с Github.com, перейти внутрь проекта  
````
git clone https://github.com/Povarenskiy/product_storage.git
cd product_storage
````
Установить и настроить виртуальное окружение
````
python -m venv venv

venv\Scripts\activate        # on Windows
source venv/bin/activate     # on Linux
````
Провести миграции в базу данных 
````
python manage.py migrate            
````

## 2 Запуск
Указать настройки генератора маркета в .\product_storage\settings.py при необходимости.
На данный момент выставлены следующие настройки: 
````
ITEM_NUMBER = 50                # Количество разных товаров
STORAGES_NUMBER = 3000          # Количество складов
MAX_STORAGE_ITEM_NUMBER = 10    # Максимальное количество типов товаров на складе 
MAX_ITEM_CAPACITY = 20          # Лимит хранения товара 
MAX_ITEM_PRICE = 20             # Максимальная цена за хранение товара

MAX_DISTANCE = 10               # максимальное расстояние от склада до клиента
TRANSPORTATION_RATE = 0.01      # стоимость 1 км транспортировки единицы товара
MAX_CLIENT_ITEM_NUMBER = 10     # максимальное количество видов товаро у клиента 
MAX_CLIENT_ITEM_AMOUNT = 50     # максимальное количество одного товара у клиента
````

Сгенерировать маркет
````
python manage.py create_market      # можно добавить --new для удаления удаления старых записей
````
Запустить цикл с указанием количества итераций 
````
python manage.py run 100       
````

## 3 Пример работы
````
python manage.py run 3              
*******************Информациия по клиенту*******************
Клиент: Client object (13), количество видов товаров: 8
...................Информациия по товарам...................
Товар: ClientItem object (71) в колличестве 47
Товар: ClientItem object (72) в колличестве 26
Товар: ClientItem object (73) в колличестве 21
Товар: ClientItem object (74) в колличестве 7
Товар: ClientItem object (75) в колличестве 17
Товар: ClientItem object (76) в колличестве 33
Товар: ClientItem object (77) в колличестве 21
Товар: ClientItem object (78) в колличестве 45
..................Информациия по доставке...................
Выбран самый дешевый вариант
Товар: Item object (131) на склад: Storage object (6001) в количестве: 6
Товар: Item object (131) на склад: Storage object (6002) в количестве: 8
Товар: Item object (131) на склад: Storage object (6022) в количестве: 19
Товар: Item object (131) на склад: Storage object (6024) в количестве: 14
Товар: Item object (133) на склад: Storage object (6005) в количестве: 15
Товар: Item object (133) на склад: Storage object (6008) в количестве: 11
Товар: Item object (110) на склад: Storage object (6024) в количестве: 16
Товар: Item object (110) на склад: Storage object (6031) в количестве: 3
Товар: Item object (110) на склад: Storage object (6036) в количестве: 2
Товар: Item object (111) на склад: Storage object (6015) в количестве: 7
Товар: Item object (112) на склад: Storage object (6002) в количестве: 2
Товар: Item object (112) на склад: Storage object (6017) в количестве: 2
Товар: Item object (112) на склад: Storage object (6026) в количестве: 1
Товар: Item object (112) на склад: Storage object (6029) в количестве: 4
Товар: Item object (112) на склад: Storage object (6044) в количестве: 8
Товар: Item object (145) на склад: Storage object (6011) в количестве: 3
Товар: Item object (145) на склад: Storage object (6013) в количестве: 14
Товар: Item object (145) на склад: Storage object (6015) в количестве: 13
Товар: Item object (145) на склад: Storage object (6016) в количестве: 3
Товар: Item object (144) на склад: Storage object (6005) в количестве: 6
Товар: Item object (144) на склад: Storage object (6009) в количестве: 5
Товар: Item object (144) на склад: Storage object (6015) в количестве: 10
Товар: Item object (143) на склад: Storage object (6016) в количестве: 14
Товар: Item object (143) на склад: Storage object (6025) в количестве: 6
Товар: Item object (143) на склад: Storage object (6028) в количестве: 6
Товар: Item object (143) на склад: Storage object (6030) в количестве: 12
Товар: Item object (143) на склад: Storage object (6032) в количестве: 7
*****************Транспортировка закончена******************

*******************Информациия по клиенту*******************
Клиент: Client object (14), количество видов товаров: 4
...................Информациия по товарам...................
Товар: ClientItem object (79) в колличестве 10
Товар: ClientItem object (80) в колличестве 22
Товар: ClientItem object (81) в колличестве 17
Товар: ClientItem object (82) в колличестве 18
..................Информациия по доставке...................
Выбран самый удобный вариант
Товар: Item object (144) на склад: Storage object (8243) в количестве: 10
Товар: Item object (113) на склад: Storage object (8243) в количестве: 16
Товар: Item object (122) на склад: Storage object (8243) в количестве: 17
Товар: Item object (139) на склад: Storage object (6526) в количестве: 18
Товар: Item object (113) на склад: Storage object (6526) в количестве: 6
*****************Транспортировка закончена****************** 

*******************Информациия по клиенту*******************
Клиент: Client object (15), количество видов товаров: 7
...................Информациия по товарам...................
Товар: ClientItem object (83) в колличестве 38
Товар: ClientItem object (84) в колличестве 11
Товар: ClientItem object (85) в колличестве 4
Товар: ClientItem object (86) в колличестве 49
Товар: ClientItem object (87) в колличестве 24
Товар: ClientItem object (88) в колличестве 20
Товар: ClientItem object (89) в колличестве 14
..................Информациия по доставке...................
Выбран самый дешевый вариант
Товар: Item object (102) на склад: Storage object (6030) в количестве: 11
Товар: Item object (102) на склад: Storage object (6032) в количестве: 5
Товар: Item object (102) на склад: Storage object (6042) в количестве: 19
Товар: Item object (102) на склад: Storage object (6047) в количестве: 3
Товар: Item object (109) на склад: Storage object (6011) в количестве: 11
Товар: Item object (145) на склад: Storage object (6057) в количестве: 2
Товар: Item object (145) на склад: Storage object (6071) в количестве: 2
Товар: Item object (147) на склад: Storage object (6012) в количестве: 19
Товар: Item object (147) на склад: Storage object (6013) в количестве: 1
Товар: Item object (147) на склад: Storage object (6017) в количестве: 19
Товар: Item object (147) на склад: Storage object (6018) в количестве: 10
Товар: Item object (118) на склад: Storage object (6004) в количестве: 15
Товар: Item object (118) на склад: Storage object (6019) в количестве: 4
Товар: Item object (118) на склад: Storage object (6022) в количестве: 5
Товар: Item object (124) на склад: Storage object (6004) в количестве: 9
Товар: Item object (124) на склад: Storage object (6017) в количестве: 3
Товар: Item object (124) на склад: Storage object (6028) в количестве: 8
Товар: Item object (127) на склад: Storage object (6003) в количестве: 4
Товар: Item object (127) на склад: Storage object (6030) в количестве: 2
Товар: Item object (127) на склад: Storage object (6050) в количестве: 8
*****************Транспортировка закончена****************** 
````
