from flask import Flask
from flask_cors import CORS
import os

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Enable CORS for development
    CORS(app)
    
    # Configure app
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['JSON_SORT_KEYS'] = False
    
    # Register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app 