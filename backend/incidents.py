"""
Incident Detection Engine
Monitors system health and detects anomalies
"""
from database.models import Incident, SystemMetric, get_db_session
from datetime import datetime
import random


class IncidentDetector:
    """Detects and creates incidents based on system metrics"""
    
    # Thresholds for different metrics
    THRESHOLDS = {
        'cpu': 80.0,  # percentage
        'memory': 85.0,  # percentage
        'disk': 90.0,  # percentage
        'response_time': 5000.0,  # milliseconds
        'error_rate': 5.0  # percentage
    }
    
    def __init__(self):
        self.db = get_db_session()
    
    def check_metric(self, service_name: str, metric_name: str, metric_value: float) -> dict:
        """
        Check if a metric exceeds threshold and create incident if needed
        
        Args:
            service_name: Name of the service
            metric_name: Name of the metric (cpu, memory, etc.)
            metric_value: Current value of the metric
            
        Returns:
            dict: Incident information if created, None otherwise
        """
        threshold = self.THRESHOLDS.get(metric_name, float('inf'))
        
        # Store the metric
        metric = SystemMetric(
            service_name=service_name,
            metric_name=metric_name,
            metric_value=metric_value,
            is_healthy=metric_value <= threshold
        )
        self.db.add(metric)
        self.db.commit()
        
        # Check if threshold exceeded
        if metric_value > threshold:
            return self.create_incident(service_name, metric_name, metric_value, threshold)
        
        return None
    
    def create_incident(self, service_name: str, metric_name: str, 
                       metric_value: float, threshold: float) -> dict:
        """
        Create a new incident
        
        Args:
            service_name: Name of the service
            metric_name: Name of the metric
            metric_value: Current metric value
            threshold: Threshold that was exceeded
            
        Returns:
            dict: Created incident information
        """
        # Determine severity based on how much threshold is exceeded
        severity = self._calculate_severity(metric_value, threshold)
        
        # Create incident title and description
        title = f"{service_name} - High {metric_name.upper()}"
        description = f"{metric_name} usage at {metric_value:.2f}% (threshold: {threshold}%)"
        
        # Create incident in database
        incident = Incident(
            title=title,
            description=description,
            severity=severity,
            status='open',
            service_name=service_name,
            error_message=f"{metric_name} exceeded threshold",
            metric_value=metric_value,
            threshold_value=threshold
        )
        
        self.db.add(incident)
        self.db.commit()
        self.db.refresh(incident)
        
        return incident.to_dict()
    
    def _calculate_severity(self, value: float, threshold: float) -> str:
        """Calculate incident severity based on threshold exceeded"""
        excess = (value - threshold) / threshold
        
        if excess > 0.5:  # 50% above threshold
            return 'critical'
        elif excess > 0.25:  # 25% above threshold
            return 'high'
        elif excess > 0.1:  # 10% above threshold
            return 'medium'
        else:
            return 'low'
    
    def get_open_incidents(self):
        """Get all open incidents"""
        incidents = self.db.query(Incident).filter(
            Incident.status.in_(['open', 'investigating'])
        ).order_by(Incident.detected_at.desc()).all()
        
        return [inc.to_dict() for inc in incidents]
    
    def get_incident_by_id(self, incident_id: int):
        """Get incident by ID"""
        incident = self.db.query(Incident).filter(Incident.id == incident_id).first()
        return incident.to_dict() if incident else None
    
    def update_incident_status(self, incident_id: int, status: str, 
                              recovery_action: str = None):
        """Update incident status"""
        incident = self.db.query(Incident).filter(Incident.id == incident_id).first()
        
        if incident:
            incident.status = status
            if recovery_action:
                incident.recovery_action = recovery_action
                incident.auto_recovered = True
            if status in ['resolved', 'closed']:
                incident.resolved_at = datetime.utcnow()
            
            self.db.commit()
            return incident.to_dict()
        
        return None
    
    def get_incident_history(self, limit: int = 50):
        """Get incident history"""
        incidents = self.db.query(Incident).order_by(
            Incident.detected_at.desc()
        ).limit(limit).all()
        
        return [inc.to_dict() for inc in incidents]
    
    def get_incident_stats(self):
        """Get incident statistics"""
        total = self.db.query(Incident).count()
        open_count = self.db.query(Incident).filter(Incident.status == 'open').count()
        resolved = self.db.query(Incident).filter(Incident.status == 'resolved').count()
        auto_recovered = self.db.query(Incident).filter(Incident.auto_recovered == True).count()
        
        return {
            'total': total,
            'open': open_count,
            'resolved': resolved,
            'auto_recovered': auto_recovered
        }
    
    def close(self):
        """Close database connection"""
        self.db.close()


def generate_demo_incidents():
    """Generate demo incidents for testing"""
    detector = IncidentDetector()
    
    demo_services = ['web-api', 'database', 'cache-server', 'auth-service']
    demo_metrics = ['cpu', 'memory', 'response_time']
    
    for service in demo_services:
        for metric in demo_metrics:
            # Generate some incidents
            if random.random() > 0.7:  # 30% chance of incident
                value = detector.THRESHOLDS[metric] * random.uniform(1.1, 1.5)
                detector.check_metric(service, metric, value)
    
    detector.close()
    print("✅ Demo incidents generated!")


if __name__ == "__main__":
    generate_demo_incidents()
