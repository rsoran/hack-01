import os
import sys

# Add the backend directory to sys.path so relative imports in app.py work
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app
