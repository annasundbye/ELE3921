from django.core.management.base import BaseCommand
from application.models import Pizza, Drink, Topping, Size

DEFAULT_TOPPINGS = [
    Topping(name="Tomato Sauce", icon="🍅", base_price=9.00),
    Topping(name="Mozzarella", icon="🧀", base_price=15.00),
    Topping(name="Pepperoni", icon="🌶️", base_price=25.00),
    Topping(name="Nduja", icon="🔥", base_price=35.00),
    Topping(name="Parmesan", icon="🧂", base_price=20.00),
    Topping(name="Blue Cheese", icon="🔵", base_price=30.00),
    Topping(name="Gorgonzola", icon="💙", base_price=35.00),
    Topping(name="Vegan Cheese", icon="🌱", base_price=9.00),
    Topping(name="Bell Pepper", icon="🫑", base_price=9.00),
    Topping(name="Zucchini", icon="🥒", base_price=15.00),
    Topping(name="Mushroom", icon="🍄", base_price=9.00),
    Topping(name="Meat Mix", icon="🥩", base_price=40.00),
    Topping(name="Ham", icon="🐖", base_price=30.00),
    Topping(name="Bacon", icon="🥓", base_price=30.00),
]

DEFAULT_PIZZAS = [
    Pizza(name="Basic AF (Margherita)", base_price=159, icon="🍅", description="Safe choice. Boring tho."),
    Pizza(name="You can't take this (Pepperoni)", base_price=209, icon="🍕", description="Loaded with pepperoni for when you're feeling extra. No cap."),
    Pizza(name="Hotter than hell (Nduja)", base_price=219, icon="🌶️", description="Bro. Bro. Bro! This is hot."),
    Pizza(name="Cheesy x 4 (Quatro Formaggi)", base_price=239, icon="🧀", description="Just cheese. No explanation needed. It's giving simplicity."),
    Pizza(name="No nothing (Vegan (none slayed))", base_price=129, icon="🥦", description="No animals were harmed making this pizza. It's the responsible choice."),
    Pizza(name="All the good stuff (Hella meat)", base_price=249, icon="🥩", description="Hella meat."),
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

DEFAULT_SIZES = [
    Size(name="small", description='10" - perfect for one', multiplier=1.0),
    Size(name="medium", description='12" - sharing is caring', multiplier=1.1),
    Size(name="large", description='14" - feed the squad', multiplier=1.2),
    Size(name="x-large", description='16" - absolute unit', multiplier=1.3),
]


class Command(BaseCommand):
    help = "Seed the database with default pizzas and drinks"

    def handle(self, *args, **kwargs):
        print("Clearing old pizzas and drinks...")
        Topping.objects.all().delete()
        Pizza.objects.all().delete()
        Drink.objects.all().delete()
        Size.objects.all().delete()
        
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

        print("Inserting sizes...")
        for size in DEFAULT_SIZES:
            size.save()

        print("Done!")
