from flask import Flask, request, jsonify, Blueprint
# ignore the error message, it's a false positive
from models import Resource, db
rr_bp = Blueprint(name='resource_route', import_name=__name__)

@rr_bp.route('/resources', methods=['GET'])
def get_resource():
    my_resources = Resource.query.all()
    # print(my_resources)
    return jsonify([{'name': resource.name, 'amount': resource.amount} for resource in my_resources]), 200

@rr_bp.route('/resources/<name>', methods=['GET'])
def get_resource_by_name(name):
    resource = Resource.query.filter_by(name=name).first()
    # print(resource.name)
    if resource:
        return jsonify({'name': resource.name, 'amount': resource.amount}), 200
    return jsonify({'error': 'Resource not found'}), 404

@rr_bp.route('/modify-resources', methods=['POST'])
def modify_resource():
    data = request.json
    data = data['searchedResources'] # type: ignore
    # print(data)
    for resource_data in data:
        resource = Resource.query.filter_by(name=resource_data['name']).first()
        # print(resource)
        if resource:
            resource.amount = resource_data['amount']
            db.session.commit()
        else:
            return jsonify({'error': 'Resource not found'}), 404
    return jsonify({'message': 'Resource saved successfully'}), 201