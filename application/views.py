from django.shortcuts import render
from .models import ShoppingList

# Create your views here.
def index(request):
   return render(request, "index.html")

def shopping_lists(request):
    lists = ShoppingList.objects.get()
    
    context = {
        "lists": lists,
    }
    
    return render(request, "shopping_lists.html", context)
    
