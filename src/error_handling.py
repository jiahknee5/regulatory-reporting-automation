"""
Error Handling Module
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

class RegulatoryReportingError(Exception):
    """Base exception for regulatory reporting"""
    pass

class ValidationError(RegulatoryReportingError):
    """Data validation error"""
    pass

class SubmissionError(RegulatoryReportingError):
    """Report submission error"""
    pass

class RuleEngineError(RegulatoryReportingError):
    """Rule engine error"""
    pass

def handle_error(error: Exception) -> Dict[str, Any]:
    """Handle and log errors"""
    logger.error(f"Error occurred: {str(error)}", exc_info=True)
    
    if isinstance(error, ValidationError):
        return {
            "error_type": "validation",
            "message": str(error),
            "code": "VAL001"
        }
    elif isinstance(error, SubmissionError):
        return {
            "error_type": "submission",
            "message": str(error),
            "code": "SUB001"
        }
    else:
        return {
            "error_type": "system",
            "message": "An unexpected error occurred",
            "code": "SYS001"
        }
