import random
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from market.models import *

from .create_market import get_random_range, get_random_int


def get_cheap_option(client_id, client_items):
    """
    Транспортировка товаров пользователя дешевым способом
    """
    print('Выбран самый дешевый вариант')
    
    for item in client_items:
        
        # SQL запрос на поиск оптимального склада по стоимости хранения и транспортировки
        raw_sql = f'SELECT s_i.id FROM market_storageitempriceandcapacity as s_i\
                    LEFT JOIN market_transportationcost as t_c\
                    ON t_c.storage_id=s_i.storage_id\
                    LEFT JOIN market_storagetotalcapacity s_c\
                    ON s_c.storage_id=s_i.storage_id\
                    WHERE s_i.item_id={item.id} \
                    AND t_c.client_id={client_id}\
                    AND s_i.capacity > 0\
                    AND s_c.total_capacity > 0\
                    ORDER BY t_c.cost * s_i.price\
                    LIMIT 1'
        
        while client_items[item].amount > 0:   
            cheapest_storage = StorageItemPriceAndCapacity.objects.raw(raw_sql)
            
            if cheapest_storage:                
                cheapest_storage = cheapest_storage[0]
                # Текущий общий лимит на хранение на складе
                storage_total_remaining_capacity = StorageTotalCapacity.objects.get(storage_id=cheapest_storage.storage.id)
                
                # Определяем доступное количество товара для транспортиовки  
                items_transport_amount = min(
                    cheapest_storage.capacity,
                    client_items[item].amount,
                    storage_total_remaining_capacity.total_capacity)

                # Перемещение товара и учет изменения лимитов хранения 
                client_items[item].amount -= items_transport_amount
                cheapest_storage.capacity -= items_transport_amount
                storage_total_remaining_capacity.total_capacity -= items_transport_amount
                
                client_items[item].save()
                cheapest_storage.save()
                storage_total_remaining_capacity.save()

                print(f'Товар: {item} на склад: {cheapest_storage.storage} в количестве: {items_transport_amount}')
            else:
                print(f'Для товара {item} не удалось найти вариант хранения')
                break


def get_convenient_option(client_id, client_items):
    """
    Транспортировка товаров пользователя удобным способом
    """
    print('Выбран самый удобный вариант')

    # SQL запрос на поиск оптимального склада по доступного лимиту хранения
    raw_sql = f'SELECT c_i.id, c_i.client_id, s_i.storage_id,\
                CASE \
                    WHEN SUM(s_i.capacity) <= AVG(s_c.total_capacity) THEN SUM(s_i.capacity)\
                    ELSE AVG(s_c.total_capacity)\
                    END as avaible \
                FROM market_clientitem c_i\
                LEFT JOIN market_storageitempriceandcapacity s_i\
                ON c_i.item_id=s_i.item_id\
                LEFT JOIN market_storagetotalcapacity s_c\
                ON s_c.storage_id=s_i.storage_id\
                WHERE c_i.client_id={client_id} AND c_i.amount > 0\
                GROUP BY s_i.storage_id\
                HAVING avaible > 0\
                ORDER BY avaible DESC\
                LIMIT 1'
    
    while client_items:
        biggest_storage = ClientItem.objects.raw(raw_sql)
        if biggest_storage:

            storage = Storage.objects.\
                prefetch_related('storagetotalcapacity_set').\
                prefetch_related('storageitempriceandcapacity_set__item').\
                get(pk=biggest_storage[0].storage_id)

            # Текущий общий лимит на хранение на складе
            storage_total_remaining_capacity = storage.storagetotalcapacity_set.get()
            # Информация по товарам у клиента
            storage_items_data = storage.storageitempriceandcapacity_set.all()
            
            # Выбираем общие товары доступные для хранения и у клиента
            items_to_storage = [i for i in storage_items_data if i.item in client_items]
            
            for item_info in items_to_storage:

                # Определяем доступное количество товара для транспортиовки  
                items_transport_amount = min(
                    client_items[item_info.item].amount, 
                    item_info.capacity,
                    storage_total_remaining_capacity.total_capacity)

                if items_transport_amount:
                    
                    # Перемещение товара и учет изменения лимитов хранения 
                    client_items[item_info.item].amount -= items_transport_amount 
                    item_info.capacity -= items_transport_amount
                    storage_total_remaining_capacity.total_capacity -= items_transport_amount

                    client_items[item_info.item].save() 
                    storage_total_remaining_capacity.save()
                    item_info.save()
                    
                    # Убираем из списка товары с 0 количеством 
                    if not client_items[item_info.item].amount:
                        client_items.pop(item_info.item)            

                    print(f'Товар: {item_info.item} на склад: {storage} в количестве: {items_transport_amount}')
        
        else:
            # Если доступного хранилища нет, сообщаем о невозможности разместить
            # оставшиеся товары
            for item in client_items:
                print(f'Для товара {item} не удалось найти вариант хранения') 
            client_items.clear()


class Command(BaseCommand):
    help = 'Цикл генерации клиентов и распределения товаров по складам'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Указывает сколько клиентов необходимо создать')

    def handle(self, *args, **kwargs):
        for i in range(0, kwargs['total']):
            client = Client.objects.create(name=f'C{i}') 
            
            storages = Storage.objects.all()
            items = Item.objects.all()

            items_set = {random.choice(items) for _ in get_random_range(settings.MAX_CLIENT_ITEM_NUMBER)}

            # Генерация товров у клиента
            client_items = ClientItem.objects.bulk_create([
                ClientItem(
                    amount=get_random_int(settings.MAX_CLIENT_ITEM_AMOUNT),
                    client=client,
                    item=item)
                for item in items_set])

            # Генерация стоимости достаки до складов
            TransportationCost.objects.bulk_create([
                TransportationCost(
                    cost=get_random_int(settings.MAX_DISTANCE) * settings.TRANSPORTATION_RATE,
                    client=client,
                    storage=storage)
                for storage in storages])

            print('Информациия по клиенту'.center(60, '*'))       
            print(f'Клиент: {client}, количество видов товаров: {len(client_items)}')
            
            print('Информациия по товарам'.center(60, '.'))   
            for i in client_items:
                print(f'Товар: {i} в колличестве {i.amount}')    
            
            print('Информациия по доставке'.center(60, '.'))

            # Уточнение спииска товаров для транспортировки и запись в виде словаря  
            client_items = {i.item: i for i in client_items if i.amount > 0}
            # Уточнение спииска товаров для транспортировки
            random.choice([get_convenient_option, get_cheap_option])(client.id, client_items)
            
            print('Транспортировка закончена'.center(60, '*'), '\n')          
            
             
            
            


                