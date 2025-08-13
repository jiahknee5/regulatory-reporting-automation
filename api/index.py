"""
Vercel API handler for Regulatory Reporting Automation
"""
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import the FastAPI app
from main import app

# Export the handler for Vercel
handler = app