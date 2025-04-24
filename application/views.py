from django.shortcuts import render, redirect
from .models import Pizza, Drink, Topping, User
from django.contrib.auth.hashers import check_password

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

def get_user_by_username(username):
    try:
        user = User.objects.get(username=username)
        return user
    except User.DoesNotExist:
        return None

def login(request):
   if request.method == "POST":
      username = request.POST.get("username")
      password = request.POST.get("password")
      print("LOGGED IN USER", username, password)

      user = get_user_by_username(username)
      if user is None:
         print("You shall not pass!!!")
         return render(request, "login.html")
      
      if not check_password(password, user.password):
         print("You shall not pass!!!")
         return render(request, "login.html")
      
      return redirect("/")

   return render(request, "login.html")