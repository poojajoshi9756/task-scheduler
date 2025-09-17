#!/usr/bin/env python3
"""
Development server runner for Windows
Use this instead of Gunicorn for local development
"""
from app import app

# Import models and routes to ensure they are loaded
import models
import routes

if __name__ == '__main__':
    # Run Flask development server
    app.run(host='0.0.0.0', port=5000, debug=True)