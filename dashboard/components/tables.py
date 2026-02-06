"""
Tables Component
Professional data tables with filters and badges
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from dashboard.config import SEVERITY_CONFIG, STATUS_CONFIG


def render_severity_badge(severity):
    """Render severity badge with color and icon"""
    config = SEVERITY_CONFIG.get(severity.lower(), SEVERITY_CONFIG['low'])
    return f"""
    <span class="badge badge-{severity.lower()}">
        {config['icon']} {config['label']}
    </span>
    """


def render_status_badge(status):
    """Render status badge with color and icon"""
    config = STATUS_CONFIG.get(status.lower(), STATUS_CONFIG['closed'])
    return f"""
    <span class="badge badge-{status.lower()}">
        {config['icon']} {config['label']}
    </span>
    """


def render_incident_table(incidents, show_actions=True):
    """
    Render incidents table with filters and actions
    
    Args:
        incidents: List of incident dictionaries
        show_actions: Whether to show action buttons
    """
    if not incidents or len(incidents) == 0:
        st.info("No incidents found")
        return
    
    # Build table HTML
    table_html = """
    <div class="dataframe-container">
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Service</th>
                    <th>Issue</th>
                    <th>Severity</th>
                    <th>Status</th>
                    <th>Created</th>
                    <th>Duration</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for incident in incidents:
        incident_id = incident.get('id', 'N/A')
        service = incident.get('service_name', 'Unknown')
        title = incident.get('title', 'No title')
        severity = incident.get('severity', 'low')
        status = incident.get('status', 'open')
        
        # Format created time
        created = incident.get('created_at', '')
        if created:
            try:
                if isinstance(created, str):
                    created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                else:
                    created_dt = created
                created_str = created_dt.strftime('%Y-%m-%d %H:%M')
                
                # Calculate duration
                duration = datetime.now() - created_dt.replace(tzinfo=None)
                hours = int(duration.total_seconds() / 3600)
                minutes = int((duration.total_seconds() % 3600) / 60)
                duration_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
            except (ValueError, TypeError, AttributeError):
                created_str = str(created)[:16]
                duration_str = "N/A"
        else:
            created_str = "N/A"
            duration_str = "N/A"
        
        severity_badge = render_severity_badge(severity)
        status_badge = render_status_badge(status)
        
        table_html += f"""
            <tr>
                <td><strong>#{incident_id}</strong></td>
                <td><code>{service}</code></td>
                <td>{title}</td>
                <td>{severity_badge}</td>
                <td>{status_badge}</td>
                <td>{created_str}</td>
                <td>{duration_str}</td>
            </tr>
        """
    
    table_html += """
            </tbody>
        </table>
    </div>
    """
    
    st.markdown(table_html, unsafe_allow_html=True)


def render_searchable_table(data, columns, search_key="search"):
    """
    Render a searchable data table
    
    Args:
        data: List of dictionaries
        columns: List of column names to display
        search_key: Unique key for search input
    """
    # Search bar
    search = st.text_input("🔍 Search", key=search_key, placeholder="Search...")
    
    # Filter data
    if search:
        filtered_data = [
            row for row in data 
            if any(search.lower() in str(row.get(col, '')).lower() for col in columns)
        ]
    else:
        filtered_data = data
    
    # Create DataFrame
    if filtered_data:
        df = pd.DataFrame(filtered_data)[columns]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No results found")


def render_user_table(users):
    """Render user management table"""
    table_html = """
    <div class="dataframe-container">
        <table>
            <thead>
                <tr>
                    <th>User</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Status</th>
                    <th>Last Login</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for user in users:
        role_color = 'var(--danger-color)' if user['role'] == 'Admin' else 'var(--primary-color)'
        status_badge = '<span class="badge badge-resolved">Active</span>' if user['status'] == 'active' else '<span class="badge badge-closed">Inactive</span>'
        
        table_html += f"""
            <tr>
                <td><strong>{user['name']}</strong></td>
                <td>{user['email']}</td>
                <td><span style="color: {role_color}; font-weight: 600;">{user['role']}</span></td>
                <td>{status_badge}</td>
                <td>{user['last_login']}</td>
                <td>
                    <button class="btn btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.8rem;">Edit</button>
                </td>
            </tr>
        """
    
    table_html += """
            </tbody>
        </table>
    </div>
    """
    
    st.markdown(table_html, unsafe_allow_html=True)


def render_recovery_logs_table(logs):
    """Render recovery action logs table"""
    if not logs:
        st.info("No recovery logs available")
        return
    
    table_html = """
    <div class="dataframe-container">
        <table>
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Incident ID</th>
                    <th>Action</th>
                    <th>Result</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for log in logs:
        result_badge = '<span class="badge badge-resolved">Success</span>' if log['success'] else '<span class="badge badge-critical">Failed</span>'
        
        table_html += f"""
            <tr>
                <td>{log['timestamp']}</td>
                <td><strong>#{log['incident_id']}</strong></td>
                <td><code>{log['action']}</code></td>
                <td>{result_badge}</td>
                <td style="font-size: 0.85rem; color: var(--text-secondary);">{log['details']}</td>
            </tr>
        """
    
    table_html += """
            </tbody>
        </table>
    </div>
    """
    
    st.markdown(table_html, unsafe_allow_html=True)


def render_filter_bar():
    """Render filter controls for tables"""
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        severity = st.multiselect(
            "Severity",
            ["critical", "high", "medium", "low"],
            default=[]
        )
    
    with col2:
        status = st.multiselect(
            "Status",
            ["open", "investigating", "resolved", "closed"],
            default=[]
        )
    
    with col3:
        service = st.multiselect(
            "Service",
            ["web-api", "database", "cache-server", "auth-service", "payment-service"],
            default=[]
        )
    
    with col4:
        if st.button("🔄 Reset", use_container_width=True):
            st.rerun()
    
    return {
        'severity': severity,
        'status': status,
        'service': service
    }
