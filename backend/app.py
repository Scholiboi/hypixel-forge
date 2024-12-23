from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Resource
from routes.resource_route import rr_bp
from routes.sandbox_route import sr_bp

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(rr_bp)
app.register_blueprint(sr_bp)

if __name__ == '__main__':
    app.run(debug=True)
