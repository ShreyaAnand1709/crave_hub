from django.contrib import admin
from .models import Cart, Item, Restaurant, User 
# Register your models here.
admin.site.register(User)
admin.site.register(Restaurant)
admin.site.register(Item)
admin.site.register(Cart)