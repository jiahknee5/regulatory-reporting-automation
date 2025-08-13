"""
Tests for report generation
"""

import pytest
from datetime import datetime

def test_pdf_generation():
    """Test PDF report generation"""
    from operating_system.projects.regulatory_reporting_automation.deliverables.report_generator import report_generator, ReportFormat
    
    # Test data
    data = {
        "financial_summary": {
            "revenue": 1000000,
            "expenses": 800000,
            "net_income": 200000
        }
    }
    
    metadata = {
        "period": "Q1 2024",
        "entity": "Test Corp"
    }
    
    # Generate PDF
    pdf_data = report_generator.generate_report(
        "10-Q",
        data,
        ReportFormat.PDF,
        metadata
    )
    
    assert isinstance(pdf_data, bytes)
    assert len(pdf_data) > 0
    
def test_xml_generation():
    """Test XML report generation"""
    from operating_system.projects.regulatory_reporting_automation.deliverables.report_generator import report_generator, ReportFormat
    
    # Test data
    data = {
        "revenue": 1000000,
        "expenses": 800000
    }
    
    # Generate XML
    xml_data = report_generator.generate_report(
        "GABRIEL",
        data,
        ReportFormat.XML
    )
    
    assert isinstance(xml_data, bytes)
    assert b"<Report" in xml_data
    assert b"<revenue>1000000</revenue>" in xml_data
