from flask import Flask
from flask_cors import CORS
import os

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Enable CORS for local network access
    CORS(app, origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://0.0.0.0:8080",
        # Allow all local network IPs
        "http://192.168.*.*:8080",
        "http://10.*.*.*:8080",
        "http://172.16.*.*:8080",
        "http://172.17.*.*:8080",
        "http://172.18.*.*:8080",
        "http://172.19.*.*:8080",
        "http://172.20.*.*:8080",
        "http://172.21.*.*:8080",
        "http://172.22.*.*:8080",
        "http://172.23.*.*:8080",
        "http://172.24.*.*:8080",
        "http://172.25.*.*:8080",
        "http://172.26.*.*:8080",
        "http://172.27.*.*:8080",
        "http://172.28.*.*:8080",
        "http://172.29.*.*:8080",
        "http://172.30.*.*:8080",
        "http://172.31.*.*:8080"
    ])
    
    # Configure app
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['JSON_SORT_KEYS'] = False
    
    # Register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)
    
    return app 