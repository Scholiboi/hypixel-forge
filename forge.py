from flask import Flask, request, jsonify, render_template, redirect, url_for
from forge_functions import * 
import json

options = ['View Base Items', 'removeResource', 'viewRequirements']
app = Flask(__name__)

with open('forging.json') as f:
    forging = json.load(f)

with open('my_resources.json') as f:
    my_resources = json.load(f)
    
forge_items = [element for element in forging]
temp_resources = {}

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html', my_resources=my_resources, options=options)

@app.route('/viewBaseItems', methods=['POST'])
def submitItem():
    forge_item = request.form.get('item')
    print(forge_item)
    temp_resources = viewItem(forge_item, temp_resources={})
    return render_template('viewbaseresource.html', 
                           my_resources=my_resources, 
                           temp_resources=temp_resources, 
                           options=options, 
                           list_of_forge_items=forge_items,
                           forge_item=""
                           )
    
@app.route('/submit', methods=['POST'])
def submit():
    selected_option = request.form.get('dropdown')
    
    # Process the selected option
    if selected_option == 'View Base Items':
        return redirect(url_for('viewBaseItems'))
        pass
    elif selected_option == 'removeResource':
        # Example processing for 'removeResource'
        pass
    elif selected_option == 'viewRequirements':
        # Example processing for 'viewRequirements'
        pass
    
    # Render the same template with updated data
    return redirect(url_for('home'))

@app.route('/viewBaseItems', methods=['POST', 'GET'])
def viewBaseItems():
    return render_template('viewbaseresource.html', 
                           my_resources=my_resources, 
                           temp_resources=temp_resources, 
                           options=options, 
                           list_of_forge_items=forge_items,
                           forge_item=""
                           )

if __name__ == '__main__':
    app.run(debug=True)