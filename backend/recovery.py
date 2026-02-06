"""
Auto-Recovery System
Automatically attempts to recover from incidents
"""
from database.models import RecoveryAction, Incident, get_db_session
from datetime import datetime
import random
import time


class AutoRecovery:
    """Handles automatic recovery actions for incidents"""
    
    # Recovery strategies for different incident types
    RECOVERY_STRATEGIES = {
        'cpu': [
            {'action': 'restart_service', 'priority': 1},
            {'action': 'scale_horizontally', 'priority': 2},
            {'action': 'optimize_resources', 'priority': 3}
        ],
        'memory': [
            {'action': 'clear_cache', 'priority': 1},
            {'action': 'restart_service', 'priority': 2},
            {'action': 'scale_vertically', 'priority': 3}
        ],
        'disk': [
            {'action': 'cleanup_logs', 'priority': 1},
            {'action': 'archive_data', 'priority': 2},
            {'action': 'expand_storage', 'priority': 3}
        ],
        'response_time': [
            {'action': 'restart_service', 'priority': 1},
            {'action': 'scale_horizontally', 'priority': 2},
            {'action': 'enable_caching', 'priority': 3}
        ],
        'error_rate': [
            {'action': 'rollback_deployment', 'priority': 1},
            {'action': 'restart_service', 'priority': 2},
            {'action': 'enable_circuit_breaker', 'priority': 3}
        ]
    }
    
    def __init__(self):
        self.db = get_db_session()
    
    def attempt_recovery(self, incident_id: int) -> dict:
        """
        Attempt to recover from an incident
        
        Args:
            incident_id: ID of the incident to recover from
            
        Returns:
            dict: Recovery action result
        """
        # Get incident details
        incident = self.db.query(Incident).filter(Incident.id == incident_id).first()
        
        if not incident:
            return {'success': False, 'error': 'Incident not found'}
        
        if incident.status in ['resolved', 'closed']:
            return {'success': False, 'error': 'Incident already resolved'}
        
        # Update incident status
        incident.status = 'investigating'
        self.db.commit()
        
        # Determine recovery strategy based on error type
        metric_name = self._extract_metric_from_incident(incident)
        strategies = self.RECOVERY_STRATEGIES.get(metric_name, [])
        
        if not strategies:
            return {'success': False, 'error': 'No recovery strategy available'}
        
        # Try recovery actions in order of priority
        for strategy in strategies:
            action_type = strategy['action']
            result = self._execute_recovery_action(incident, action_type)
            
            if result['success']:
                # Mark incident as resolved
                incident.status = 'resolved'
                incident.resolved_at = datetime.utcnow()
                incident.auto_recovered = True
                incident.recovery_action = action_type
                self.db.commit()
                
                return result
        
        # If all strategies failed
        incident.status = 'open'
        self.db.commit()
        
        return {
            'success': False, 
            'error': 'All recovery attempts failed',
            'incident_id': incident_id
        }
    
    def _extract_metric_from_incident(self, incident: Incident) -> str:
        """Extract metric type from incident error message"""
        error_msg = (incident.error_message or '').lower()
        
        for metric in ['cpu', 'memory', 'disk', 'response_time', 'error_rate']:
            if metric in error_msg:
                return metric
        
        return 'unknown'
    
    def _execute_recovery_action(self, incident: Incident, action_type: str) -> dict:
        """
        Execute a specific recovery action
        
        Args:
            incident: The incident to recover from
            action_type: Type of recovery action to execute
            
        Returns:
            dict: Result of the recovery action
        """
        # Log the recovery action
        recovery_action = RecoveryAction(
            incident_id=incident.id,
            action_type=action_type,
            action_details=f"Executing {action_type} for {incident.service_name}",
            status='pending'
        )
        self.db.add(recovery_action)
        self.db.commit()
        
        # Simulate recovery action execution
        success = self._simulate_action(action_type, incident.service_name)
        
        # Update recovery action status
        recovery_action.status = 'success' if success else 'failed'
        if not success:
            recovery_action.error_message = f"Failed to execute {action_type}"
        self.db.commit()
        
        return {
            'success': success,
            'action_type': action_type,
            'incident_id': incident.id,
            'service_name': incident.service_name
        }
    
    def _simulate_action(self, action_type: str, service_name: str) -> bool:
        """
        Simulate executing a recovery action
        In production, this would call actual infrastructure APIs
        
        Args:
            action_type: Type of action to execute
            service_name: Name of the service
            
        Returns:
            bool: True if action succeeded, False otherwise
        """
        # Simulate action execution time
        time.sleep(0.5)
        
        # Simulate success/failure (80% success rate)
        success = random.random() < 0.8
        
        if success:
            print(f"✅ Successfully executed {action_type} for {service_name}")
        else:
            print(f"❌ Failed to execute {action_type} for {service_name}")
        
        return success
    
    def get_recovery_history(self, incident_id: int = None):
        """Get recovery action history"""
        query = self.db.query(RecoveryAction)
        
        if incident_id:
            query = query.filter(RecoveryAction.incident_id == incident_id)
        
        actions = query.order_by(RecoveryAction.executed_at.desc()).all()
        return [action.to_dict() for action in actions]
    
    def get_recovery_stats(self):
        """Get recovery statistics"""
        total = self.db.query(RecoveryAction).count()
        successful = self.db.query(RecoveryAction).filter(
            RecoveryAction.status == 'success'
        ).count()
        failed = self.db.query(RecoveryAction).filter(
            RecoveryAction.status == 'failed'
        ).count()
        
        success_rate = (successful / total * 100) if total > 0 else 0
        
        return {
            'total_actions': total,
            'successful': successful,
            'failed': failed,
            'success_rate': round(success_rate, 2)
        }
    
    def close(self):
        """Close database connection"""
        self.db.close()


if __name__ == "__main__":
    # Test auto-recovery
    recovery = AutoRecovery()
    print("Auto-recovery system initialized!")
    recovery.close()
