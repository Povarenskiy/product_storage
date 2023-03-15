from django.contrib import admin
from .models import *


admin.site.register(Item)
admin.site.register(Storage)
admin.site.register(Client)

admin.site.register(StorageItemPriceAndCapacity)
admin.site.register(StorageTotalCapacity)

admin.site.register(TransportationCost)
admin.site.register(ClientItem)
