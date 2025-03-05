import os
import sys
import threading
import time
import webbrowser
from flask import Flask, send_from_directory, abort, request, jsonify
from flask_cors import CORS
from models import db
from routes.resource_route import rr_bp
from routes.sandbox_route import sr_bp
from routes.inventoryresources_route import ir_bp

base_path = sys._MEIPASS

# this is for when frozen, the frontend build was bundled inside the executable
BUILD_DIR = os.path.join(base_path, 'frontend', 'build')
RECIPES_DIR = os.path.join(base_path, 'recipes')
INSTANCE_DIR = os.path.join(base_path, 'instance')


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

browser_opened = False

def start_server():
    global browser_opened
    time.sleep(1)
    if not browser_opened:
        print('browser opened')
        webbrowser.open("http://127.0.0.1:5000")
        browser_opened = True

if __name__ == '__main__':
    threading.Thread(target=start_server).start()
    app.run(debug=False, port=5000)