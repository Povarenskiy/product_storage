import random
import os
from django.core.management.base import BaseCommand
from market.models import *

from django.conf import settings

def get_random_range(amount):
    return range(random.randint(1, amount))

def get_random_int(max_int, min_int=1):
    return random.randint(min_int, max_int)


class Command(BaseCommand):
    help = 'Генерация рынка предложений'

    def add_arguments(self, parser):
        parser.add_argument('-N', '--new', action='store_true', help='Удалить текущий рынок предложений')

    def handle(self, *args, **kwargs):
        new = kwargs['new']

       

        if new:
            Storage.objects.all().delete()
            Item.objects.all().delete()

        storages = Storage.objects.bulk_create([Storage(name=f'S{i}') for i in range(settings.STORAGES_NUMBER)])

        items = Item.objects.bulk_create([Item(name=f'I{i}') for i in range(settings.ITEM_NUMBER)])

        storage_single_capacity = []
        storage_total_capacity = []
        for storage in storages:
            storage_items = {random.choice(items) for _ in get_random_range(settings.MAX_STORAGE_ITEM_NUMBER)}
            total_items_capacity = 0
            for item in storage_items:
                item_capacity = get_random_int(settings.MAX_ITEM_CAPACITY) 
                total_items_capacity += item_capacity

                storage_single_capacity.append(StorageItemPriceAndCapacity(
                    storage=storage,
                    item=item,
                    capacity=item_capacity,
                    price=get_random_int(settings.MAX_ITEM_PRICE)
                ))
            
            total_items_capacity = get_random_int(total_items_capacity, min_int=int(total_items_capacity * 0.5))
            storage_total_capacity.append(StorageTotalCapacity(storage=storage, total_capacity=total_items_capacity))

        storage_single_capacity = StorageItemPriceAndCapacity.objects.bulk_create(storage_single_capacity)
        storage_total_capacity = StorageTotalCapacity.objects.bulk_create(storage_total_capacity)
        
        
