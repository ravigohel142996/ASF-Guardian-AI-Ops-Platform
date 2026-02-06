"""
Monitoring UI Components
Reusable components for the dashboard
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd


def show_metric_card(label: str, value: any, delta: str = None, color: str = "blue"):
    """
    Display a metric card
    
    Args:
        label: Metric label
        value: Metric value
        delta: Optional delta/change value
        color: Card color theme
    """
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.metric(label=label, value=value, delta=delta)


def show_severity_badge(severity: str):
    """Show severity badge with appropriate color"""
    colors = {
        'critical': '🔴',
        'high': '🟠',
        'medium': '🟡',
        'low': '🟢'
    }
    
    emoji = colors.get(severity.lower(), '⚪')
    return f"{emoji} {severity.upper()}"


def show_status_badge(status: str):
    """Show status badge with appropriate color"""
    colors = {
        'open': '🔴',
        'investigating': '🟡',
        'resolved': '🟢',
        'closed': '⚪'
    }
    
    emoji = colors.get(status.lower(), '⚪')
    return f"{emoji} {status.title()}"


def create_incidents_timeline(incidents: list):
    """
    Create timeline chart for incidents
    
    Args:
        incidents: List of incidents
        
    Returns:
        Plotly figure
    """
    if not incidents:
        return None
    
    df = pd.DataFrame(incidents)
    df['detected_at'] = pd.to_datetime(df['detected_at'])
    
    # Count incidents by hour
    df['hour'] = df['detected_at'].dt.floor('H')
    incident_counts = df.groupby('hour').size().reset_index(name='count')
    
    fig = px.line(
        incident_counts,
        x='hour',
        y='count',
        title='Incidents Timeline',
        labels={'hour': 'Time', 'count': 'Number of Incidents'}
    )
    
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Incidents",
        hovermode='x unified'
    )
    
    return fig


def create_severity_distribution(incidents: list):
    """
    Create pie chart for severity distribution
    
    Args:
        incidents: List of incidents
        
    Returns:
        Plotly figure
    """
    if not incidents:
        return None
    
    df = pd.DataFrame(incidents)
    severity_counts = df['severity'].value_counts()
    
    colors = {
        'critical': '#dc3545',
        'high': '#fd7e14',
        'medium': '#ffc107',
        'low': '#28a745'
    }
    
    color_list = [colors.get(sev, '#6c757d') for sev in severity_counts.index]
    
    fig = go.Figure(data=[go.Pie(
        labels=severity_counts.index,
        values=severity_counts.values,
        marker=dict(colors=color_list),
        hole=0.4
    )])
    
    fig.update_layout(
        title='Incidents by Severity',
        showlegend=True
    )
    
    return fig


def create_service_health_gauge(services: list):
    """
    Create gauge charts for service health
    
    Args:
        services: List of service metrics
        
    Returns:
        List of Plotly figures
    """
    figures = []
    
    for service in services:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=service.get('health_score', 0),
            title={'text': service.get('name', 'Unknown')},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 75], 'color': "yellow"},
                    {'range': [75, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=250)
        figures.append(fig)
    
    return figures


def create_recovery_stats_chart(stats: dict):
    """
    Create bar chart for recovery statistics
    
    Args:
        stats: Recovery statistics
        
    Returns:
        Plotly figure
    """
    data = {
        'Status': ['Successful', 'Failed'],
        'Count': [
            stats.get('successful', 0),
            stats.get('failed', 0)
        ]
    }
    
    df = pd.DataFrame(data)
    
    fig = px.bar(
        df,
        x='Status',
        y='Count',
        title='Recovery Actions',
        color='Status',
        color_discrete_map={
            'Successful': '#28a745',
            'Failed': '#dc3545'
        }
    )
    
    fig.update_layout(showlegend=False)
    
    return fig


def show_incident_table(incidents: list):
    """
    Display incidents in a formatted table
    
    Args:
        incidents: List of incidents
    """
    if not incidents:
        st.info("No incidents to display")
        return
    
    for incident in incidents:
        with st.expander(
            f"{show_severity_badge(incident['severity'])} {incident['title']} - "
            f"{show_status_badge(incident['status'])}"
        ):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**ID:** #{incident['id']}")
                st.write(f"**Service:** {incident['service_name']}")
                st.write(f"**Detected:** {incident['detected_at']}")
            
            with col2:
                st.write(f"**Severity:** {incident['severity']}")
                st.write(f"**Status:** {incident['status']}")
                if incident.get('auto_recovered'):
                    st.success("✅ Auto-recovered")
            
            st.write(f"**Description:** {incident['description']}")
            
            if incident.get('recovery_action'):
                st.info(f"**Recovery Action:** {incident['recovery_action']}")


def show_system_metrics(metrics: dict):
    """
    Display system metrics with progress bars
    
    Args:
        metrics: Dictionary of metric values
    """
    st.subheader("📊 System Metrics")
    
    for metric_name, value in metrics.items():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Determine color based on value
            if value >= 80:
                color = "🔴"
            elif value >= 60:
                color = "🟡"
            else:
                color = "🟢"
            
            st.write(f"{color} **{metric_name.upper()}**")
            st.progress(min(value / 100, 1.0))
        
        with col2:
            st.metric("", f"{value:.1f}%")


def create_mttr_chart(incidents: list):
    """
    Create Mean Time To Recovery chart
    
    Args:
        incidents: List of incidents with resolution times
        
    Returns:
        Plotly figure
    """
    resolved_incidents = [
        inc for inc in incidents
        if inc.get('resolved_at') and inc.get('detected_at')
    ]
    
    if not resolved_incidents:
        return None
    
    mttr_data = []
    for inc in resolved_incidents:
        detected = datetime.fromisoformat(inc['detected_at'].replace('Z', '+00:00'))
        resolved = datetime.fromisoformat(inc['resolved_at'].replace('Z', '+00:00'))
        recovery_time = (resolved - detected).total_seconds() / 60  # minutes
        
        mttr_data.append({
            'incident_id': inc['id'],
            'service': inc['service_name'],
            'recovery_time': recovery_time,
            'auto_recovered': inc.get('auto_recovered', False)
        })
    
    df = pd.DataFrame(mttr_data)
    
    fig = px.bar(
        df,
        x='incident_id',
        y='recovery_time',
        color='auto_recovered',
        title='Mean Time To Recovery (MTTR)',
        labels={
            'incident_id': 'Incident ID',
            'recovery_time': 'Recovery Time (minutes)',
            'auto_recovered': 'Auto-Recovered'
        },
        color_discrete_map={True: '#28a745', False: '#ffc107'}
    )
    
    return fig


def show_alert_settings():
    """Display alert configuration settings"""
    st.subheader("⚙️ Alert Settings")
    
    with st.form("alert_settings"):
        st.write("Configure threshold values for alerts:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cpu_threshold = st.slider("CPU Threshold (%)", 0, 100, 80)
            memory_threshold = st.slider("Memory Threshold (%)", 0, 100, 85)
        
        with col2:
            disk_threshold = st.slider("Disk Threshold (%)", 0, 100, 90)
            response_threshold = st.slider("Response Time (ms)", 0, 10000, 5000)
        
        email_alerts = st.checkbox("Enable Email Alerts", value=True)
        auto_recovery = st.checkbox("Enable Auto-Recovery", value=True)
        
        submitted = st.form_submit_button("Save Settings")
        
        if submitted:
            st.success("✅ Settings saved successfully!")
            return {
                'cpu': cpu_threshold,
                'memory': memory_threshold,
                'disk': disk_threshold,
                'response_time': response_threshold,
                'email_alerts': email_alerts,
                'auto_recovery': auto_recovery
            }
    
    return None
