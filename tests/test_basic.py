"""
Basic tests for regulatory reporting system
"""

import pytest
from datetime import datetime

def test_project_structure():
    """Test project structure is correct"""
    import os
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent
    
    # Check required directories
    assert (project_root / "src").exists()
    assert (project_root / "tests").exists()
    assert (project_root / "docs").exists()
    assert (project_root / "3_deliverables").exists()
    
def test_imports():
    """Test all modules can be imported"""
    try:
        from src.main import app
        from src.api.submission import submission_router
        from src.api.validation import validation_router
        from src.core.rule_interpreter import RuleInterpreter
        from src.core.data_validator import DataValidator
        from src.core.report_builder import ReportBuilder
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")
        
def test_api_health():
    """Test API health endpoint"""
    from fastapi.testclient import TestClient
    from src.main import app
    
    client = TestClient(app)
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
