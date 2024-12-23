import json

name = 'Titanium Drill DR-X655'

with open('recipes/forging.json') as f:
    forging = json.load(f)
# with open('recipes/gemstone_recipes.json') as f:
#     gemstone_recipes = json.load(f)
# forging.update(gemstone_recipes)

my_resources = {
    "Refined Titanium": 0,
    "Refined Mithril": 0,
    "Refined Diamond": 10,
    "Glacite Jewel": 10,
    "Enchanted Gold Block": 10,
    "Enchanted Iron Block": 0,
    "Enchanted Redstone Block": 0,
    "Treasurite": 0,
    "Corleonite": 0,
    "Mithril Plate": 0,
    "Golden Plate": 1,
    "Fine Amber Gemstone": 0,
    "Fine Amethyst Gemstone": 0,
    "Fine Aquamarine Gemstone": 0,
    "Fine Citrine Gemstone": 0,
    "Fine Jade Gemstone": 0,
    "Fine Jasper Gemstone": 0,
    "Fine Ruby Gemstone": 0,
    "Fine Sapphire Gemstone": 0,
    "Fine Topaz Gemstone": 0,
    "Sludge Juice": 0,
    "Gemstone Mixture": 0,
    "Drill Motor": 0,
    "Titanium Drill DR-X655": 1
}


def build_recipe(current_item, multiplier=1):
    global my_resources
    for item, quantity in forging[current_item].items():
        if item in forging:
            quantity -= my_resources[item]
            composite_material(item, quantity * multiplier)


def check(current_item, multiplier=1):
    global my_resources
    count = []
    for base_item, quantity_of_base_item in forging[current_item].items():
        possible_items = my_resources[base_item] // quantity_of_base_item
        count.append(multiplier - possible_items)
    maxcount = max(count) if max(count) > 0 else 0
    my_resources[current_item] += (multiplier - maxcount)
    allocate(current_item, multiplier - maxcount)


def allocate(current_item, a):
    global my_resources
    for base_item, quantity_of_base_item in forging[current_item].items():
        my_resources[base_item] -= quantity_of_base_item * a


def composite_material(current_item, multiplier=1):
    global my_resources
    # making bigger units from smaller units upto maximum utilization
    for item, quantity in forging[current_item].items():
        if item in forging:
            composite_material(item, quantity * multiplier)
        else:
            pass
    check(current_item, multiplier)


def expand_required_recipe(current_name, multiplier=1):
    global my_resources
    if current_name not in forging:
        if my_resources[current_name] < multiplier:
            temp = my_resources[current_name]
            my_resources[current_name] = 0
            return {'name': current_name, 'amount': multiplier - temp}
        else:
            my_resources[current_name] -= multiplier
            return {'name': current_name, 'amount': 0}
    else:
        ingredients = []
        for item, qty in forging[current_name].items():
            if item in forging:
                if my_resources[item] < qty * multiplier:
                    expanded = expand_required_recipe(item, (qty * multiplier)- my_resources[item])
                    ingredients.append(expanded)
                    my_resources[item] = 0
                else:
                    my_resources[item] -= qty * multiplier
                    expanded = expand_required_recipe(item, 0)
                    ingredients.append(expanded)
            else:
                if my_resources[item] < qty * multiplier:
                    expanded = expand_required_recipe(item, (qty * multiplier))
                    ingredients.append(expanded)
                else:
                    my_resources[item] -= qty * multiplier
                    expanded = expand_required_recipe(item, 0)
                    ingredients.append(expanded)
        return {'name': current_name, 'amount': multiplier, 'ingredients': ingredients}


build_recipe(name)
expanded_recipe = expand_required_recipe(name)

response = {
    'name': name,
    'full_recipe': expanded_recipe
}

print(json.dumps(response, indent=4))