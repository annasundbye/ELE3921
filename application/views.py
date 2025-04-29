from django.shortcuts import render, redirect
from .models import Pizza, Drink, Topping, User
from django.contrib.auth import authenticate, login as auth_login

def home(request):
   all_pizzas = Pizza.objects.all()
   
   return render(request, "home.html", {"pizzas": all_pizzas})

def menu(request):
   all_pizzas = Pizza.objects.all()
   all_drinks = Drink.objects.all()
   return render(request, "menu.html", {"pizzas": all_pizzas, "drinks": all_drinks})

def select_pizza(request, pizza_id):
   pizza = Pizza.objects.get(id=pizza_id)
   drinks = Drink.objects.all()
   toppings = Topping.objects.all()
   
   return render(request, "select-pizza.html", {
      "pizza": pizza, 
      "drinks": drinks, 
      "toppings": toppings
   })

def login(request):
   if request.method == "POST":
      username = request.POST.get("username")
      password = request.POST.get("password")
      
      user = authenticate(request, username=username, password=password)

      if user is not None:
         auth_login(request, user) 
         print("User logged in:", user.username)
         return redirect("/")
      else:
         print("You shall not pass!!!")
         return render(request, "login.html", {"error": "Invalid credentials."})

   return render(request, "login.html")

def cart(request):
   if request.method == "POST":
      if not request.user.is_authenticated:
         return redirect("/login")
      
      # do more stuff here later
      
      return render(request, "cart.html")
      
   if request.method == "GET":
      return render(request, "cart.html")