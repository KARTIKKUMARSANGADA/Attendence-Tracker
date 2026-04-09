import os
import sys

# Add the backend directory to sys.path so we can import our modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
backend_dir = os.path.join(parent_dir, "backend")
sys.path.append(backend_dir)

# Import the FastAPI app from main.py
from main import app as handler

# This is the entry point Vercel looks for
app = handler
