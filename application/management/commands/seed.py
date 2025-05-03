from django.core.management.base import BaseCommand
from application.models import Pizza, Drink, Topping

DEFAULT_TOPPINGS = [
    Topping(name="Tomato Sauce", icon="🍅"),
    Topping(name="Mozzarella", icon="🧀"),
    Topping(name="Pepperoni", icon="🌶️"),
    Topping(name="Nduja", icon="🔥"),
    Topping(name="Parmesan", icon="🧂"),
    Topping(name="Blue Cheese", icon="🔵"),
    Topping(name="Gorgonzola", icon="💙"),
    Topping(name="Vegan Cheese", icon="🌱"),
    Topping(name="Bell Pepper", icon="🫑"),
    Topping(name="Zucchini", icon="🥒"),
    Topping(name="Mushroom", icon="🍄"),
    Topping(name="Meat Mix", icon="🥩"),
    Topping(name="Ham", icon="🐖"),
    Topping(name="Bacon", icon="🥓"),
]

DEFAULT_PIZZAS = [
   Pizza(name="Basic AF (Margherita)", base_price=259.99, icon="🍅", description="Safe choice. Boring tho."),
   Pizza(name="You can't take this (Pepperoni)", base_price=229.99, icon="🍕", description="Loaded with pepperoni for when you're feeling extra. No cap."),
   Pizza(name="Hotter than hell (Nduja)", base_price=299.99, icon="🌶️", description="Bro. Bro. Bro! This is hot."),
   Pizza(name="Cheesy x 4 (Quatro Formaggi)", base_price=219.99, icon="🧀", description="Just cheese. No explanation needed. It's giving simplicity."),
   Pizza(name="No nothing (Vegan (none slayed))", base_price=119.99, icon="🥦", description="No animals were harmed making this pizza. It's the responsible choice."),
   Pizza(name="All the good stuff (Hella meat)", base_price=319.99, icon="🥩", description="Hella meat."),
]

PIZZA_TOPPING_MAP = {
    "Basic AF (Margherita)": ["Tomato Sauce", "Mozzarella"],
    "You can't take this (Pepperoni)": ["Tomato Sauce", "Mozzarella", "Pepperoni"],
    "Hotter than hell (Nduja)": ["Tomato Sauce", "Mozzarella", "Nduja"],
    "Cheesy x 4 (Quatro Formaggi)": ["Mozzarella", "Parmesan", "Blue Cheese", "Gorgonzola"],
    "No nothing (Vegan (none slayed))": ["Tomato Sauce", "Vegan Cheese", "Bell Pepper", "Zucchini", "Mushroom"],
    "All the good stuff (Hella meat)": ["Tomato Sauce", "Mozzarella", "Meat Mix", "Ham", "Bacon"],
}

DEFAULT_DRINKS = [
   Drink(name="Orange juice", price=39.99, icon="🍊", description="I see you're thirsty..."),
   Drink(name="Lemonade", price=59.99, icon="🍋", description="I see you're thirsty..."),
   Drink(name="Ice Tea", price=45.99, icon="🌱", description="I see you're thirsty..."),
   Drink(name="Coca Cola", price=49.99, icon="🥤", description="I see you're thirsty..."),
   Drink(name="Water", price=49.99, icon="💦", description="I see you're thirsty..."),
   Drink(name="Sparkling Water", price=49.99, icon="🫧", description="I see you're thirsty..."),
]


class Command(BaseCommand):
    help = "Seed the database with default pizzas and drinks"

    def handle(self, *args, **kwargs):
        print("Clearing old pizzas and drinks...")
        Topping.objects.all().delete()
        Pizza.objects.all().delete()
        Drink.objects.all().delete()
        
        print("Inserting toppings...")
        for topping in DEFAULT_TOPPINGS:
            topping.save()
            
        # topping_lookup = {t.name: t for t in Topping.objects.all()}
        topping_map = {}
        for topping in Topping.objects.all():
            topping_map[topping.name] = topping
        
        print("Inserting pizzas...")
        for pizza in DEFAULT_PIZZAS:
            pizza_to_add = Pizza.objects.create(
                name=pizza.name,
                description=pizza.description,
                icon=pizza.icon,
                base_price=pizza.base_price,
            )
            
            topping_names = PIZZA_TOPPING_MAP.get(pizza.name, [])
            for topping_name in topping_names:
                topping = topping_map.get(topping_name)
                if topping:
                    pizza_to_add.available_toppings.add(topping)
                    
            pizza_to_add.save()

        print("Inserting drinks...")
        for drink in DEFAULT_DRINKS:
            drink.save()

        print("Done!")
