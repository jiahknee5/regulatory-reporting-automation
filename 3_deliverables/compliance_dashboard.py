"""
Compliance Dashboard Module
Real-time monitoring and visualization of regulatory compliance
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
from dataclasses import dataclass, asdict
from collections import defaultdict
import asyncio
import logging

logger = logging.getLogger(__name__)

@dataclass 
class ComplianceStatus:
    """Status of a specific compliance requirement"""
    requirement_id: str
    regulator: str
    report_type: str
    status: str  # "compliant", "pending", "overdue", "failed"
    last_submission: Optional[datetime]
    next_deadline: datetime
    completion_percentage: float
    issues: List[str]

class ComplianceDashboard:
    """Main compliance monitoring dashboard"""
    
    def __init__(self):
        self.compliance_items: Dict[str, ComplianceStatus] = {}
        self.submission_history: List[Dict] = []
        self.alerts: List[Dict] = []
        self.metrics_cache = {}
        
    def update_compliance_status(self, requirement_id: str, status: ComplianceStatus):
        """Update status for a compliance requirement"""
        self.compliance_items[requirement_id] = status
        
        # Check for alerts
        if status.status == "overdue":
            self.create_alert(
                f"OVERDUE: {status.report_type} for {status.regulator}",
                "HIGH",
                {"requirement_id": requirement_id}
            )
        elif status.next_deadline <= datetime.now() + timedelta(days=7):
            self.create_alert(
                f"UPCOMING: {status.report_type} due in 7 days",
                "MEDIUM",
                {"requirement_id": requirement_id}
            )
            
    def create_alert(self, message: str, severity: str, context: Dict = None):
        """Create compliance alert"""
        alert = {
            "id": f"alert_{len(self.alerts)}",
            "message": message,
            "severity": severity,
            "timestamp": datetime.now().isoformat(),
            "acknowledged": False,
            "context": context or {}
        }
        self.alerts.append(alert)
        logger.warning(f"Compliance alert: {message}")
        
    def record_submission(self, report_type: str, regulator: str, 
                         status: str, submission_id: str):
        """Record report submission"""
        submission = {
            "submission_id": submission_id,
            "report_type": report_type,
            "regulator": regulator,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        self.submission_history.append(submission)
        
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data"""
        return {
            "overview": self._get_overview_metrics(),
            "compliance_status": self._get_compliance_summary(),
            "upcoming_deadlines": self._get_upcoming_deadlines(),
            "recent_submissions": self._get_recent_submissions(),
            "alerts": self._get_active_alerts(),
            "trends": self._get_compliance_trends()
        }
        
    def _get_overview_metrics(self) -> Dict[str, Any]:
        """Get high-level compliance metrics"""
        total_requirements = len(self.compliance_items)
        compliant = sum(1 for item in self.compliance_items.values() 
                       if item.status == "compliant")
        pending = sum(1 for item in self.compliance_items.values() 
                     if item.status == "pending")
        overdue = sum(1 for item in self.compliance_items.values() 
                     if item.status == "overdue")
        
        compliance_rate = (compliant / total_requirements * 100) if total_requirements > 0 else 100
        
        return {
            "total_requirements": total_requirements,
            "compliant": compliant,
            "pending": pending,
            "overdue": overdue,
            "compliance_rate": round(compliance_rate, 2),
            "active_alerts": len([a for a in self.alerts if not a["acknowledged"]])
        }
        
    def _get_compliance_summary(self) -> Dict[str, List[Dict]]:
        """Get compliance status by regulator"""
        summary = defaultdict(list)
        
        for item in self.compliance_items.values():
            summary[item.regulator].append({
                "report_type": item.report_type,
                "status": item.status,
                "completion": item.completion_percentage,
                "next_deadline": item.next_deadline.isoformat()
            })
            
        return dict(summary)
        
    def _get_upcoming_deadlines(self) -> List[Dict]:
        """Get upcoming reporting deadlines"""
        deadlines = []
        cutoff_date = datetime.now() + timedelta(days=30)
        
        for item in self.compliance_items.values():
            if item.next_deadline <= cutoff_date:
                days_until = (item.next_deadline - datetime.now()).days
                deadlines.append({
                    "requirement_id": item.requirement_id,
                    "report_type": item.report_type,
                    "regulator": item.regulator,
                    "deadline": item.next_deadline.isoformat(),
                    "days_until": days_until,
                    "status": item.status,
                    "urgency": "HIGH" if days_until < 7 else "MEDIUM"
                })
                
        # Sort by deadline
        deadlines.sort(key=lambda x: x["deadline"])
        return deadlines[:10]  # Top 10 upcoming
        
    def _get_recent_submissions(self) -> List[Dict]:
        """Get recent report submissions"""
        # Return last 20 submissions
        return self.submission_history[-20:]
        
    def _get_active_alerts(self) -> List[Dict]:
        """Get unacknowledged alerts"""
        return [a for a in self.alerts if not a["acknowledged"]][-10:]
        
    def _get_compliance_trends(self) -> Dict[str, Any]:
        """Calculate compliance trends"""
        # Group submissions by month
        monthly_stats = defaultdict(lambda: {"total": 0, "successful": 0})
        
        for submission in self.submission_history:
            timestamp = datetime.fromisoformat(submission["timestamp"])
            month_key = timestamp.strftime("%Y-%m")
            monthly_stats[month_key]["total"] += 1
            if submission["status"] == "success":
                monthly_stats[month_key]["successful"] += 1
                
        # Calculate trend
        months = sorted(monthly_stats.keys())[-6:]  # Last 6 months
        trend_data = []
        
        for month in months:
            stats = monthly_stats[month]
            success_rate = (stats["successful"] / stats["total"] * 100) if stats["total"] > 0 else 0
            trend_data.append({
                "month": month,
                "total_submissions": stats["total"],
                "success_rate": round(success_rate, 2)
            })
            
        return {
            "monthly_trends": trend_data,
            "overall_trend": self._calculate_trend_direction(trend_data)
        }
        
    def _calculate_trend_direction(self, trend_data: List[Dict]) -> str:
        """Calculate if compliance is improving or declining"""
        if len(trend_data) < 2:
            return "stable"
            
        recent_rates = [d["success_rate"] for d in trend_data[-3:]]
        older_rates = [d["success_rate"] for d in trend_data[:-3]]
        
        if not older_rates:
            return "stable"
            
        recent_avg = sum(recent_rates) / len(recent_rates)
        older_avg = sum(older_rates) / len(older_rates)
        
        if recent_avg > older_avg + 5:
            return "improving"
        elif recent_avg < older_avg - 5:
            return "declining"
        else:
            return "stable"
            
    def export_compliance_report(self, filepath: str):
        """Export compliance data for reporting"""
        report_data = {
            "generated_at": datetime.now().isoformat(),
            "dashboard_data": self.get_dashboard_data(),
            "compliance_items": [
                {
                    "requirement_id": k,
                    **asdict(v),
                    "last_submission": v.last_submission.isoformat() if v.last_submission else None,
                    "next_deadline": v.next_deadline.isoformat()
                }
                for k, v in self.compliance_items.items()
            ],
            "submission_history": self.submission_history,
            "alerts": self.alerts
        }
        
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=2)
            
        logger.info(f"Compliance report exported to {filepath}")

# Export dashboard instance
dashboard = ComplianceDashboard()
