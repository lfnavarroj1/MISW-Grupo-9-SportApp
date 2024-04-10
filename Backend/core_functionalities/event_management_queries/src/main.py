from flask import Flask
from .extensions import db
from .api.event import event_blueprint
import os
from src.config import DevelopmentConfig

# Configuration
DATABASE_URI = os.environ.get("DATABASE_URL")

def create_app(config_object=None):
    app = Flask(__name__)
    
    if config_object:
        app.config.from_object(config_object)
    else:
        # Default to DevelopmentConfig if nothing is specified
        app.config.from_object(DevelopmentConfig) 
    # Database configuration
    #app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    # Initialize app with SQLAlchemy

    db.init_app(app)

    # Register blueprints
    app.register_blueprint(event_blueprint)

    # Function to register CLI commands
    def register_cli_commands(app):
        @app.cli.command("init-db")
        def init_db():
            """Create database tables."""
            db.create_all()
            print("Database tables created.")
    
    register_cli_commands(app)

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()  # Create database tables for our data models
    app.run(host="0.0.0.0", port=3002)