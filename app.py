import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Try to import DeclarativeBase for newer SQLAlchemy versions
try:
    from sqlalchemy.orm import DeclarativeBase
    class Base(DeclarativeBase):
        pass
    db = SQLAlchemy(model_class=Base)
except ImportError:
    # Fallback for older SQLAlchemy versions
    db = SQLAlchemy()

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
database_url = os.environ.get("DATABASE_URL", "sqlite:///tasks.db")
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

def create_app():
    """Application factory function"""
    # Import models and routes after app initialization
    import models
    import routes
    
    with app.app_context():
        # Create all tables
        db.create_all()
    
    return app

# Create the application
create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
