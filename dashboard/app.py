"""
ASF-Guardian Enterprise Dashboard
Professional AI Ops Platform UI
Version 2.0.0
"""
import streamlit as st
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Import components
from dashboard.components.navbar import render_navbar, render_sidebar, render_user_menu, render_notifications
from dashboard.components.cards import render_kpi_cards, render_status_card, render_mini_stat
from dashboard.components.charts import (
    create_health_risk_chart, create_load_chart, create_cost_chart,
    create_incident_distribution_chart, create_recovery_success_chart,
    create_mttr_trend_chart, create_service_health_heatmap, create_incident_timeline_chart
)
from dashboard.components.tables import (
    render_incident_table, render_user_table, render_recovery_logs_table,
    render_filter_bar, render_searchable_table
)
from dashboard.components.ai_panel import (
    render_ai_chat_interface, render_recommendation_cards,
    render_quick_insights, render_ai_analysis_panel
)
from dashboard.sample_data import (
    generate_kpi_metrics, generate_sample_incidents, generate_recovery_logs,
    generate_user_data, generate_system_metrics, generate_billing_info,
    generate_auto_healing_config, generate_notification_settings
)
from dashboard.config import APP_CONFIG, COLORS

# Page configuration
st.set_page_config(
    page_title=f"{APP_CONFIG['name']} - {APP_CONFIG['tagline']}",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_path = Path(__file__).parent / "styles.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if 'demo_mode' not in st.session_state:
    st.session_state.demo_mode = True

# Render navbar
render_navbar()

# Render sidebar and get selected page
selected_page = render_sidebar()

# Render notifications and user menu
render_notifications()
render_user_menu()


# ==================== DASHBOARD PAGE ====================
if selected_page == "dashboard":
    st.markdown('<div class="section-header">📊 Dashboard Overview</div>', unsafe_allow_html=True)
    
    # KPI Cards
    kpi_data = generate_kpi_metrics()
    render_kpi_cards(kpi_data)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Insights
    render_quick_insights()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent Activity
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-subheader">🚨 Recent Incidents</div>', unsafe_allow_html=True)
        incidents = generate_sample_incidents(10)
        render_incident_table(incidents[:5], show_actions=False)
    
    with col2:
        st.markdown('<div class="section-subheader">📊 Severity Distribution</div>', unsafe_allow_html=True)
        fig = create_incident_distribution_chart()
        st.plotly_chart(fig, use_container_width=True)


# ==================== SYSTEM OVERVIEW PAGE ====================
elif selected_page == "system_overview":
    st.markdown('<div class="section-header">📊 System Overview</div>', unsafe_allow_html=True)
    
    # System Metrics
    metrics = generate_system_metrics()
    
    cols = st.columns(4)
    with cols[0]:
        render_mini_stat("CPU Usage", f"{metrics['cpu']['current']}%", "🖥️")
    with cols[1]:
        render_mini_stat("Memory Usage", f"{metrics['memory']['current']}%", "💾")
    with cols[2]:
        render_mini_stat("Disk Usage", f"{metrics['disk']['current']}%", "💿")
    with cols[3]:
        render_mini_stat("Response Time", f"{metrics['response_time']['current']}ms", "⚡")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = create_health_risk_chart()
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = create_load_chart()
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = create_cost_chart()
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = create_recovery_success_chart()
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Service Health Heatmap
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = create_service_health_heatmap()
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ==================== INCIDENT MANAGEMENT PAGE ====================
elif selected_page == "incidents":
    st.markdown('<div class="section-header">🚨 Incident Management</div>', unsafe_allow_html=True)
    
    # Filters
    filters = render_filter_bar()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Generate and filter incidents
    incidents = generate_sample_incidents(25)
    
    # Apply filters
    if filters['severity']:
        incidents = [i for i in incidents if i['severity'] in filters['severity']]
    if filters['status']:
        incidents = [i for i in incidents if i['status'] in filters['status']]
    if filters['service']:
        incidents = [i for i in incidents if i['service_name'] in filters['service']]
    
    # Stats cards
    cols = st.columns(4)
    with cols[0]:
        open_count = len([i for i in incidents if i['status'] == 'open'])
        render_status_card('Open Incidents', 'danger' if open_count > 5 else 'warning', f'{open_count} incidents require attention', '🚨')
    with cols[1]:
        critical_count = len([i for i in incidents if i['severity'] == 'critical'])
        render_status_card('Critical Issues', 'danger' if critical_count > 0 else 'success', f'{critical_count} critical incidents', '🔴')
    with cols[2]:
        resolved_count = len([i for i in incidents if i['status'] == 'resolved'])
        render_status_card('Resolved Today', 'success', f'{resolved_count} incidents resolved', '✅')
    with cols[3]:
        auto_recovered = len([i for i in incidents if i.get('auto_recovered')])
        render_status_card('Auto-Recovered', 'success', f'{auto_recovered} automated fixes', '🤖')
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Incidents table
    st.markdown('<div class="section-subheader">📋 All Incidents</div>', unsafe_allow_html=True)
    render_incident_table(incidents)
    
    # Timeline chart
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = create_incident_timeline_chart(incidents)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ==================== AI ADVISOR PAGE ====================
elif selected_page == "ai_advisor":
    st.markdown('<div class="section-header">🤖 AI-Powered Advisor</div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["💬 Chat", "💡 Recommendations", "🔍 Analysis"])
    
    with tabs[0]:
        render_ai_chat_interface()
    
    with tabs[1]:
        render_recommendation_cards()
    
    with tabs[2]:
        st.markdown('<div class="section-subheader">🔍 Incident Analysis</div>', unsafe_allow_html=True)
        
        # Incident selector
        incidents = generate_sample_incidents(10)
        incident_options = {f"#{i['id']} - {i['title']}": i['id'] for i in incidents}
        
        selected = st.selectbox("Select Incident to Analyze", list(incident_options.keys()))
        
        if selected:
            incident_id = incident_options[selected]
            render_ai_analysis_panel(incident_id)


# ==================== AUTO-HEALING PAGE ====================
elif selected_page == "auto_healing":
    st.markdown('<div class="section-header">⚙️ Auto-Healing Configuration</div>', unsafe_allow_html=True)
    
    config = generate_auto_healing_config()
    
    # Status card
    status = 'success' if config['enabled'] else 'warning'
    render_status_card(
        'Auto-Healing System',
        status,
        'System is actively monitoring and recovering from incidents' if config['enabled'] else 'Auto-healing is currently disabled',
        '⚙️'
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recovery Rules
    st.markdown('<div class="section-subheader">🔧 Recovery Rules</div>', unsafe_allow_html=True)
    
    for rule in config['rules']:
        enabled_badge = '<span class="badge badge-resolved">ENABLED</span>' if rule['enabled'] else '<span class="badge badge-closed">DISABLED</span>'
        
        st.markdown(f"""
        <div class="glass-card" style="margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div style="flex: 1;">
                    <h4 style="margin: 0; color: var(--text-primary);">{rule['name']}</h4>
                    <div style="margin-top: 0.5rem;">
                        {enabled_badge}
                        <span style="margin-left: 1rem; color: var(--text-secondary);">Success Rate: <strong>{rule['success_rate']}%</strong></span>
                    </div>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div>
                    <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 0.25rem;">CONDITION</div>
                    <code style="color: var(--primary-color);">{rule['condition']}</code>
                </div>
                <div>
                    <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 0.25rem;">ACTION</div>
                    <code style="color: var(--accent-color);">{rule['action']}</code>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recovery Logs
    st.markdown('<div class="section-subheader">📜 Recent Recovery Actions</div>', unsafe_allow_html=True)
    logs = generate_recovery_logs(10)
    render_recovery_logs_table(logs)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # MTTR Chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = create_mttr_trend_chart()
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ==================== ADMIN PANEL PAGE ====================
elif selected_page == "admin":
    st.markdown('<div class="section-header">👥 Admin Panel</div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["👥 Users", "💳 Billing", "🔔 Notifications"])
    
    with tabs[0]:
        st.markdown('<div class="section-subheader">User Management</div>', unsafe_allow_html=True)
        
        # Add user button
        if st.button("➕ Add New User", key="add_user"):
            st.info("Add user functionality would open a modal here")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Users table
        users = generate_user_data()
        render_user_table(users)
    
    with tabs[1]:
        st.markdown('<div class="section-subheader">💳 Billing & Subscription</div>', unsafe_allow_html=True)
        
        billing = generate_billing_info()
        
        # Plan info
        cols = st.columns(3)
        with cols[0]:
            render_status_card('Current Plan', 'success', billing['plan'], '📦')
        with cols[1]:
            render_status_card('Status', 'success', billing['status'], '✅')
        with cols[2]:
            render_status_card('Next Billing', 'info', billing['next_billing_date'], '📅')
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Usage vs Limits
        st.markdown('<div class="section-subheader">📊 Usage & Limits</div>', unsafe_allow_html=True)
        
        usage_items = [
            ('Incidents Tracked', billing['current_usage']['incidents_tracked'], billing['plan_limits']['incidents_tracked']),
            ('API Calls', billing['current_usage']['api_calls'], billing['plan_limits']['api_calls']),
            ('Storage (GB)', billing['current_usage']['storage_gb'], billing['plan_limits']['storage_gb']),
            ('Users', billing['current_usage']['users'], billing['plan_limits']['users'])
        ]
        
        for label, current, limit in usage_items:
            percentage = (current / limit) * 100
            st.markdown(f"""
            <div class="glass-card" style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span style="color: var(--text-secondary);">{label}</span>
                    <span style="color: var(--text-primary); font-weight: 600;">{current:,} / {limit:,}</span>
                </div>
                <div style="background: var(--border-color); height: 8px; border-radius: 4px; overflow: hidden;">
                    <div style="width: {percentage}%; height: 100%; background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Cost breakdown
        st.markdown('<div class="section-subheader">💰 Cost Breakdown</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid var(--border-color);">
                <span>Base Plan</span>
                <span style="font-weight: 600;">${billing['costs']['base_plan']}</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid var(--border-color);">
                <span>Additional Users</span>
                <span style="font-weight: 600;">${billing['costs']['additional_users']}</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 0.75rem 0; border-bottom: 1px solid var(--border-color);">
                <span>Overage Charges</span>
                <span style="font-weight: 600;">${billing['costs']['overage_charges']}</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 1rem 0 0.5rem 0; font-size: 1.25rem;">
                <span style="font-weight: 700; color: var(--text-primary);">Total</span>
                <span style="font-weight: 700; color: var(--primary-color);">${billing['costs']['total']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown('<div class="section-subheader">🔔 Notification Settings</div>', unsafe_allow_html=True)
        
        settings = generate_notification_settings()
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # Email alerts
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Email Alerts**")
            st.markdown('<small style="color: var(--text-secondary);">Receive email notifications for incidents</small>', unsafe_allow_html=True)
        with col2:
            st.toggle("Enable", value=settings['email_alerts'], key="email_alerts")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Slack integration
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Slack Integration**")
            st.markdown('<small style="color: var(--text-secondary);">Send alerts to Slack channels</small>', unsafe_allow_html=True)
        with col2:
            st.toggle("Enable", value=settings['slack_integration'], key="slack")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # PagerDuty integration
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**PagerDuty Integration**")
            st.markdown('<small style="color: var(--text-secondary);">Create PagerDuty incidents</small>', unsafe_allow_html=True)
        with col2:
            st.toggle("Enable", value=settings['pagerduty_integration'], key="pagerduty")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Alert configuration
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        st.selectbox("Alert Frequency", ["Immediate", "Every 5 minutes", "Every 15 minutes", "Hourly"], key="freq")
        st.selectbox("Severity Threshold", ["All", "Low and above", "Medium and above", "High and above", "Critical only"], key="severity_threshold")
        
        st.markdown('</div>', unsafe_allow_html=True)


# ==================== SETTINGS PAGE ====================
elif selected_page == "settings":
    st.markdown('<div class="section-header">⚙️ Settings</div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["🔧 General", "🔒 Security", "🔗 Integrations"])
    
    with tabs[0]:
        st.markdown('<div class="section-subheader">General Settings</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.text_input("Company Name", value=APP_CONFIG['company'])
        st.text_input("Support Email", value=APP_CONFIG['support_email'])
        st.selectbox("Timezone", ["UTC", "America/New_York", "America/Los_Angeles", "Europe/London", "Asia/Tokyo"])
        st.selectbox("Date Format", ["YYYY-MM-DD", "MM/DD/YYYY", "DD/MM/YYYY"])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown('<div class="section-subheader">Security Settings</div>', unsafe_allow_html=True)
        
        render_status_card('Security Status', 'success', 'All security features are enabled', '🔒')
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.toggle("Two-Factor Authentication", value=True)
        st.toggle("Session Timeout (30 minutes)", value=True)
        st.toggle("IP Whitelisting", value=False)
        st.toggle("Audit Logging", value=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown('<div class="section-subheader">Integration Settings</div>', unsafe_allow_html=True)
        
        integrations = [
            {"name": "Slack", "status": "Connected", "icon": "💬"},
            {"name": "PagerDuty", "status": "Not Connected", "icon": "📟"},
            {"name": "Datadog", "status": "Connected", "icon": "📊"},
            {"name": "Grafana", "status": "Not Connected", "icon": "📈"}
        ]
        
        for integration in integrations:
            status_badge = '<span class="badge badge-resolved">Connected</span>' if integration['status'] == 'Connected' else '<span class="badge badge-closed">Not Connected</span>'
            
            st.markdown(f"""
            <div class="glass-card" style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div style="font-size: 2rem;">{integration['icon']}</div>
                        <div>
                            <div style="font-weight: 600; color: var(--text-primary);">{integration['name']}</div>
                            <div style="margin-top: 0.25rem;">{status_badge}</div>
                        </div>
                    </div>
                    <button class="btn btn-secondary" style="padding: 0.5rem 1.5rem;">
                        {"Configure" if integration['status'] == 'Connected' else "Connect"}
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ==================== FOOTER ====================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
<div class="dashboard-footer">
    <div class="footer-content">
        <div class="footer-section">
            <div class="footer-title">{APP_CONFIG['name']}</div>
            <div class="footer-text">Version {APP_CONFIG['version']}</div>
            <div class="footer-text">{APP_CONFIG['company']}</div>
        </div>
        <div class="footer-section">
            <div class="footer-title">Support</div>
            <div class="footer-text">{APP_CONFIG['support_email']}</div>
            <div class="footer-text">24/7 Support Available</div>
        </div>
        <div class="footer-section">
            <div class="footer-title">Security</div>
            <div class="footer-text">🔒 SOC 2 Compliant</div>
            <div class="footer-text">🛡️ ISO 27001 Certified</div>
        </div>
        <div class="footer-section">
            <div class="footer-title">Links</div>
            <div class="footer-text"><a href="#" style="color: var(--primary-color);">Documentation</a></div>
            <div class="footer-text"><a href="#" style="color: var(--primary-color);">API Reference</a></div>
        </div>
    </div>
    <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--border-color); text-align: center; color: var(--text-secondary);">
        © 2024 {APP_CONFIG['company']}. All rights reserved. | Built with Streamlit & FastAPI
    </div>
</div>
""", unsafe_allow_html=True)
