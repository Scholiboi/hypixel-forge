import os
import sys
import json
from flask import Flask, request, jsonify, Blueprint
from models import Resource, db

sr_bp = Blueprint(name='sandbox_route', import_name=__name__, url_prefix='/api/sandbox')

def resource_path(relative_path):
    base_path = sys._MEIPASS
    return os.path.join(base_path, relative_path)

@sr_bp.route('/get-recipes-names', methods=["GET"])
def get_recipe_names():
    forging_path = resource_path('recipes/forging.json')
    gemstone_path = resource_path('recipes/gemstone_recipes.json')
    with open(forging_path) as f:
        forging = json.load(f)
    with open(gemstone_path) as f:
        gemstone_recipes = json.load(f)
    forging.update(gemstone_recipes)
    return jsonify(list(forging.keys())), 200

@sr_bp.route('/get-recipe/<name>/<int:amt>', methods=["GET"])
def get_recipe(name,amt):
    def expand_recipe(current_name, multiplier=1):
        if current_name not in forging:
            return {'name': current_name, 'amount': multiplier}
        else:
            ingredients = []
            for item, qty in forging[current_name].items():
                expanded = expand_recipe(item, qty * multiplier)
                ingredients.append(expanded)
            return {'name': current_name, 'amount': multiplier, 'ingredients': ingredients}

    forging_path = resource_path('recipes/forging.json')
    gemstone_path = resource_path('recipes/gemstone_recipes.json')
    with open(forging_path) as f:
        forging = json.load(f)
    with open(gemstone_path) as f:
        gemstone_recipes = json.load(f)
    forging.update(gemstone_recipes)

    if name not in forging:
        return jsonify({'error': 'Recipe not found'}), 404

    simple_recipe = forging[name]
    expanded_recipe = expand_recipe(name, amt)
    for key in simple_recipe:
        simple_recipe[key] = simple_recipe[key] * amt

    response = {
        'name': name,
        'simple_recipe': simple_recipe,
        'full_recipe': expanded_recipe
    }
    # print(response)
    return jsonify(response), 200

@sr_bp.route('/get-remaining-ingredients/<name>/<int:amt>', methods=["GET"])
def remaining_ingredients(name, amt):
    def build_recipe(current_item, multiplier=1):
        nonlocal my_resources
        for item, quantity in forging[current_item].items():
            if item in forging:
                composite_material(item, max(0,(quantity * multiplier)-my_resources[item])) # this composite material will check if this sub item already exists in our resources

        # this check is for checking if (main) item can be crafted from smaller resources
        # and will be called last
        check(current_item, multiplier)

    def check(current_item, multiplier=1):
        nonlocal my_resources, messages
        count = []
        for base_item, quantity_of_base_item in forging[current_item].items():
            possible_items = my_resources[base_item] // quantity_of_base_item
            count.append(multiplier - possible_items)
        # print(count)
        maxcount = max(count) if max(count) > 0 else 0
        # print(f"maxcount: {maxcount}\n multiplier: {multiplier}")
        my_resources[current_item] += (multiplier - maxcount)
        if multiplier - maxcount > 0:
            messages.append(f"You need to craft x{multiplier-maxcount} {current_item}")
        allocate(current_item, multiplier-maxcount)

    def allocate(current_item, a):
        nonlocal my_resources
        for base_item, quantity_of_base_item in forging[current_item].items():
            my_resources[base_item] -= quantity_of_base_item * a

    def composite_material(current_item, multiplier=1):
        #making bigger units from smaller units upto maximum utilization
        nonlocal my_resources
        for item, quantity in forging[current_item].items():
            if item in forging:
                # quantity -= my_resources[item]
                composite_material(item, max(0,(quantity * multiplier) - my_resources[item]))
            else:
                pass
        check(current_item, multiplier)

    def expand_required_recipe(current_name, multiplier=1):
        nonlocal my_resources
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
                        expanded = expand_required_recipe(item, (qty * multiplier) - my_resources[item])
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

    forging_path = resource_path('recipes/forging.json')
    gemstone_path = resource_path('recipes/gemstone_recipes.json')
    with open(forging_path) as f:
        forging = json.load(f)
    with open(gemstone_path) as f:
        gemstone_recipes = json.load(f)
    forging.update(gemstone_recipes)

    my_resources = {resource.name: resource.amount for resource in Resource.query.all()}
    messages = []
    old = my_resources[name]

    build_recipe(name, amt)
    new = my_resources[name]
    
    if new - old >= amt:
        expanded_recipe = expand_required_recipe(name, (new-old)-amt)
    else:
        expanded_recipe = expand_required_recipe(name, amt-(new-old))

    response = {
        'name': name,
        'full_recipe': expanded_recipe,
        'messages': messages
    }

    return jsonify(response), 200

@sr_bp.route('/craft', methods=["POST"])
def craft():
    # print(request)
    def craft_item(current_item, multiplier=1):
        nonlocal my_resources
        if current_item in forging:
            if my_resources[current_item] < multiplier:
                multiplier -= my_resources[current_item]
                my_resources[current_item] = 0
            else:
                my_resources[current_item] -= multiplier
                multiplier = 0
            for item, qty in forging[current_item].items():
                craft_item(item, qty*multiplier)
        else:
            my_resources[current_item] -= multiplier

    forging_path = resource_path('recipes/forging.json')
    gemstone_path = resource_path('recipes/gemstone_recipes.json')
    with open(forging_path) as f:
        forging = json.load(f)
    with open(gemstone_path) as f:
        gemstone_recipes = json.load(f)
    forging.update(gemstone_recipes)
    my_resources = {resource.name: resource.amount for resource in Resource.query.all()}

    data = request.json
    name = data['name']  
    amt = int(data['amount'])
    my_resources[name] += amt
    # print(my_resources)
    for item, qty in forging[name].items():
        craft_item(item, qty*amt)
    # print(my_resources)
    for resource in Resource.query.all():
        resource.amount = my_resources[resource.name]
    db.session.commit()

    return jsonify({'message': 'Crafted successfully'}), 201
