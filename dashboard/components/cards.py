"""
KPI Cards Component
Glass-morphism metric cards with hover effects
"""
import streamlit as st
from dashboard.config import COLORS, KPI_METRICS


def render_kpi_cards(metrics_data):
    """
    Render KPI cards with glassmorphism design
    
    Args:
        metrics_data: Dictionary with metric values
    """
    cols = st.columns(4)
    
    # System Health
    with cols[0]:
        health_score = metrics_data.get('system_health', 95)
        trend = metrics_data.get('health_trend', '+2')
        trend_color = 'var(--success-color)' if '+' in str(trend) else 'var(--danger-color)'
        
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">💚</div>
            <div class="kpi-label">System Health</div>
            <div class="kpi-value">{health_score}%</div>
            <div class="kpi-trend" style="color: {trend_color};">
                {'▲' if '+' in str(trend) else '▼'} {trend}% vs last week
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Failure Risk
    with cols[1]:
        risk_score = metrics_data.get('failure_risk', 12)
        trend = metrics_data.get('risk_trend', '-3')
        trend_color = 'var(--success-color)' if '-' in str(trend) else 'var(--danger-color)'
        
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">⚠️</div>
            <div class="kpi-label">Failure Risk</div>
            <div class="kpi-value">{risk_score}%</div>
            <div class="kpi-trend" style="color: {trend_color};">
                {'▼' if '-' in str(trend) else '▲'} {trend}% vs last week
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Active Incidents
    with cols[2]:
        incidents = metrics_data.get('active_incidents', 3)
        trend = metrics_data.get('incidents_trend', '-2')
        trend_color = 'var(--success-color)' if '-' in str(trend) else 'var(--danger-color)'
        
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🚨</div>
            <div class="kpi-label">Active Incidents</div>
            <div class="kpi-value">{incidents}</div>
            <div class="kpi-trend" style="color: {trend_color};">
                {'▼' if '-' in str(trend) else '▲'} {trend} vs yesterday
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Monthly Cost
    with cols[3]:
        cost = metrics_data.get('monthly_cost', 4250)
        trend = metrics_data.get('cost_trend', '+5')
        trend_color = 'var(--danger-color)' if '+' in str(trend) else 'var(--success-color)'
        
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Monthly Cost</div>
            <div class="kpi-value">${cost:,}</div>
            <div class="kpi-trend" style="color: {trend_color};">
                {'▲' if '+' in str(trend) else '▼'} {trend}% vs last month
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_metric_card(title, value, delta=None, icon="📊", color="primary"):
    """
    Render a single metric card
    
    Args:
        title: Card title
        value: Metric value
        delta: Optional change indicator
        icon: Card icon
        color: Color theme
    """
    delta_html = ""
    if delta:
        delta_color = 'var(--success-color)' if '+' in str(delta) or delta > 0 else 'var(--danger-color)'
        delta_arrow = '▲' if ('+' in str(delta) or delta > 0) else '▼'
        delta_html = f'<div class="kpi-trend" style="color: {delta_color};">{delta_arrow} {delta}</div>'
    
    st.markdown(f"""
    <div class="glass-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{title}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def render_status_card(title, status, description, icon="ℹ️"):
    """
    Render a status information card
    
    Args:
        title: Card title
        status: Status indicator (success, warning, danger, info)
        description: Card description
        icon: Card icon
    """
    status_colors = {
        'success': 'var(--success-color)',
        'warning': 'var(--warning-color)',
        'danger': 'var(--danger-color)',
        'info': 'var(--info-color)'
    }
    
    status_icons = {
        'success': '✅',
        'warning': '⚠️',
        'danger': '🔴',
        'info': 'ℹ️'
    }
    
    color = status_colors.get(status, 'var(--info-color)')
    status_icon = status_icons.get(status, 'ℹ️')
    
    st.markdown(f"""
    <div class="glass-card" style="border-left: 4px solid {color};">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
            <div class="kpi-icon" style="font-size: 1.5rem;">{icon}</div>
            <div style="flex: 1;">
                <div class="kpi-label">{title}</div>
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-top: 0.25rem;">
                    <span>{status_icon}</span>
                    <span style="color: {color}; font-weight: 600; text-transform: uppercase; font-size: 0.85rem;">{status}</span>
                </div>
            </div>
        </div>
        <div style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.5rem;">
            {description}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_mini_stat(label, value, icon="📊"):
    """Render a compact stat display"""
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem; background: var(--card-bg); border-radius: 8px; border: 1px solid var(--border-color);">
        <div style="font-size: 1.5rem;">{icon}</div>
        <div style="flex: 1;">
            <div style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase;">{label}</div>
            <div style="font-size: 1.25rem; font-weight: 700; color: var(--text-primary);">{value}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
