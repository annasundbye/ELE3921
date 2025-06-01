from django.contrib.auth.models import User
from django.db import models


class Size(models.Model):
    """Pizza size. Can be small, medium or large."""
    name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name

class Topping(models.Model):
    """The different kinds of topping on a pizza."""
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, default="")
    base_price = models.DecimalField(max_digits=6, decimal_places=2, default=15.00)
    
    def __str__(self):
        return self.name

class Pizza(models.Model):
    """This is the model for a pizza. 
    It has a name, the base price (can be adjusted on a sale for example) 
    and the available toppings."""
    name = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=6, decimal_places=2)
    available_toppings = models.ManyToManyField(Topping, blank=True)
    icon = models.CharField(max_length=255)
    description = models.CharField(max_length=100)
    available = models.BooleanField(default=True, db_index=True)
    
    def __str__(self):
        return self.name

class PizzaPrice(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together = ('pizza', 'size')

    def __str__(self):
        return f"{self.pizza.name} - {self.size.name}"

class Drink(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    icon = models.CharField(max_length=255)
    description = models.CharField(max_length=100)
    available = models.BooleanField(default=True, db_index=True)
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def total_price(self):
        return sum(item.total_price() for item in self.cartitems.all())
    
    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cartitems', on_delete=models.CASCADE)
    pizza = models.ForeignKey(PizzaPrice, null=True, blank=True, on_delete=models.PROTECT)
    drink = models.ForeignKey(Drink, null=True, blank=True, on_delete=models.PROTECT)
    toppings = models.ManyToManyField(Topping, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    
    def total_price(self):
        base_price = self.pizza.price if self.pizza else (self.drink.price if self.drink else 0)
        topping_cost = 0

        if self.pizza:
            size_name = self.pizza.size.name.lower()
            multiplier = {
                "small": 1.0,
                "medium": 1.25,
                "large": 1.5,
            }.get(size_name, 1.0)

            for topping in self.toppings.all():
                topping_cost += topping.base_price * multiplier

        return (base_price + topping_cost) * int(self.quantity)

    def __str__(self):
        return f"CartItem ({self.pizza or self.drink}) x{self.quantity}"


# an order is basically a cart, but checked out / payed for
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='orderitems', on_delete=models.CASCADE)
    pizza = models.ForeignKey(PizzaPrice, null=True, blank=True, on_delete=models.CASCADE)
    drink = models.ForeignKey(Drink, null=True, blank=True, on_delete=models.CASCADE)
    toppings = models.ManyToManyField(Topping, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    
    def total_price(self):
        base_price = self.pizza.price if self.pizza else (self.drink.price if self.drink else 0)
        topping_cost = 0

        if self.pizza:
            size_name = self.pizza.size.name.lower()
            multiplier = {
                "small": 1.0,
                "medium": 1.25,
                "large": 1.5,
            }.get(size_name, 1.0)

            for topping in self.toppings.all():
                topping_cost += topping.base_price * multiplier

        return (base_price + topping_cost) * int(self.quantity)

    
    def __str__(self):
        return f"OrderItem ({self.pizza or self.drink}) x{self.quantity}"
