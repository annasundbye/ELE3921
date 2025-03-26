from django.contrib import admin

# Register your models here.
from .models import Size, Topping, Pizza, PizzaPrice, Drink, Order, OrderItem, Cart

admin.site.register(Size)
admin.site.register(Topping)
admin.site.register(Pizza)
admin.site.register(PizzaPrice)
admin.site.register(Drink)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)