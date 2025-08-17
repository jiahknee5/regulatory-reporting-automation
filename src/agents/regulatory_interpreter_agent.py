"""
Regulatory Interpreter Agent (Cognitive Order 5)
Interprets complex regulatory texts using NLP and maintains contextual understanding
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import re

# For production, these would be actual imports from Project Chimera
# from operating_system.core.agents.cognitive_base import CognitiveAgent

logger = logging.getLogger(__name__)

class InterpretationType(Enum):
    """Types of regulatory interpretations"""
    REQUIREMENT = "requirement"
    PROHIBITION = "prohibition"
    EXEMPTION = "exemption"
    CALCULATION = "calculation"
    DEFINITION = "definition"
    PROCESS = "process"

@dataclass
class RegulatoryInterpretation:
    """Structured interpretation of regulatory text"""
    regulation_id: str
    section: str
    interpretation_type: InterpretationType
    original_text: str
    interpreted_meaning: str
    data_requirements: List[str]
    calculation_formula: Optional[str]
    conditions: List[str]
    effective_date: datetime
    confidence_score: float
    metadata: Dict[str, Any]

class RegulatoryInterpreterAgent:
    """
    Cognitive Order 5 Agent for interpreting complex regulatory requirements
    Uses NLP to parse regulatory texts and extract actionable requirements
    """
    
    def __init__(self):
        self.cognitive_order = 5
        self.name = "Regulatory Interpreter Agent"
        self.interpretations_cache = {}
        self.regulatory_patterns = self._load_regulatory_patterns()
        self.domain_knowledge = self._load_domain_knowledge()
        
    def _load_regulatory_patterns(self) -> Dict[str, List[str]]:
        """Load common regulatory language patterns"""
        return {
            "requirements": [
                r"shall\s+(?P<action>\w+)",
                r"must\s+(?P<action>\w+)",
                r"required\s+to\s+(?P<action>\w+)",
                r"obligated\s+to\s+(?P<action>\w+)"
            ],
            "prohibitions": [
                r"shall\s+not\s+(?P<action>\w+)",
                r"must\s+not\s+(?P<action>\w+)",
                r"prohibited\s+from\s+(?P<action>\w+)",
                r"may\s+not\s+(?P<action>\w+)"
            ],
            "exemptions": [
                r"except\s+(?P<condition>.+)",
                r"unless\s+(?P<condition>.+)",
                r"exempted\s+if\s+(?P<condition>.+)",
                r"not\s+applicable\s+to\s+(?P<entity>.+)"
            ],
            "calculations": [
                r"calculated\s+as\s+(?P<formula>.+)",
                r"determined\s+by\s+(?P<method>.+)",
                r"equals?\s+(?P<formula>.+)",
                r"(?P<metric>\w+)\s*=\s*(?P<formula>.+)"
            ],
            "data_fields": [
                r"report\s+(?P<field>\w+)",
                r"disclose\s+(?P<field>\w+)",
                r"provide\s+(?P<field>\w+)",
                r"submit\s+(?P<field>\w+)"
            ],
            "deadlines": [
                r"within\s+(?P<days>\d+)\s+days",
                r"by\s+(?P<date>[\w\s,]+)",
                r"no\s+later\s+than\s+(?P<date>[\w\s,]+)",
                r"(?P<frequency>monthly|quarterly|annually)"
            ]
        }
        
    def _load_domain_knowledge(self) -> Dict[str, Any]:
        """Load domain-specific regulatory knowledge"""
        return {
            "sec": {
                "forms": ["10-K", "10-Q", "8-K", "DEF 14A"],
                "concepts": ["material", "non-GAAP", "beneficial ownership"],
                "calculations": {
                    "eps": "net_income / weighted_average_shares",
                    "current_ratio": "current_assets / current_liabilities"
                }
            },
            "fca": {
                "forms": ["GABRIEL", "REP-CRIM", "FSA001"],
                "concepts": ["conduct risk", "operational resilience"],
                "thresholds": {
                    "large_firm": {"assets": 15000000000}
                }
            },
            "esma": {
                "forms": ["EMIR", "MiFID II", "AIFMD"],
                "concepts": ["systematic internaliser", "dark pool"],
                "calculations": {
                    "leverage": "exposure / nav"
                }
            }
        }
        
    async def interpret_regulation(self, 
                                 regulation_text: str,
                                 regulator: str,
                                 context: Optional[Dict[str, Any]] = None) -> RegulatoryInterpretation:
        """
        Main method to interpret regulatory text
        
        Args:
            regulation_text: The raw regulatory text to interpret
            regulator: The regulatory body (SEC, FCA, ESMA, etc.)
            context: Additional context for interpretation
            
        Returns:
            Structured interpretation of the regulation
        """
        logger.info(f"Interpreting regulation for {regulator}")
        
        # Step 1: Preprocess and clean text
        cleaned_text = self._preprocess_text(regulation_text)
        
        # Step 2: Identify interpretation type
        interpretation_type = self._identify_interpretation_type(cleaned_text)
        
        # Step 3: Extract key components
        components = self._extract_components(cleaned_text, interpretation_type, regulator)
        
        # Step 4: Apply domain knowledge
        enhanced_components = self._apply_domain_knowledge(components, regulator)
        
        # Step 5: Generate structured interpretation
        interpretation = self._generate_interpretation(
            cleaned_text,
            interpretation_type,
            enhanced_components,
            regulator,
            context
        )
        
        # Step 6: Calculate confidence score
        interpretation.confidence_score = self._calculate_confidence(interpretation)
        
        # Cache the interpretation
        cache_key = f"{regulator}:{hash(regulation_text)}"
        self.interpretations_cache[cache_key] = interpretation
        
        return interpretation
        
    def _preprocess_text(self, text: str) -> str:
        """Clean and normalize regulatory text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Standardize section references
        text = re.sub(r'§\s*(\d+)', r'Section \1', text)
        # Expand common abbreviations
        abbreviations = {
            "Corp.": "Corporation",
            "Inc.": "Incorporated",
            "Ltd.": "Limited",
            "Co.": "Company"
        }
        for abbr, full in abbreviations.items():
            text = text.replace(abbr, full)
        return text.strip()
        
    def _identify_interpretation_type(self, text: str) -> InterpretationType:
        """Identify the type of regulatory interpretation needed"""
        text_lower = text.lower()
        
        # Check for calculation patterns
        if any(re.search(pattern, text_lower) for pattern in self.regulatory_patterns["calculations"]):
            return InterpretationType.CALCULATION
            
        # Check for prohibitions
        if any(re.search(pattern, text_lower) for pattern in self.regulatory_patterns["prohibitions"]):
            return InterpretationType.PROHIBITION
            
        # Check for exemptions
        if any(re.search(pattern, text_lower) for pattern in self.regulatory_patterns["exemptions"]):
            return InterpretationType.EXEMPTION
            
        # Check for process descriptions
        if "procedure" in text_lower or "process" in text_lower or "steps" in text_lower:
            return InterpretationType.PROCESS
            
        # Check for definitions
        if "means" in text_lower or "defined as" in text_lower:
            return InterpretationType.DEFINITION
            
        # Default to requirement
        return InterpretationType.REQUIREMENT
        
    def _extract_components(self, text: str, interpretation_type: InterpretationType, regulator: str) -> Dict[str, Any]:
        """Extract key components based on interpretation type"""
        components = {
            "actions": [],
            "conditions": [],
            "data_fields": [],
            "deadlines": [],
            "entities": [],
            "calculations": []
        }
        
        # Extract actions required
        for pattern in self.regulatory_patterns["requirements"]:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if "action" in match.groupdict():
                    components["actions"].append(match.group("action"))
                    
        # Extract data fields
        for pattern in self.regulatory_patterns["data_fields"]:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if "field" in match.groupdict():
                    components["data_fields"].append(match.group("field"))
                    
        # Extract conditions
        for pattern in self.regulatory_patterns["exemptions"]:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if "condition" in match.groupdict():
                    components["conditions"].append(match.group("condition"))
                    
        # Extract calculations if applicable
        if interpretation_type == InterpretationType.CALCULATION:
            for pattern in self.regulatory_patterns["calculations"]:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    if "formula" in match.groupdict():
                        components["calculations"].append(match.group("formula"))
                        
        return components
        
    def _apply_domain_knowledge(self, components: Dict[str, Any], regulator: str) -> Dict[str, Any]:
        """Enhance components with domain-specific knowledge"""
        enhanced = components.copy()
        
        if regulator.lower() in self.domain_knowledge:
            domain = self.domain_knowledge[regulator.lower()]
            
            # Map generic terms to specific forms
            if "report" in " ".join(components["actions"]).lower():
                for form in domain.get("forms", []):
                    if form.lower() in " ".join(components["actions"]).lower():
                        enhanced["specific_forms"] = [form]
                        
            # Enhance calculations with known formulas
            if components["calculations"] and "calculations" in domain:
                for calc in components["calculations"]:
                    for name, formula in domain["calculations"].items():
                        if name in calc.lower():
                            enhanced["calculation_formulas"] = {name: formula}
                            
        return enhanced
        
    def _generate_interpretation(self,
                               text: str,
                               interpretation_type: InterpretationType,
                               components: Dict[str, Any],
                               regulator: str,
                               context: Optional[Dict[str, Any]]) -> RegulatoryInterpretation:
        """Generate the final structured interpretation"""
        
        # Build interpreted meaning
        interpreted_meaning = self._build_interpreted_meaning(interpretation_type, components)
        
        # Extract data requirements
        data_requirements = list(set(components.get("data_fields", [])))
        
        # Get calculation formula if present
        calculation_formula = None
        if "calculation_formulas" in components:
            calculation_formula = json.dumps(components["calculation_formulas"])
            
        # Build conditions list
        conditions = components.get("conditions", [])
        
        # Set effective date (would be extracted from text in production)
        effective_date = datetime.now()
        
        # Create metadata
        metadata = {
            "regulator": regulator,
            "interpretation_timestamp": datetime.now().isoformat(),
            "components": components,
            "context": context or {}
        }
        
        return RegulatoryInterpretation(
            regulation_id=f"{regulator}_{hash(text)}",
            section="TBD",  # Would be extracted from text
            interpretation_type=interpretation_type,
            original_text=text,
            interpreted_meaning=interpreted_meaning,
            data_requirements=data_requirements,
            calculation_formula=calculation_formula,
            conditions=conditions,
            effective_date=effective_date,
            confidence_score=0.0,  # Will be calculated
            metadata=metadata
        )
        
    def _build_interpreted_meaning(self, interpretation_type: InterpretationType, components: Dict[str, Any]) -> str:
        """Build human-readable interpretation"""
        if interpretation_type == InterpretationType.REQUIREMENT:
            actions = components.get("actions", ["perform required actions"])
            fields = components.get("data_fields", [])
            if fields:
                return f"Must {', '.join(actions)} and report {', '.join(fields)}"
            return f"Must {', '.join(actions)}"
            
        elif interpretation_type == InterpretationType.PROHIBITION:
            actions = components.get("actions", ["perform prohibited actions"])
            return f"Prohibited from {', '.join(actions)}"
            
        elif interpretation_type == InterpretationType.CALCULATION:
            calcs = components.get("calculations", ["specified calculations"])
            return f"Calculate values using: {', '.join(calcs)}"
            
        elif interpretation_type == InterpretationType.EXEMPTION:
            conditions = components.get("conditions", ["specified conditions"])
            return f"Exemption applies if: {'; '.join(conditions)}"
            
        else:
            return "Interpretation requires manual review"
            
    def _calculate_confidence(self, interpretation: RegulatoryInterpretation) -> float:
        """Calculate confidence score for the interpretation"""
        score = 0.5  # Base score
        
        # Increase confidence based on identified components
        if interpretation.data_requirements:
            score += 0.1 * min(len(interpretation.data_requirements), 3)
        if interpretation.conditions:
            score += 0.1 * min(len(interpretation.conditions), 2)
        if interpretation.calculation_formula:
            score += 0.2
            
        # Decrease confidence for ambiguous language
        ambiguous_terms = ["may", "could", "might", "generally", "typically"]
        for term in ambiguous_terms:
            if term in interpretation.original_text.lower():
                score -= 0.05
                
        return min(max(score, 0.0), 1.0)
        
    async def analyze_regulatory_change(self, 
                                      old_regulation: str,
                                      new_regulation: str,
                                      regulator: str) -> Dict[str, Any]:
        """Analyze changes between regulation versions"""
        old_interp = await self.interpret_regulation(old_regulation, regulator)
        new_interp = await self.interpret_regulation(new_regulation, regulator)
        
        changes = {
            "type_changed": old_interp.interpretation_type != new_interp.interpretation_type,
            "new_requirements": list(set(new_interp.data_requirements) - set(old_interp.data_requirements)),
            "removed_requirements": list(set(old_interp.data_requirements) - set(new_interp.data_requirements)),
            "calculation_changed": old_interp.calculation_formula != new_interp.calculation_formula,
            "conditions_changed": old_interp.conditions != new_interp.conditions,
            "impact_assessment": self._assess_change_impact(old_interp, new_interp)
        }
        
        return changes
        
    def _assess_change_impact(self, old: RegulatoryInterpretation, new: RegulatoryInterpretation) -> str:
        """Assess the impact of regulatory changes"""
        if new.interpretation_type == InterpretationType.PROHIBITION and old.interpretation_type != InterpretationType.PROHIBITION:
            return "HIGH - New prohibition introduced"
        elif len(new.data_requirements) > len(old.data_requirements):
            return "MEDIUM - Additional reporting requirements"
        elif new.calculation_formula != old.calculation_formula:
            return "MEDIUM - Calculation methodology changed"
        else:
            return "LOW - Minor changes"