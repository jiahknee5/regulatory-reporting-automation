"""
Regulatory Rule Engine
Interprets and applies regulatory rules to data
"""

from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import json
import re
from dataclasses import dataclass
from enum import Enum

class RuleType(Enum):
    VALIDATION = "validation"
    CALCULATION = "calculation"
    TRANSFORMATION = "transformation"
    CONDITIONAL = "conditional"

@dataclass
class Rule:
    """Individual regulatory rule"""
    rule_id: str
    regulator: str
    rule_type: RuleType
    description: str
    expression: str
    parameters: Dict[str, Any]
    version: str
    effective_date: datetime
    
class RuleEngine:
    """Main rule engine for regulatory compliance"""
    
    def __init__(self):
        self.rules: Dict[str, List[Rule]] = {}
        self.rule_functions: Dict[str, Callable] = {}
        self._register_standard_functions()
        
    def load_rules(self, rules_file: str):
        """Load rules from configuration file"""
        with open(rules_file, 'r') as f:
            rules_data = json.load(f)
            
        for rule_data in rules_data:
            rule = Rule(
                rule_id=rule_data['rule_id'],
                regulator=rule_data['regulator'],
                rule_type=RuleType(rule_data['rule_type']),
                description=rule_data['description'],
                expression=rule_data['expression'],
                parameters=rule_data.get('parameters', {}),
                version=rule_data['version'],
                effective_date=datetime.fromisoformat(rule_data['effective_date'])
            )
            
            if rule.regulator not in self.rules:
                self.rules[rule.regulator] = []
            self.rules[rule.regulator].append(rule)
            
    def apply_rules(self, data: Dict[str, Any], regulator: str) -> Dict[str, Any]:
        """Apply all rules for a specific regulator"""
        if regulator not in self.rules:
            raise ValueError(f"No rules found for regulator: {regulator}")
            
        results = {
            "data": data.copy(),
            "validation_results": [],
            "calculations": {},
            "transformations": {},
            "rule_applications": []
        }
        
        for rule in self.rules[regulator]:
            if rule.effective_date <= datetime.now():
                result = self._apply_single_rule(rule, results["data"])
                results["rule_applications"].append({
                    "rule_id": rule.rule_id,
                    "status": result["status"],
                    "message": result.get("message"),
                    "output": result.get("output")
                })
                
                # Update data based on rule type
                if rule.rule_type == RuleType.TRANSFORMATION:
                    results["data"] = result.get("transformed_data", results["data"])
                elif rule.rule_type == RuleType.CALCULATION:
                    results["calculations"][rule.rule_id] = result.get("output")
                elif rule.rule_type == RuleType.VALIDATION:
                    results["validation_results"].append(result)
                    
        return results
        
    def _apply_single_rule(self, rule: Rule, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply a single rule to data"""
        try:
            if rule.rule_type == RuleType.VALIDATION:
                return self._apply_validation_rule(rule, data)
            elif rule.rule_type == RuleType.CALCULATION:
                return self._apply_calculation_rule(rule, data)
            elif rule.rule_type == RuleType.TRANSFORMATION:
                return self._apply_transformation_rule(rule, data)
            elif rule.rule_type == RuleType.CONDITIONAL:
                return self._apply_conditional_rule(rule, data)
        except Exception as e:
            return {
                "status": "error",
                "message": f"Rule application failed: {str(e)}",
                "rule_id": rule.rule_id
            }
            
    def _apply_validation_rule(self, rule: Rule, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply validation rule"""
        # Parse expression (simplified - use proper parser in production)
        # Example: "revenue > 0 AND revenue < 1000000000"
        
        # For demo, implement simple validation
        if "field" in rule.parameters and "condition" in rule.parameters:
            field_value = data.get(rule.parameters["field"])
            condition = rule.parameters["condition"]
            
            if condition == "required" and field_value is None:
                return {
                    "status": "failed",
                    "message": f"{rule.parameters['field']} is required",
                    "rule_id": rule.rule_id
                }
            elif condition == "positive" and field_value is not None and field_value < 0:
                return {
                    "status": "failed", 
                    "message": f"{rule.parameters['field']} must be positive",
                    "rule_id": rule.rule_id
                }
                
        return {
            "status": "passed",
            "rule_id": rule.rule_id
        }
        
    def _apply_calculation_rule(self, rule: Rule, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply calculation rule"""
        # Example: Calculate ratio or derived metric
        if rule.expression in self.rule_functions:
            output = self.rule_functions[rule.expression](data, rule.parameters)
            return {
                "status": "success",
                "output": output,
                "rule_id": rule.rule_id
            }
            
        return {
            "status": "error",
            "message": f"Unknown calculation: {rule.expression}",
            "rule_id": rule.rule_id
        }
        
    def _apply_transformation_rule(self, rule: Rule, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply transformation rule"""
        transformed_data = data.copy()
        
        # Example transformations
        if rule.expression == "standardize_currency":
            # Convert all amounts to USD
            for field in rule.parameters.get("fields", []):
                if field in transformed_data:
                    # Simplified - add real conversion logic
                    transformed_data[field] = transformed_data[field] * rule.parameters.get("rate", 1.0)
                    
        return {
            "status": "success",
            "transformed_data": transformed_data,
            "rule_id": rule.rule_id
        }
        
    def _apply_conditional_rule(self, rule: Rule, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply conditional rule"""
        # Implement conditional logic based on rule expression
        return {
            "status": "success",
            "rule_id": rule.rule_id
        }
        
    def _register_standard_functions(self):
        """Register standard calculation functions"""
        
        def debt_to_equity_ratio(data: Dict, params: Dict) -> float:
            debt = data.get("total_debt", 0)
            equity = data.get("total_equity", 1)
            return debt / equity if equity != 0 else 0
            
        def working_capital(data: Dict, params: Dict) -> float:
            current_assets = data.get("current_assets", 0)
            current_liabilities = data.get("current_liabilities", 0)
            return current_assets - current_liabilities
            
        self.rule_functions["debt_to_equity_ratio"] = debt_to_equity_ratio
        self.rule_functions["working_capital"] = working_capital
        
    def validate_rule_consistency(self) -> List[Dict]:
        """Check for rule conflicts or inconsistencies"""
        issues = []
        
        for regulator, regulator_rules in self.rules.items():
            # Check for duplicate rule IDs
            rule_ids = [r.rule_id for r in regulator_rules]
            if len(rule_ids) != len(set(rule_ids)):
                issues.append({
                    "type": "duplicate_rule_id",
                    "regulator": regulator,
                    "message": "Duplicate rule IDs found"
                })
                
        return issues

# Export rule engine instance
rule_engine = RuleEngine()
