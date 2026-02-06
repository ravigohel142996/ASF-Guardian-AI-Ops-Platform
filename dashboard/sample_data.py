"""
Sample Data Generator
Generates realistic demo data for the dashboard
"""
import random
from datetime import datetime, timedelta


def generate_kpi_metrics():
    """Generate KPI metrics data"""
    return {
        'system_health': random.randint(88, 98),
        'health_trend': random.choice(['+2', '+3', '+1', '-1']),
        'failure_risk': random.randint(8, 18),
        'risk_trend': random.choice(['-3', '-2', '-1', '+1']),
        'active_incidents': random.randint(1, 8),
        'incidents_trend': random.choice(['-2', '-1', '0', '+1']),
        'monthly_cost': random.randint(3800, 4800),
        'cost_trend': random.choice(['+3', '+5', '+7', '-2'])
    }


def generate_sample_incidents(count=20):
    """Generate sample incident data"""
    services = ['web-api', 'database', 'cache-server', 'auth-service', 'payment-service', 'notification-service']
    metrics = ['cpu', 'memory', 'disk', 'response_time', 'error_rate']
    severities = ['critical', 'high', 'medium', 'low']
    statuses = ['open', 'investigating', 'resolved', 'closed']
    
    incidents = []
    
    for i in range(count):
        service = random.choice(services)
        metric = random.choice(metrics)
        severity = random.choice(severities)
        status = random.choice(statuses)
        
        # Weight towards resolved/closed for older incidents
        if i < count * 0.3:
            status = random.choice(['open', 'investigating'])
        
        created_time = datetime.now() - timedelta(hours=random.randint(1, 168))
        
        title_templates = {
            'cpu': f'High CPU usage detected on {service}',
            'memory': f'Memory threshold exceeded on {service}',
            'disk': f'Disk space critical on {service}',
            'response_time': f'Slow response time from {service}',
            'error_rate': f'Elevated error rate on {service}'
        }
        
        incidents.append({
            'id': i + 1,
            'service_name': service,
            'metric_name': metric,
            'metric_value': round(random.uniform(80, 100), 2),
            'title': title_templates.get(metric, f'Issue detected on {service}'),
            'severity': severity,
            'status': status,
            'created_at': created_time.isoformat(),
            'resolved_at': (created_time + timedelta(minutes=random.randint(10, 120))).isoformat() if status in ['resolved', 'closed'] else None,
            'auto_recovered': random.choice([True, False]) if status in ['resolved', 'closed'] else False
        })
    
    return incidents


def generate_recovery_logs(count=10):
    """Generate sample recovery action logs"""
    actions = [
        'restart_service',
        'clear_cache',
        'scale_up_instances',
        'kill_zombie_processes',
        'flush_connections',
        'reset_circuit_breaker'
    ]
    
    logs = []
    
    for i in range(count):
        timestamp = datetime.now() - timedelta(minutes=random.randint(5, 1440))
        success = random.choice([True, True, True, False])  # 75% success rate
        
        logs.append({
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'incident_id': random.randint(1, 20),
            'action': random.choice(actions),
            'success': success,
            'details': 'Successfully executed recovery action' if success else 'Recovery action failed - manual intervention required'
        })
    
    return sorted(logs, key=lambda x: x['timestamp'], reverse=True)


def generate_user_data():
    """Generate sample user management data"""
    users = [
        {
            'name': 'John Smith',
            'email': 'john.smith@company.com',
            'role': 'Admin',
            'status': 'active',
            'last_login': '2024-02-06 14:30'
        },
        {
            'name': 'Sarah Johnson',
            'email': 'sarah.j@company.com',
            'role': 'DevOps',
            'status': 'active',
            'last_login': '2024-02-06 16:15'
        },
        {
            'name': 'Mike Chen',
            'email': 'mike.chen@company.com',
            'role': 'Developer',
            'status': 'active',
            'last_login': '2024-02-06 09:45'
        },
        {
            'name': 'Emily Davis',
            'email': 'emily.d@company.com',
            'role': 'DevOps',
            'status': 'active',
            'last_login': '2024-02-05 18:20'
        },
        {
            'name': 'Robert Taylor',
            'email': 'robert.t@company.com',
            'role': 'Viewer',
            'status': 'inactive',
            'last_login': '2024-01-28 11:00'
        }
    ]
    
    return users


def generate_system_metrics():
    """Generate current system metrics"""
    return {
        'cpu': {
            'current': random.randint(35, 75),
            'trend': random.choice(['+2', '-3', '+1', '-2']),
            'threshold': 80
        },
        'memory': {
            'current': random.randint(50, 85),
            'trend': random.choice(['+3', '-2', '+1', '0']),
            'threshold': 90
        },
        'disk': {
            'current': random.randint(30, 65),
            'trend': random.choice(['+1', '+2', '0', '-1']),
            'threshold': 85
        },
        'response_time': {
            'current': random.randint(180, 450),
            'unit': 'ms',
            'trend': random.choice(['-20', '-15', '+10', '+5']),
            'threshold': 500
        }
    }


def generate_billing_info():
    """Generate billing and subscription data"""
    return {
        'plan': 'Enterprise',
        'status': 'Active',
        'billing_cycle': 'Monthly',
        'next_billing_date': '2024-03-01',
        'current_usage': {
            'incidents_tracked': 1247,
            'api_calls': 45890,
            'storage_gb': 12.5,
            'users': 5
        },
        'plan_limits': {
            'incidents_tracked': 5000,
            'api_calls': 100000,
            'storage_gb': 50,
            'users': 10
        },
        'costs': {
            'base_plan': 299,
            'additional_users': 0,
            'overage_charges': 0,
            'total': 299
        }
    }


def generate_auto_healing_config():
    """Generate auto-healing configuration"""
    return {
        'enabled': True,
        'rules': [
            {
                'name': 'High CPU Recovery',
                'condition': 'cpu > 85%',
                'action': 'restart_service',
                'enabled': True,
                'success_rate': 92
            },
            {
                'name': 'Memory Leak Fix',
                'condition': 'memory > 90%',
                'action': 'clear_cache + restart',
                'enabled': True,
                'success_rate': 87
            },
            {
                'name': 'Database Connection Pool',
                'condition': 'db_connections > 95%',
                'action': 'flush_connections',
                'enabled': True,
                'success_rate': 95
            },
            {
                'name': 'Response Time Degradation',
                'condition': 'response_time > 5000ms',
                'action': 'scale_up_instances',
                'enabled': False,
                'success_rate': 78
            }
        ]
    }


def generate_notification_settings():
    """Generate notification settings"""
    return {
        'email_alerts': True,
        'slack_integration': False,
        'pagerduty_integration': False,
        'alert_frequency': 'Immediate',
        'severity_threshold': 'medium',
        'quiet_hours': {
            'enabled': False,
            'start': '22:00',
            'end': '08:00'
        }
    }
