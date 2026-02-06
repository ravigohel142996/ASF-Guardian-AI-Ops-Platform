"""
Background Monitoring Worker
Continuously monitors system health using Celery
"""
from celery import Celery
from celery.schedules import crontab
import psutil
import random
import os
from backend.incidents import IncidentDetector
from backend.recovery import AutoRecovery

# Initialize Celery
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
app = Celery('asf_guardian', broker=REDIS_URL, backend=REDIS_URL)

# Celery configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Celery Beat schedule for periodic tasks
app.conf.beat_schedule = {
    'monitor-system-health': {
        'task': 'workers.monitor.monitor_system_health',
        'schedule': 60.0,  # Run every 60 seconds
    },
    'monitor-services': {
        'task': 'workers.monitor.monitor_services',
        'schedule': 120.0,  # Run every 2 minutes
    },
}


@app.task(name='workers.monitor.monitor_system_health')
def monitor_system_health():
    """
    Monitor system health metrics
    Runs periodically to check CPU, memory, and disk usage
    """
    try:
        detector = IncidentDetector()
        
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent
        
        # Check each metric
        incidents = []
        
        cpu_incident = detector.check_metric('system', 'cpu', cpu_percent)
        if cpu_incident:
            incidents.append(cpu_incident)
            trigger_recovery.delay(cpu_incident['id'])
        
        memory_incident = detector.check_metric('system', 'memory', memory_percent)
        if memory_incident:
            incidents.append(memory_incident)
            trigger_recovery.delay(memory_incident['id'])
        
        disk_incident = detector.check_metric('system', 'disk', disk_percent)
        if disk_incident:
            incidents.append(disk_incident)
            trigger_recovery.delay(disk_incident['id'])
        
        detector.close()
        
        result = {
            'status': 'success',
            'metrics': {
                'cpu': cpu_percent,
                'memory': memory_percent,
                'disk': disk_percent
            },
            'incidents_created': len(incidents)
        }
        
        print(f"✅ System health monitored: {result}")
        return result
    
    except Exception as e:
        print(f"❌ Error monitoring system health: {str(e)}")
        return {'status': 'error', 'message': str(e)}


@app.task(name='workers.monitor.monitor_services')
def monitor_services():
    """
    Monitor application services
    Simulates monitoring of various microservices
    """
    try:
        detector = IncidentDetector()
        
        # Simulate monitoring different services
        services = [
            'web-api',
            'database',
            'cache-server',
            'auth-service',
            'payment-service'
        ]
        
        incidents = []
        
        for service in services:
            # Simulate response time monitoring (random for demo)
            response_time = random.uniform(100, 6000)
            
            incident = detector.check_metric(service, 'response_time', response_time)
            if incident:
                incidents.append(incident)
                trigger_recovery.delay(incident['id'])
        
        detector.close()
        
        result = {
            'status': 'success',
            'services_monitored': len(services),
            'incidents_created': len(incidents)
        }
        
        print(f"✅ Services monitored: {result}")
        return result
    
    except Exception as e:
        print(f"❌ Error monitoring services: {str(e)}")
        return {'status': 'error', 'message': str(e)}


@app.task(name='workers.monitor.trigger_recovery')
def trigger_recovery(incident_id: int):
    """
    Trigger auto-recovery for an incident
    
    Args:
        incident_id: ID of the incident to recover
    """
    try:
        recovery = AutoRecovery()
        result = recovery.attempt_recovery(incident_id)
        recovery.close()
        
        # Send email alert if configured
        from alerts.mailer import send_incident_alert
        send_incident_alert.delay(incident_id, result)
        
        print(f"🔄 Recovery triggered for incident {incident_id}: {result}")
        return result
    
    except Exception as e:
        print(f"❌ Recovery failed for incident {incident_id}: {str(e)}")
        return {'status': 'error', 'message': str(e)}


@app.task(name='workers.monitor.simulate_incident')
def simulate_incident(service_name: str, metric_name: str, severity: str = 'high'):
    """
    Simulate an incident for testing purposes
    
    Args:
        service_name: Name of the service
        metric_name: Type of metric (cpu, memory, etc.)
        severity: Severity level
    """
    try:
        detector = IncidentDetector()
        
        # Get threshold and exceed it
        threshold = detector.THRESHOLDS.get(metric_name, 100)
        
        # Generate value based on severity
        if severity == 'critical':
            value = threshold * 1.6
        elif severity == 'high':
            value = threshold * 1.3
        else:
            value = threshold * 1.15
        
        incident = detector.check_metric(service_name, metric_name, value)
        detector.close()
        
        if incident:
            trigger_recovery(incident['id'])
            print(f"✅ Simulated incident created: {incident}")
            return incident
        
        return {'status': 'no_incident_created'}
    
    except Exception as e:
        print(f"❌ Error simulating incident: {str(e)}")
        return {'status': 'error', 'message': str(e)}


if __name__ == '__main__':
    # Run worker
    app.start()
