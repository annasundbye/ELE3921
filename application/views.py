from django.shortcuts import render
from .models import Pizza, Drink

def home(request):
   all_pizzas = Pizza.objects.all()
   
   return render(request, "home.html", {"pizzas": all_pizzas})

def menu(request):
   all_pizzas = Pizza.objects.all()
   all_drinks = Drink.objects.all()
   return render(request, "menu.html", {"pizzas": all_pizzas, "drinks": all_drinks})

def select_pizza(request, pizza_id):
   pizza = Pizza.objects.get(id=pizza_id)
   return render(request, "select-pizza.html", {"pizza": pizza})