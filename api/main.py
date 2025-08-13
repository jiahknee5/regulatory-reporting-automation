"""
Minimal API for Vercel deployment
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Regulatory Reporting Automation",
    description="AI-powered regulatory reporting system",
    version="1.0.0"
)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint - returns landing page"""
    return """
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
                <a href="/docs" class="button">📚 API Documentation</a>
                <a href="/health" class="button secondary">🔍 System Status</a>
                <a href="https://github.com/jiahknee5/regulatory-reporting-automation" class="button secondary">💻 GitHub</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "regulatory-reporting-automation",
        "version": "1.0.0"
    }

@app.get("/api")
async def api_info():
    """API information"""
    return {
        "message": "Regulatory Reporting Automation API",
        "endpoints": {
            "health": "/health",
            "docs": "/docs"
        }
    }