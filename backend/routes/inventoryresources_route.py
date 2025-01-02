from flask import Flask, request, jsonify, Blueprint
from models import Resource, db

ir_bp = Blueprint(name='inventoryresources_route', import_name=__name__, url_prefix='/mod')

@ir_bp.route('/modify-resources', methods=['POST'])
def modify_resource():
    data = request.json 
    for item in data: #type: ignore
        if item == '':
            continue
        resource = Resource.query.filter_by(name=item).first()
        if resource:
            resource.amount += data[item] #type: ignore
        else:
            item_split = item.split()
            if len(item_split) == 1:
                continue
            item_refined = ' '.join(item_split[1:])
            resource = Resource.query.filter_by(name=item_refined).first()
            if resource:
                resource.amount += data[item] #type: ignore
            
    db.session.commit()
    return jsonify({'message': 'Resource updated successfully'}), 200

@ir_bp.route('/reset', methods=['POST'])
def reset_resources():
    for resource in Resource.query.all():
        resource.amount = 0
    db.session.commit()
    return jsonify({'message': 'Resources reset successfully'}), 200
