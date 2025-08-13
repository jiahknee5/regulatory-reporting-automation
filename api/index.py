"""
Vercel API handler for Regulatory Reporting Automation
"""
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the FastAPI app
from src.main import app

# Create the handler for Vercel
handler = app