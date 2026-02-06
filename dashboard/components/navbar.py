"""
Navigation Bar Component
Professional top navigation with user profile and notifications
"""
import streamlit as st
from datetime import datetime
from dashboard.config import APP_CONFIG


def render_navbar():
    """Render professional navigation bar"""
    st.markdown("""
    <div class="navbar">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div class="navbar-brand">
                🛡️ {name}
            </div>
            <div style="color: var(--text-secondary); font-size: 0.9rem;">
                {tagline}
            </div>
        </div>
        <div class="navbar-user">
            <div style="color: var(--text-secondary); font-size: 0.85rem;">
                {time}
            </div>
            <div style="color: var(--text-primary); font-weight: 600;">
                Admin
            </div>
        </div>
    </div>
    """.format(
        name=APP_CONFIG['name'],
        tagline=APP_CONFIG['tagline'],
        time=datetime.now().strftime("%B %d, %Y • %H:%M")
    ), unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar navigation"""
    st.sidebar.markdown(f"""
    <div style="padding: 1rem 0; border-bottom: 1px solid var(--border-color); margin-bottom: 1rem;">
        <div style="font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem;">
            🛡️ {APP_CONFIG['name']}
        </div>
        <div style="color: var(--text-secondary); font-size: 0.85rem;">
            v{APP_CONFIG['version']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation options
    pages = {
        "🏠 Dashboard": "dashboard",
        "📊 System Overview": "system_overview", 
        "🚨 Incident Management": "incidents",
        "🤖 AI Advisor": "ai_advisor",
        "⚙️ Auto-Healing": "auto_healing",
        "👥 Admin Panel": "admin",
        "⚙️ Settings": "settings"
    }
    
    selected_page = st.sidebar.radio(
        "Navigation",
        list(pages.keys()),
        label_visibility="collapsed"
    )
    
    # Quick Stats
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚡ Quick Stats")
    
    return pages[selected_page]


def render_user_menu():
    """Render user profile menu"""
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 👤 User Profile")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("👤")
        with col2:
            st.markdown("**Admin User**")
            st.markdown(f"<small style='color: var(--text-secondary);'>admin@asf-guardian.com</small>", unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            st.info("Logout functionality would be implemented here")


def render_notifications():
    """Render notification panel"""
    notifications = [
        {"type": "critical", "message": "Critical incident detected in web-api", "time": "2 min ago"},
        {"type": "success", "message": "Auto-recovery successful for db-service", "time": "15 min ago"},
        {"type": "warning", "message": "High CPU usage detected", "time": "1 hour ago"},
    ]
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🔔 Notifications")
        
        for notif in notifications[:3]:
            icon = "🔴" if notif["type"] == "critical" else "✅" if notif["type"] == "success" else "⚠️"
            st.markdown(f"""
            <div style="padding: 0.75rem; background: var(--card-bg); border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid {'var(--danger-color)' if notif['type'] == 'critical' else 'var(--success-color)' if notif['type'] == 'success' else 'var(--warning-color)'};">
                <div style="font-size: 0.85rem; color: var(--text-primary);">{icon} {notif['message']}</div>
                <div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.25rem;">{notif['time']}</div>
            </div>
            """, unsafe_allow_html=True)
