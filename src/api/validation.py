"""
Validation API endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List

router = APIRouter()

class ValidationRequest(BaseModel):
    data: Dict
    rules: List[str]
    regulator: str

class ValidationResponse(BaseModel):
    is_valid: bool
    errors: List[Dict]
    warnings: List[Dict]

@router.post("/validate", response_model=ValidationResponse)
async def validate_data(request: ValidationRequest):
    """Validate data against regulatory rules"""
    # Run validation
    errors = []
    warnings = []
    
    # Example validation
    if "revenue" not in request.data:
        errors.append({
            "field": "revenue",
            "message": "Revenue field is required",
            "rule": "SEC_10K_001"
        })
    
    return ValidationResponse(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )

validation_router = router
