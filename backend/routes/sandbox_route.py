from flask import Flask, request, jsonify, Blueprint
from models import Resource, db
import json

sr_bp = Blueprint(name='sandbox_route', import_name=__name__, url_prefix='/sandbox')

# @sr_bp.route('/get-recipes', methods=["GET"])
# def get_recipes():
#     with open('recipes/forging.json') as f:
#         forging = json.load(f)
#     with open('recipes/gemstone_recipes.json') as f:
#         gemstone_recipes = json.load(f)
#     forging.update(gemstone_recipes)
#     return jsonify(forging), 200

@sr_bp.route('/get-recipes-names', methods=["GET"])
def get_recipe_names():
    with open('recipes/forging.json') as f:
        forging = json.load(f)
    with open('recipes/gemstone_recipes.json') as f:
        gemstone_recipes = json.load(f)
    forging.update(gemstone_recipes)
    return jsonify(list(forging.keys())), 200

@sr_bp.route('/get-recipe/<name>', methods=["GET"])
def get_recipe(name):
    with open('recipes/forging.json') as f:
        forging = json.load(f)
    with open('recipes/gemstone_recipes.json') as f:
        gemstone_recipes = json.load(f)
    forging.update(gemstone_recipes)
    if name not in forging:
        return jsonify({'error': 'Recipe not found'}), 404

    simple_recipe = forging[name]

    def expand_recipe(current_name, multiplier=1):
        if current_name not in forging:
            return {'name': current_name, 'amount': multiplier}
        else:
            ingredients = []
            for item, qty in forging[current_name].items():
                expanded = expand_recipe(item, qty * multiplier)
                ingredients.append(expanded)
            return {'name': current_name, 'amount': multiplier, 'ingredients': ingredients}

    expanded_recipe = expand_recipe(name)

    response = {
        'name': name,
        'simple_recipe': simple_recipe,
        'full_recipe': expanded_recipe
    }
    # print(response)
    return jsonify(response), 200

@sr_bp.route('/get-remaining-ingredients/<name>', methods=["GET"])
def remaining_ingredients(name):
    with open('recipes/forging.json') as f:
        forging = json.load(f)
    with open('recipes/gemstone_recipes.json') as f:
        gemstone_recipes = json.load(f)
    forging.update(gemstone_recipes)

    my_resources = {resource.name: resource.amount for resource in Resource.query.all()}
    messages = []

    def build_recipe(current_item, multiplier=1):
        nonlocal my_resources
        for item, quantity in forging[current_item].items():
            if item in forging:
                quantity -= my_resources[item]
                composite_material(item, my_resources, quantity * multiplier)


    def check(current_item, multiplier=1):
        nonlocal my_resources, messages
        count = []
        for base_item, quantity_of_base_item in forging[current_item].items():
            possible_items = my_resources[base_item] // quantity_of_base_item
            count.append(multiplier - possible_items)
        print(count)
        maxcount = max(count) if max(count) > 0 else 0
        print(f"maxcount: {maxcount}\n multiplier: {multiplier}")
        my_resources[current_item] += (multiplier - maxcount)
        if multiplier - maxcount > 0:
            messages.append(f"You need to craft x{multiplier-maxcount} {current_item}")
        allocate(current_item, multiplier-maxcount)

    def allocate(current_item, a):
        nonlocal my_resources
        for base_item, quantity_of_base_item in forging[current_item].items():
            my_resources[base_item] -= quantity_of_base_item * a

    def composite_material(current_item, my_resources, multiplier=1):
        #making bigger units from smaller units upto maximum utilization
        for item, quantity in forging[current_item].items():
            if item in forging:
                composite_material(item, my_resources, quantity * multiplier)
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

    build_recipe(name)
    expanded_recipe = expand_required_recipe(name)

    response = {
        'name': name,
        'full_recipe': expanded_recipe,
        'messages': messages
    }

    return jsonify(response), 200