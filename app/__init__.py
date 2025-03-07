import os
from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG')

    # Register blueprints
    from app.routes.sensors import sensors_bp
    from app.routes.data import data_bp 
    from app.routes.root import root_bp
    from app.routes.users import users_bp

    app.register_blueprint(sensors_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(root_bp)


    return app
