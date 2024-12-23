import json
from app import app, db
from models import Resource

# with open('my_resources.json') as f:
#     resources = json.load(f)
forging = ["Rough Amber Gemstone", "Rough Amethyst Gemstone", "Rough Aquamarine Gemstone", "Rough Citrine Gemstone", "Rough Jade Gemstone", "Rough Jasper Gemstone", "Rough Ruby Gemstone", "Rough Sapphire Gemstone", "Rough Topaz Gemstone"]
with app.app_context():
    # db.create_all()
    # i = 0
    # for resource_i in resources:
    #     db.session.add(Resource(id=i, name=resource_i, amount=resources[resource_i]))
    #     i += 1
    # db.session.commit()
    # print('Resources added to database')

    # for item in forging:
    #     db.session.add(Resource(name=item, amount=0))
    db.session.add(Resource(name='Enchanted Coal Block', amount=0))
    db.session.commit()