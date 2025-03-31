from app import app, db
from models import Resource

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

with app.app_context():
    for resource in Resource.query.all():
       resource.amount = 0
    db.session.commit()
