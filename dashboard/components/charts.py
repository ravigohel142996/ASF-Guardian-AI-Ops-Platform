"""
Charts Component
Professional Plotly charts with dark theme
"""
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
from dashboard.config import COLORS, CHART_COLORS, CHART_CONFIG
import random


def get_chart_layout(title=""):
    """Get standard chart layout with dark theme"""
    return {
        'template': 'plotly_dark',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'title': {
            'text': title,
            'font': {
                'size': 18,
                'color': COLORS['text_primary'],
                'family': CHART_CONFIG['font_family']
            }
        },
        'font': {
            'family': CHART_CONFIG['font_family'],
            'size': CHART_CONFIG['font_size'],
            'color': COLORS['text_secondary']
        },
        'xaxis': {
            'gridcolor': COLORS['border'],
            'showgrid': True,
            'zeroline': False
        },
        'yaxis': {
            'gridcolor': COLORS['border'],
            'showgrid': True,
            'zeroline': False
        },
        'margin': CHART_CONFIG['margin'],
        'height': CHART_CONFIG['height']
    }


def create_health_risk_chart():
    """Create line chart showing Health vs Risk over time"""
    # Generate sample data
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    
    health = [95 - i * 0.5 + random.randint(-3, 3) for i in range(30)]
    risk = [10 + i * 0.3 + random.randint(-2, 2) for i in range(30)]
    
    fig = go.Figure()
    
    # Health line
    fig.add_trace(go.Scatter(
        x=dates,
        y=health,
        name='System Health',
        line=dict(color=CHART_COLORS['health'], width=3),
        fill='tonexty',
        fillcolor=f"rgba(76, 175, 80, 0.1)"
    ))
    
    # Risk line
    fig.add_trace(go.Scatter(
        x=dates,
        y=risk,
        name='Failure Risk',
        line=dict(color=CHART_COLORS['risk'], width=3),
        fill='tozeroy',
        fillcolor=f"rgba(244, 67, 54, 0.1)"
    ))
    
    fig.update_layout(**get_chart_layout('System Health vs Failure Risk'))
    fig.update_layout(hovermode='x unified')
    
    return fig


def create_load_chart():
    """Create area chart showing system load"""
    # Generate sample data
    hours = pd.date_range(end=datetime.now(), periods=24, freq='H')
    
    cpu_load = [30 + i * 2 + random.randint(-5, 10) for i in range(24)]
    memory_load = [40 + i * 1.5 + random.randint(-5, 10) for i in range(24)]
    disk_load = [25 + i * 1 + random.randint(-3, 8) for i in range(24)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=hours,
        y=cpu_load,
        name='CPU Load',
        line=dict(color=CHART_COLORS['load'], width=2),
        stackgroup='one',
        fillcolor=f"rgba(33, 150, 243, 0.3)"
    ))
    
    fig.add_trace(go.Scatter(
        x=hours,
        y=memory_load,
        name='Memory Load',
        line=dict(color=CHART_COLORS['cost'], width=2),
        stackgroup='one',
        fillcolor=f"rgba(255, 152, 0, 0.3)"
    ))
    
    fig.add_trace(go.Scatter(
        x=hours,
        y=disk_load,
        name='Disk Load',
        line=dict(color=CHART_COLORS['health'], width=2),
        stackgroup='one',
        fillcolor=f"rgba(76, 175, 80, 0.3)"
    ))
    
    fig.update_layout(**get_chart_layout('System Load (Last 24 Hours)'))
    fig.update_layout(hovermode='x unified')
    
    return fig


