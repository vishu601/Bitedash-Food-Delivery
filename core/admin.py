from django.contrib import admin
from .models import FoodItem, Order, DeliveryLocation

admin.site.register(FoodItem)
admin.site.register(Order)
admin.site.register(DeliveryLocation)