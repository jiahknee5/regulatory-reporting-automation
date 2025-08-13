"""
Tests for data validation
"""

import pytest
import pandas as pd

def test_anomaly_detection():
    """Test anomaly detection model"""
    from operating_system.projects.regulatory_reporting_automation.deliverables.ml_models import anomaly_detector
    
    # Create test data
    normal_data = pd.DataFrame({
        'revenue': [1000, 1100, 1050, 1080, 1020],
        'expenses': [800, 850, 820, 840, 810]
    })
    
    # Train model
    anomaly_detector.train(normal_data)
    
    # Test anomaly detection
    test_data = pd.DataFrame({
        'revenue': [1050, 5000],  # Second value is anomaly
        'expenses': [830, 900]
    })
    
    result = anomaly_detector.detect(test_data)
    
    assert 'is_anomaly' in result.columns
    assert result['is_anomaly'].iloc[1] == True  # Second row should be anomaly
    
def test_data_validation():
    """Test data validation"""
    from src.core.data_validator import DataValidator
    
    validator = DataValidator()
    
    # Test data with missing values
    data = pd.DataFrame({
        'revenue': [1000, None, 1200],
        'expenses': [800, 900, 1000]
    })
    
    result = validator.validate(data, [])
    
    assert len(result["warnings"]) > 0
    assert any(w["type"] == "missing_data" for w in result["warnings"])
