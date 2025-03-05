import os
import sys
from flask import Flask, send_from_directory, abort
from flask_cors import CORS
from models import db
from routes.resource_route import rr_bp
from routes.sandbox_route import sr_bp
from routes.inventoryresources_route import ir_bp

if getattr(sys, '_MEIPASS', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(os.path.dirname(__file__))

if getattr(sys, '_MEIPASS', False):
    # this is for when frozen, the frontend build was bundled inside the executable
    BUILD_DIR = os.path.join(base_path, 'frontend', 'build')
    RECIPES_DIR = os.path.join(base_path, 'recipes')
    INSTANCE_DIR = os.path.join(base_path, 'instance')
else:
    # otherwise during dev, use relative paths 
    BUILD_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build')
    RECIPES_DIR = os.path.join(os.path.dirname(__file__), 'recipes')
    INSTANCE_DIR = os.path.join(os.path.dirname(__file__), 'instance')

app = Flask(__name__, static_folder=BUILD_DIR)
CORS(app)

db_path = os.path.join(INSTANCE_DIR, 'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(rr_bp)
app.register_blueprint(ir_bp)
app.register_blueprint(sr_bp)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    print("Requested path:", path)
    if path.startswith('api'):
        abort(404)
    try:
        return send_from_directory(app.static_folder, path)
    except Exception as e:
        # print("Error serving file:", e)
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)