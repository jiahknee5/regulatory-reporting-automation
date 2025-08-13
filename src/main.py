"""
Regulatory Reporting Automation System
Main application entry point
"""

import os
import asyncio
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

# Handle imports for Vercel deployment
try:
    from src.api.submission import submission_router
    from src.api.validation import validation_router
    from src.core.rule_interpreter import RuleInterpreter
    from src.core.data_validator import DataValidator
    from src.core.report_builder import ReportBuilder
except ImportError:
    # For Vercel, adjust import paths
    from api.submission import submission_router
    from api.validation import validation_router
    from core.rule_interpreter import RuleInterpreter
    from core.data_validator import DataValidator
    from core.report_builder import ReportBuilder

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Regulatory Reporting Automation",
    description="AI-powered regulatory reporting system",
    version="1.0.0",
    docs_url="/regreporting/docs",
    redoc_url="/regreporting/redoc",
    openapi_url="/regreporting/openapi.json",
    root_path="/regreporting" if os.getenv("VERCEL") else ""
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(submission_router, prefix="/api/v1/submission", tags=["submission"])
app.include_router(validation_router, prefix="/api/v1/validation", tags=["validation"])

@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    logger.info("Starting Regulatory Reporting Automation System")
    # Initialize components
    # Load rules, connect to databases, etc.

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Regulatory Reporting Automation System")
    # Close connections, save state, etc.

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint - returns landing page"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Regulatory Reporting Automation</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                max-width: 600px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            h1 {
                color: #1e3c72;
                margin-bottom: 20px;
            }
            p {
                color: #666;
                line-height: 1.6;
                margin-bottom: 30px;
            }
            .buttons {
                display: flex;
                gap: 15px;
                justify-content: center;
                flex-wrap: wrap;
            }
            .button {
                display: inline-block;
                padding: 12px 24px;
                background: #1e3c72;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                transition: all 0.3s ease;
            }
            .button:hover {
                background: #2a5298;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            }
            .button.secondary {
                background: #6c757d;
            }
            .button.secondary:hover {
                background: #5a6268;
            }
            .status {
                display: inline-block;
                padding: 5px 15px;
                background: #28a745;
                color: white;
                border-radius: 20px;
                font-size: 0.9em;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <span class="status">OPERATIONAL</span>
            <h1>🏛️ Regulatory Reporting Automation</h1>
            <p>
                AI-powered compliance reporting system that automates the preparation and 
                submission of regulatory reports. Our intelligent system interprets complex 
                rules, validates data, and generates compliant reports across multiple jurisdictions.
            </p>
            <div class="buttons">
                <a href="/regreporting/docs" class="button">📚 API Documentation</a>
                <a href="/regreporting/health" class="button secondary">🔍 System Status</a>
                <a href="https://github.com/johnnycchung/regulatory-reporting-automation" class="button secondary">💻 GitHub</a>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "message": "Regulatory Reporting Automation System",
        "status": "operational",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/regreporting/docs",
            "health": "/regreporting/health",
            "submission": "/regreporting/api/v1/submission",
            "validation": "/regreporting/api/v1/validation"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "api": "operational",
            "rule_engine": "operational",
            "ml_models": "operational"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
