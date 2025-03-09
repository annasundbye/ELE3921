from django.contrib import admin

# Register your models here.
from .models import ShoppingList

admin.site.register(ShoppingList)