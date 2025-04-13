from django.shortcuts import render
from .models import Pizza, Drink

# mocking the pizzas for now.
# will get them from the database.
fake_pizzas = [
   Pizza(name="Basic AF (Margherita)", base_price=259.99, icon="🍅", description="Safe choice. Boring tho."),
   Pizza(name="You can't take this (Pepperoni)", base_price=229.99, icon="🍕", description="Loaded with pepperoni for when you're feeling extra. No cap."),
   Pizza(name="This one hot (Nduja)", base_price=299.99, icon="🌶️", description="Bro. Bro. Bro! This is hot."),
   Pizza(name="Cheesy x 4 (Quatro Formaggi)", base_price=219.99, icon="🧀", description="Just cheese. No explanation needed. It's giving simplicity."),
   Pizza(name="No nothing (Vegan (none slayed))", base_price=119.99, icon="🥦", description="Veggies on veggies on veggies. It's the responsible choice."),
   Pizza(name="All the good stuff (Hella meat)", base_price=319.99, icon="🥩", description="Hella meat."),
]

drinks = [
   Drink(name="Orange juice", price=39.99, icon="🍊"),
   Drink(name="Lemonade", price=59.99, icon="🍋"),
   Drink(name="Ice Tea", price=45.99, icon="🌱"),
   Drink(name="Coca Cola", price=49.99, icon="🥤"),
   Drink(name="Water", price=49.99, icon="💦"),
   Drink(name="Sparkling Water", price=49.99, icon="🫧"),
]

def home(request):
   return render(request, "home.html", {"pizzas": fake_pizzas[:3]})

def menu(request):
   return render(request, "menu.html", {"pizzas": fake_pizzas, "drinks": drinks})