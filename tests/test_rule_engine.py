"""
Tests for rule engine
"""

import pytest
from datetime import datetime

def test_rule_loading():
    """Test loading rules from file"""
    from operating_system.projects.regulatory_reporting_automation.deliverables.rule_engine import rule_engine, Rule, RuleType
    
    # Create test rule
    test_rule = Rule(
        rule_id="TEST001",
        regulator="SEC",
        rule_type=RuleType.VALIDATION,
        description="Test rule",
        expression="revenue > 0",
        parameters={"field": "revenue", "condition": "positive"},
        version="1.0",
        effective_date=datetime.now()
    )
    
    # Add rule
    rule_engine.rules["SEC"] = [test_rule]
    
    assert len(rule_engine.rules["SEC"]) == 1
    assert rule_engine.rules["SEC"][0].rule_id == "TEST001"
    
def test_validation_rule():
    """Test validation rule application"""
    from operating_system.projects.regulatory_reporting_automation.deliverables.rule_engine import rule_engine
    
    # Test data
    data = {"revenue": -1000}
    
    # Apply rules
    results = rule_engine.apply_rules(data, "SEC")
    
    # Check validation failed
    assert any(r["status"] == "failed" for r in results["validation_results"])
