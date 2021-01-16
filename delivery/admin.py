from django.contrib import admin

# Register your models here.
from .models import User, Food, Restaurant, Order

admin.site.register(User)
admin.site.register(Food)
admin.site.register(Restaurant)
admin.site.register(Order)