def create_cost_chart():
    """Create bar chart showing monthly costs"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    compute = [2800, 3200, 3500, 3800, 4100, 4200]
    storage = [800, 850, 900, 950, 1000, 1050]
    network = [400, 420, 450, 480, 500, 520]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=months,
        y=compute,
        name='Compute',
        marker_color=CHART_COLORS['load']
    ))
    
    fig.add_trace(go.Bar(
        x=months,
        y=storage,
        name='Storage',
        marker_color=CHART_COLORS['cost']
    ))
    
    fig.add_trace(go.Bar(
        x=months,
        y=network,
        name='Network',
        marker_color=CHART_COLORS['health']
    ))
    
    fig.update_layout(**get_chart_layout('Monthly Costs by Category'))
    fig.update_layout(barmode='stack', hovermode='x unified')
    
    return fig


def create_incident_distribution_chart(incidents_data=None):
    """Create pie chart showing incident distribution by severity"""
    if not incidents_data:
        # Sample data
        severities = ['Critical', 'High', 'Medium', 'Low']
        counts = [5, 12, 23, 8]
    else:
        # Parse real data
        severities = []
        counts = []
        # Add logic to parse incidents_data
    
    colors = [CHART_COLORS['critical'], CHART_COLORS['high'], 
              CHART_COLORS['medium'], CHART_COLORS['low']]
    
    fig = go.Figure(data=[go.Pie(
        labels=severities,
        values=counts,
        hole=0.4,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textfont=dict(size=14)
    )])
    
    fig.update_layout(**get_chart_layout('Incidents by Severity'))
    fig.update_layout(showlegend=True, height=350)
    
    return fig


def create_recovery_success_chart():
    """Create gauge chart showing recovery success rate"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=87,
        delta={'reference': 80, 'increasing': {'color': CHART_COLORS['health']}},
        title={'text': "Auto-Recovery Success Rate", 'font': {'size': 18}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1},
            'bar': {'color': CHART_COLORS['health']},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': COLORS['border'],
            'steps': [
                {'range': [0, 50], 'color': 'rgba(244, 67, 54, 0.2)'},
                {'range': [50, 75], 'color': 'rgba(255, 152, 0, 0.2)'},
                {'range': [75, 100], 'color': 'rgba(76, 175, 80, 0.2)'}
            ],
            'threshold': {
                'line': {'color': COLORS['text_primary'], 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(**get_chart_layout())
    fig.update_layout(height=300)
    
    return fig


def create_mttr_trend_chart():
    """Create line chart showing Mean Time To Recovery trend"""
    weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
    mttr_values = [45, 38, 32, 28]  # in minutes
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=weeks,
        y=mttr_values,
        mode='lines+markers',
        line=dict(color=CHART_COLORS['load'], width=3),
        marker=dict(size=10, color=CHART_COLORS['load']),
        fill='tozeroy',
        fillcolor='rgba(33, 150, 243, 0.2)'
    ))
    
    fig.update_layout(**get_chart_layout('Mean Time To Recovery (MTTR) Trend'))
    fig.update_yaxes(title_text="Minutes")
    
    return fig


def create_service_health_heatmap():
    """Create heatmap showing service health over time"""
    services = ['web-api', 'database', 'cache', 'auth-service', 'payment']
    hours = list(range(24))
    
    # Generate sample health data
    health_data = []
    for service in services:
        row = [85 + random.randint(-15, 10) for _ in hours]
        health_data.append(row)
    
    fig = go.Figure(data=go.Heatmap(
        z=health_data,
        x=hours,
        y=services,
        colorscale=[
            [0, CHART_COLORS['critical']],
            [0.5, CHART_COLORS['medium']],
            [1, CHART_COLORS['health']]
        ],
        text=health_data,
        texttemplate='%{text}%',
        textfont={"size": 10},
        colorbar=dict(title="Health %")
    ))
    
    fig.update_layout(**get_chart_layout('Service Health Heatmap (Last 24 Hours)'))
    fig.update_xaxes(title_text="Hour of Day")
    fig.update_yaxes(title_text="Service")
    
    return fig


def create_incident_timeline_chart(incidents=None):
    """Create timeline chart showing incident occurrences"""
    if not incidents or len(incidents) == 0:
        # Sample data
        dates = pd.date_range(end=datetime.now(), periods=10, freq='H')
        incidents_count = [random.randint(0, 5) for _ in range(10)]
    else:
        # Parse real incidents data
        dates = []
        incidents_count = []
        # Add logic to parse incidents
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=dates,
        y=incidents_count,
        marker_color=CHART_COLORS['risk'],
        name='Incidents'
    ))
    
    fig.update_layout(**get_chart_layout('Incident Timeline'))
    fig.update_yaxes(title_text="Count")
    
    return fig
