from django.db import models

class Storage(models.Model):
    """Модель склада"""
    name = models.CharField(max_length=55)

class Client(models.Model):
    """Модель клиента"""
    name = models.CharField(max_length=55)

class Item(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=55)


class StorageItemPriceAndCapacity(models.Model):
    """Модель стоимости и лимита хранения для товара на складе"""
    price = models.IntegerField()
    capacity = models.IntegerField()
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


class StorageTotalCapacity(models.Model):
    """Модель полного лимита хранения на складе"""
    total_capacity = models.IntegerField()
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    

class TransportationCost(models.Model):
    """Модель стоимости транспортировки"""
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    cost = models.IntegerField()
    

class ClientItem(models.Model):
    """Модель товаров клиента"""
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.IntegerField()



