"""
Monitoring Module for Regulatory Reporting System
Tracks system health, performance, and compliance metrics
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from dataclasses import dataclass
from collections import defaultdict
import json

logger = logging.getLogger(__name__)

@dataclass
class ReportMetrics:
    """Metrics for a single report"""
    report_id: str
    report_type: str
    processing_time: float
    validation_errors: int
    submission_status: str
    timestamp: datetime

class MonitoringSystem:
    """Main monitoring system for regulatory reporting"""
    
    def __init__(self):
        self.metrics: List[ReportMetrics] = []
        self.alerts: List[Dict] = []
        self.performance_data = defaultdict(list)
        self.compliance_scores = {}
        
    def track_report(self, report_id: str, report_type: str, 
                     start_time: float, errors: int = 0,
                     status: str = "success"):
        """Track report processing metrics"""
        processing_time = time.time() - start_time
        
        metric = ReportMetrics(
            report_id=report_id,
            report_type=report_type,
            processing_time=processing_time,
            validation_errors=errors,
            submission_status=status,
            timestamp=datetime.now()
        )
        
        self.metrics.append(metric)
        self.performance_data[report_type].append(processing_time)
        
        # Check for alerts
        if processing_time > 300:  # 5 minutes
            self.create_alert("PERFORMANCE", f"Report {report_id} took {processing_time:.2f}s")
        if errors > 0:
            self.create_alert("VALIDATION", f"Report {report_id} has {errors} errors")
            
    def create_alert(self, alert_type: str, message: str, severity: str = "MEDIUM"):
        """Create system alert"""
        alert = {
            "type": alert_type,
            "message": message,
            "severity": severity,
            "timestamp": datetime.now().isoformat(),
            "acknowledged": False
        }
        
        self.alerts.append(alert)
        logger.warning(f"Alert created: {alert_type} - {message}")
        
    def get_dashboard_metrics(self) -> Dict:
        """Get metrics for dashboard display"""
        now = datetime.now()
        last_24h = now - timedelta(hours=24)
        
        recent_metrics = [m for m in self.metrics if m.timestamp > last_24h]
        
        # Calculate statistics
        if recent_metrics:
            avg_processing_time = sum(m.processing_time for m in recent_metrics) / len(recent_metrics)
            success_rate = sum(1 for m in recent_metrics if m.submission_status == "success") / len(recent_metrics)
            total_errors = sum(m.validation_errors for m in recent_metrics)
        else:
            avg_processing_time = 0
            success_rate = 1.0
            total_errors = 0
            
        return {
            "reports_processed_24h": len(recent_metrics),
            "average_processing_time": avg_processing_time,
            "success_rate": success_rate,
            "total_validation_errors": total_errors,
            "active_alerts": len([a for a in self.alerts if not a["acknowledged"]]),
            "system_health": self._calculate_system_health()
        }
        
    def get_compliance_metrics(self) -> Dict:
        """Get compliance-specific metrics"""
        # Group by report type
        report_stats = defaultdict(lambda: {"total": 0, "on_time": 0, "errors": 0})
        
        for metric in self.metrics:
            stats = report_stats[metric.report_type]
            stats["total"] += 1
            if metric.submission_status == "success":
                stats["on_time"] += 1
            stats["errors"] += metric.validation_errors
            
        # Calculate compliance scores
        compliance_data = {}
        for report_type, stats in report_stats.items():
            if stats["total"] > 0:
                compliance_data[report_type] = {
                    "compliance_rate": stats["on_time"] / stats["total"],
                    "error_rate": stats["errors"] / stats["total"],
                    "total_reports": stats["total"]
                }
                
        return compliance_data
        
    def _calculate_system_health(self) -> str:
        """Calculate overall system health"""
        # Simple health calculation
        recent_alerts = [a for a in self.alerts[-10:] if a["severity"] == "HIGH"]
        
        if len(recent_alerts) > 2:
            return "CRITICAL"
        elif len(recent_alerts) > 0:
            return "WARNING"
        else:
            return "HEALTHY"
            
    def export_metrics(self, filepath: str):
        """Export metrics to file"""
        data = {
            "metrics": [
                {
                    "report_id": m.report_id,
                    "report_type": m.report_type,
                    "processing_time": m.processing_time,
                    "validation_errors": m.validation_errors,
                    "submission_status": m.submission_status,
                    "timestamp": m.timestamp.isoformat()
                }
                for m in self.metrics
            ],
            "alerts": self.alerts,
            "exported_at": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
            
        logger.info(f"Metrics exported to {filepath}")

# Global monitoring instance
monitor = MonitoringSystem()
