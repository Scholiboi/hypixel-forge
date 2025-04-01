from app import app, db
from models import Resource

with app.app_context():
    for resource in Resource.query.all():
       resource.amount = 0
    db.session.commit()
