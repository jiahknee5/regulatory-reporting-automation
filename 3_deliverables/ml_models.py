"""
Machine Learning Models for Regulatory Reporting
Includes anomaly detection, NLP parsing, and prediction models
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from transformers import pipeline, AutoTokenizer, AutoModel
import torch
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class AnomalyDetector:
    """Detect anomalies in financial data"""
    
    def __init__(self):
        self.model = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        self.is_trained = False
        
    def train(self, historical_data: pd.DataFrame):
        """Train anomaly detection model"""
        features = self._extract_features(historical_data)
        self.model.fit(features)
        self.is_trained = True
        logger.info("Anomaly detector trained successfully")
        
    def detect(self, data: pd.DataFrame) -> pd.DataFrame:
        """Detect anomalies in new data"""
        if not self.is_trained:
            raise ValueError("Model not trained yet")
            
        features = self._extract_features(data)
        predictions = self.model.predict(features)
        
        # -1 indicates anomaly
        data['is_anomaly'] = predictions == -1
        data['anomaly_score'] = self.model.score_samples(features)
        
        return data
        
    def _extract_features(self, data: pd.DataFrame) -> np.ndarray:
        """Extract numerical features for anomaly detection"""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        return data[numeric_cols].fillna(0).values

class RegulatoryNLPParser:
    """Parse regulatory text using NLP"""
    
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.model = AutoModel.from_pretrained("bert-base-uncased")
        self.classifier = pipeline(
            "text-classification",
            model="bert-base-uncased"
        )
        
    def parse_regulation(self, text: str) -> Dict:
        """Extract requirements from regulatory text"""
        # Tokenize
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            max_length=512,
            truncation=True
        )
        
        # Get embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
            
        # Extract key information
        requirements = self._extract_requirements(text)
        deadlines = self._extract_deadlines(text)
        data_fields = self._extract_data_fields(text)
        
        return {
            "requirements": requirements,
            "deadlines": deadlines,
            "data_fields": data_fields,
            "complexity_score": self._calculate_complexity(text)
        }
        
    def _extract_requirements(self, text: str) -> List[str]:
        """Extract requirement statements"""
        # Simplified - in production use more sophisticated NER
        requirements = []
        sentences = text.split('.')
        
        for sentence in sentences:
            if any(word in sentence.lower() for word in ['must', 'shall', 'required']):
                requirements.append(sentence.strip())
                
        return requirements
        
    def _extract_deadlines(self, text: str) -> List[Dict]:
        """Extract deadline information"""
        # Simplified date extraction
        import re
        date_pattern = r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b'
        dates = re.findall(date_pattern, text)
        
        return [{"date": date, "context": "extracted"} for date in dates]
        
    def _extract_data_fields(self, text: str) -> List[str]:
        """Extract required data fields"""
        # In production, use NER to identify financial terms
        fields = []
        financial_terms = ['revenue', 'assets', 'liabilities', 'equity', 'income']
        
        for term in financial_terms:
            if term in text.lower():
                fields.append(term)
                
        return fields
        
    def _calculate_complexity(self, text: str) -> float:
        """Calculate regulatory complexity score"""
        # Simple heuristic - can be enhanced
        word_count = len(text.split())
        requirement_count = len(self._extract_requirements(text))
        
        return min(1.0, (word_count / 1000 + requirement_count / 10) / 2)

class CompliancePredictorcompliancepredictor:
    """Predict compliance risks using ML"""
    
    def __init__(self):
        self.risk_factors = {}
        self.historical_issues = []
        
    def predict_risk(self, report_data: pd.DataFrame, metadata: Dict) -> Dict:
        """Predict compliance risk for a report"""
        risk_score = 0.0
        risk_factors = []
        
        # Check data completeness
        completeness = 1 - (report_data.isnull().sum().sum() / report_data.size)
        if completeness < 0.95:
            risk_score += 0.3
            risk_factors.append("Incomplete data")
            
        # Check historical issues
        if metadata.get('report_type') in self.historical_issues:
            risk_score += 0.2
            risk_factors.append("Historical issues with this report type")
            
        # Check deadline proximity
        days_until_deadline = metadata.get('days_until_deadline', 30)
        if days_until_deadline < 5:
            risk_score += 0.4
            risk_factors.append("Close to deadline")
            
        return {
            "risk_score": min(1.0, risk_score),
            "risk_level": self._get_risk_level(risk_score),
            "risk_factors": risk_factors,
            "recommendations": self._get_recommendations(risk_factors)
        }
        
    def _get_risk_level(self, score: float) -> str:
        """Convert risk score to level"""
        if score < 0.3:
            return "LOW"
        elif score < 0.7:
            return "MEDIUM"
        else:
            return "HIGH"
            
    def _get_recommendations(self, factors: List[str]) -> List[str]:
        """Generate recommendations based on risk factors"""
        recommendations = []
        
        if "Incomplete data" in factors:
            recommendations.append("Review and complete missing data fields")
        if "Close to deadline" in factors:
            recommendations.append("Prioritize report completion and review")
        if "Historical issues with this report type" in factors:
            recommendations.append("Perform additional quality checks")
            
        return recommendations

# Export model instances
anomaly_detector = AnomalyDetector()
nlp_parser = RegulatoryNLPParser()
compliance_predictor = CompliancePredictor()
