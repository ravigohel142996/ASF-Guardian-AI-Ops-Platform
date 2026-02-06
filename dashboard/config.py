"""
Configuration file for ASF-Guardian Dashboard
Centralized settings and constants
"""

# Design System Colors
COLORS = {
    'primary': '#2196F3',
    'secondary': '#00BCD4',
    'accent': '#9C27B0',
    'success': '#4CAF50',
    'warning': '#FF9800',
    'danger': '#F44336',
    'info': '#2196F3',
    'background': '#0A1929',
    'background_secondary': '#1A2332',
    'card_background': 'rgba(255, 255, 255, 0.05)',
    'text_primary': '#FFFFFF',
    'text_secondary': '#B0BEC5',
    'border': 'rgba(255, 255, 255, 0.1)'
}

# Chart Colors
CHART_COLORS = {
    'health': '#4CAF50',
    'risk': '#F44336',
    'load': '#2196F3',
    'cost': '#FF9800',
    'critical': '#F44336',
    'high': '#FF9800',
    'medium': '#FFC107',
    'low': '#4CAF50'
}

# Severity Configuration
SEVERITY_CONFIG = {
    'critical': {
        'color': '#F44336',
        'icon': '🔴',
        'label': 'Critical'
    },
    'high': {
        'color': '#FF9800',
        'icon': '🟠',
        'label': 'High'
    },
    'medium': {
        'color': '#FFC107',
        'icon': '🟡',
        'label': 'Medium'
    },
    'low': {
        'color': '#4CAF50',
        'icon': '🟢',
        'label': 'Low'
    }
}

# Status Configuration
STATUS_CONFIG = {
    'open': {
        'color': '#F44336',
        'icon': '●',
        'label': 'Open'
    },
    'investigating': {
        'color': '#FF9800',
        'icon': '●',
        'label': 'Investigating'
    },
    'resolved': {
        'color': '#4CAF50',
        'icon': '●',
        'label': 'Resolved'
    },
    'closed': {
        'color': '#9E9E9E',
        'icon': '●',
        'label': 'Closed'
    }
}

# Thresholds
THRESHOLDS = {
    'cpu': {'warning': 70, 'critical': 85},
    'memory': {'warning': 75, 'critical': 90},
    'disk': {'warning': 80, 'critical': 95},
    'response_time': {'warning': 3000, 'critical': 5000},
    'error_rate': {'warning': 3, 'critical': 5}
}

# Application Settings
APP_CONFIG = {
    'name': 'ASF-Guardian',
    'version': '2.0.0',
    'company': 'ASF Technologies',
    'tagline': 'Enterprise AI Ops Platform',
    'support_email': 'support@asf-guardian.com'
}

# Chart Configuration
CHART_CONFIG = {
    'height': 400,
    'margin': {'l': 50, 'r': 50, 't': 50, 'b': 50},
    'font_family': 'Inter, system-ui, sans-serif',
    'font_size': 12,
    'font_color': COLORS['text_secondary']
}

# KPI Metrics
KPI_METRICS = [
    {
        'id': 'system_health',
        'label': 'System Health',
        'icon': '💚',
        'format': 'percentage'
    },
    {
        'id': 'failure_risk',
        'label': 'Failure Risk',
        'icon': '⚠️',
        'format': 'percentage'
    },
    {
        'id': 'active_incidents',
        'label': 'Active Incidents',
        'icon': '🚨',
        'format': 'number'
    },
    {
        'id': 'monthly_cost',
        'label': 'Monthly Cost',
        'icon': '💰',
        'format': 'currency'
    }
]
