import json
from app import app, db
from models import Resource

gemstones = [
    "Amber", "Amethyst", "Aquamarine", "Citrine", "Jade", 
    "Jasper", "Onyx", "Opal", "Peridot", "Ruby", "Sapphire", "Topaz"
]

tiers = ["Rough", "Flawed", "Fine", "Flawless", "Perfect"]

precursor_apparatus = {
        "Control Switch": 1,
        "Electron Transmitter": 1,
        "FTX 3070": 1,
        "Robotron Reflector": 1,
        "Superlite Motor": 1,
        "Synthetic Heart": 1
    }

Drill_Engines = {
    "Mithril-Plated Drill Engine": 1,
    "Titanium-Plated Drill Engine": 1,
    "Ruby-Polished Drill Engine": 1,
    "Sapphire-Polished Drill Engine": 1,
    "Amber-Polished Drill Engine": 1,
}


#
# with app.app_context():
#     while True:
#     # for gemstone in gemstones:
#     #     for tier in tiers:
#     #         name = f"{tier} {gemstone} Gemstone"
#     #         db.session.add(Resource(name=name, amount=0))
#     # for key in precursor_apparatus:
#     #     db.session.add(Resource(name=key, amount=0))
#     # db.session.add(Resource(name="Precursor Apparatus", amount=0))
#     # db.session.add(Resource(name="Volta", amount=0))
#         customname = input()
#         # for key in Drill_Engines:
#         #     db.session.add(Resource(name=key, amount=0))
#         try:
#             db.session.add(Resource(name=customname, amount=0))
#         except:
#             print(f'"{customname}" already exists in database')
#         else:
#             db.session.commit()
#             print(f'"{customname}" added to database')

resources = {}

with app.app_context():
    for resource in Resource.query.all():
        resources[resource.name] = resource.amount

print(json.dumps(resources, indent=4))