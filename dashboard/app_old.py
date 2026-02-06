"""
ASF-Guardian Dashboard
Main Streamlit application for enterprise AI Ops platform
"""
import streamlit as st
import requests
import sys
import os
from datetime import datetime
import time

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dashboard.monitor import (
    show_metric_card,
    show_severity_badge,
    show_status_badge,
    create_incidents_timeline,
    create_severity_distribution,
    create_recovery_stats_chart,
    show_incident_table,
    show_system_metrics,
    create_mttr_chart,
    show_alert_settings
)
from ai_advisor.chatbot import AIAdvisor

# Page configuration
st.set_page_config(
    page_title="ASF-Guardian",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern SaaS style
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(120deg, #2196F3, #00BCD4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-header {
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .status-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")

# Initialize session state
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

if 'selected_incident' not in st.session_state:
    st.session_state.selected_incident = None


def get_api_data(endpoint: str):
    """Fetch data from API"""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None


def post_api_data(endpoint: str, data: dict):
    """Post data to API"""
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data, timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None


# Header
st.markdown('<h1 class="main-header">🛡️ ASF-Guardian</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Enterprise AI Incident & Auto-Healing Platform</p>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Dashboard", "🚨 Incidents", "🤖 AI Advisor", "⚙️ Settings", "📊 Analytics"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔗 Quick Links")
st.sidebar.markdown(f"[API Docs]({API_BASE_URL}/docs)")
st.sidebar.markdown("[GitHub](https://github.com/ravigohel142996/ASF-Guardian-AI-Ops-Platform)")

st.sidebar.markdown("---")
st.sidebar.info("Built with ❤️ by Ravi")

# ==================== DASHBOARD PAGE ====================
if page == "🏠 Dashboard":
    st.header("📊 System Overview")
    
    # Fetch stats
    incident_stats = get_api_data("/api/incidents/stats/summary")
    recovery_stats = get_api_data("/api/recovery/stats")
    
    if incident_stats and recovery_stats:
        # Top metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Incidents", incident_stats.get('total', 0))
        
        with col2:
            st.metric("Open Incidents", incident_stats.get('open', 0), 
                     delta=None if incident_stats.get('open', 0) == 0 else "⚠️")
        
        with col3:
            st.metric("Auto-Recovered", incident_stats.get('auto_recovered', 0))
        
        with col4:
            success_rate = recovery_stats.get('success_rate', 0)
            st.metric("Recovery Rate", f"{success_rate}%")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Recent Activity")
        incidents_data = get_api_data("/api/incidents?limit=50")
        
        if incidents_data and incidents_data.get('incidents'):
            incidents = incidents_data['incidents']
            
            # Timeline chart
            timeline_fig = create_incidents_timeline(incidents)
            if timeline_fig:
                st.plotly_chart(timeline_fig, use_container_width=True)
            
            # Recent incidents
            st.subheader("🔔 Recent Incidents")
            recent = incidents[:5]
            show_incident_table(recent)
        else:
            st.info("No incidents found")
    
    with col2:
        st.subheader("📊 Statistics")
        
        if incidents_data and incidents_data.get('incidents'):
            # Severity distribution
            severity_fig = create_severity_distribution(incidents)
            if severity_fig:
                st.plotly_chart(severity_fig, use_container_width=True)
            
            # Recovery stats
            if recovery_stats:
                recovery_fig = create_recovery_stats_chart(recovery_stats)
                if recovery_fig:
                    st.plotly_chart(recovery_fig, use_container_width=True)
    
    # System metrics (simulated)
    st.markdown("---")
    st.subheader("💻 System Health")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("CPU Usage", "45%", delta="-5%", delta_color="inverse")
        st.progress(0.45)
    
    with col2:
        st.metric("Memory Usage", "62%", delta="2%", delta_color="inverse")
        st.progress(0.62)
    
    with col3:
        st.metric("Disk Usage", "38%", delta="-1%", delta_color="inverse")
        st.progress(0.38)


# ==================== INCIDENTS PAGE ====================
elif page == "🚨 Incidents":
    st.header("🚨 Incident Management")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["All Incidents", "Open Incidents", "Create Test Incident"])
    
    with tab1:
        st.subheader("All Incidents")
        
        incidents_data = get_api_data("/api/incidents?limit=100")
        
        if incidents_data and incidents_data.get('incidents'):
            incidents = incidents_data['incidents']
            
            # Filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                severity_filter = st.multiselect(
                    "Filter by Severity",
                    ["critical", "high", "medium", "low"],
                    default=[]
                )
            
            with col2:
                status_filter = st.multiselect(
                    "Filter by Status",
                    ["open", "investigating", "resolved", "closed"],
                    default=[]
                )
            
            # Apply filters
            filtered = incidents
            if severity_filter:
                filtered = [i for i in filtered if i['severity'] in severity_filter]
            if status_filter:
                filtered = [i for i in filtered if i['status'] in status_filter]
            
            st.write(f"Showing {len(filtered)} incidents")
            
            # Display incidents
            show_incident_table(filtered)
        else:
            st.info("No incidents found")
    
    with tab2:
        st.subheader("Open Incidents")
        
        open_incidents = get_api_data("/api/incidents?status=open")
        
        if open_incidents and open_incidents.get('incidents'):
            incidents = open_incidents['incidents']
            
            if len(incidents) == 0:
                st.success("✅ No open incidents!")
            else:
                st.warning(f"⚠️ {len(incidents)} open incident(s) require attention")
                show_incident_table(incidents)
                
                # Bulk actions
                st.subheader("Bulk Actions")
                if st.button("🔄 Attempt Recovery on All"):
                    with st.spinner("Attempting recovery..."):
                        for incident in incidents:
                            result = post_api_data(
                                "/api/recovery/attempt",
                                {"incident_id": incident['id']}
                            )
                            if result and result.get('success'):
                                st.success(f"✅ Recovered incident #{incident['id']}")
                            else:
                                st.error(f"❌ Failed to recover incident #{incident['id']}")
                        
                        time.sleep(1)
                        st.rerun()
        else:
            st.success("✅ No open incidents!")
    
    with tab3:
        st.subheader("Create Test Incident")
        st.info("Generate a test incident for demonstration purposes")
        
        with st.form("create_incident"):
            col1, col2 = st.columns(2)
            
            with col1:
                service = st.selectbox(
                    "Service",
                    ["web-api", "database", "cache-server", "auth-service", "payment-service"]
                )
                metric = st.selectbox(
                    "Metric",
                    ["cpu", "memory", "disk", "response_time", "error_rate"]
                )
            
            with col2:
                severity = st.selectbox("Severity", ["critical", "high", "medium", "low"])
                
                # Calculate value based on severity
                thresholds = {
                    'cpu': 80, 'memory': 85, 'disk': 90,
                    'response_time': 5000, 'error_rate': 5
                }
                
                base_threshold = thresholds.get(metric, 100)
                
                if severity == 'critical':
                    value = base_threshold * 1.6
                elif severity == 'high':
                    value = base_threshold * 1.3
                elif severity == 'medium':
                    value = base_threshold * 1.15
                else:
                    value = base_threshold * 1.05
                
                st.metric("Generated Value", f"{value:.2f}")
            
            submitted = st.form_submit_button("Create Test Incident")
            
            if submitted:
                with st.spinner("Creating incident..."):
                    result = post_api_data(
                        "/api/incidents/check",
                        {
                            "service_name": service,
                            "metric_name": metric,
                            "metric_value": value
                        }
                    )
                    
                    if result and result.get('status') == 'incident_created':
                        st.success(f"✅ Test incident created: #{result['incident']['id']}")
                        st.json(result['incident'])
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Failed to create incident")


# ==================== AI ADVISOR PAGE ====================
elif page == "🤖 AI Advisor":
    st.header("🤖 AI-Powered Advisor")
    
    tab1, tab2 = st.tabs(["Chat", "Quick Analysis"])
    
    with tab1:
        st.subheader("💬 Chat with AI Advisor")
        
        # Chat interface
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.chat_messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
        
        # Chat input
        user_input = st.chat_input("Ask me anything about incident management...")
        
        if user_input:
            # Add user message
            st.session_state.chat_messages.append({
                "role": "user",
                "content": user_input
            })
            
            # Get AI response
            with st.spinner("Thinking..."):
                advisor = AIAdvisor()
                response = advisor.ask(user_input)
                advisor.close()
                
                if response.get('success'):
                    answer = response['answer']
                else:
                    answer = response.get('answer', 'Sorry, I encountered an error.')
                
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": answer
                })
            
            st.rerun()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_messages = []
            st.rerun()
    
    with tab2:
        st.subheader("📋 Quick Analysis")
        
        # Get recent incidents
        incidents_data = get_api_data("/api/incidents?limit=10")
        
        if incidents_data and incidents_data.get('incidents'):
            incidents = incidents_data['incidents']
            
            # Select incident to analyze
            incident_options = {
                f"#{i['id']} - {i['title']}": i['id']
                for i in incidents
            }
            
            selected = st.selectbox("Select Incident to Analyze", list(incident_options.keys()))
            
            if selected and st.button("🔍 Analyze Incident"):
                incident_id = incident_options[selected]
                
                with st.spinner("Analyzing incident..."):
                    advisor = AIAdvisor()
                    analysis = advisor.analyze_incident(incident_id)
                    advisor.close()
                    
                    if analysis.get('success'):
                        st.success("✅ Analysis Complete")
                        st.markdown(analysis['answer'])
                    else:
                        st.error(analysis.get('message', 'Analysis failed'))
        else:
            st.info("No incidents available for analysis")
        
        # Quick tips
        st.markdown("---")
        st.subheader("💡 Quick Tips")
        
        advisor = AIAdvisor()
        tips = advisor.get_quick_tips()
        advisor.close()
        
        for tip in tips:
            st.markdown(f"- {tip}")


# ==================== SETTINGS PAGE ====================
elif page == "⚙️ Settings":
    st.header("⚙️ Configuration")
    
    # Alert settings
    settings = show_alert_settings()
    
    st.markdown("---")
    
    # API Configuration
    st.subheader("🔗 API Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("API URL", value=API_BASE_URL, disabled=True)
        st.text_input("Database", value="SQLite", disabled=True)
    
    with col2:
        api_status = get_api_data("/health")
        if api_status:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Disconnected")
    
    # Environment info
    st.markdown("---")
    st.subheader("ℹ️ System Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**Platform**\nASF-Guardian v1.0.0")
    
    with col2:
        st.info("**Tech Stack**\nStreamlit + FastAPI")
    
    with col3:
        st.info("**Database**\nSQLite")


# ==================== ANALYTICS PAGE ====================
elif page == "📊 Analytics":
    st.header("📊 Advanced Analytics")
    
    incidents_data = get_api_data("/api/incidents?limit=100")
    
    if incidents_data and incidents_data.get('incidents'):
        incidents = incidents_data['incidents']
        
        # MTTR Chart
        st.subheader("⏱️ Mean Time To Recovery (MTTR)")
        mttr_fig = create_mttr_chart(incidents)
        if mttr_fig:
            st.plotly_chart(mttr_fig, use_container_width=True)
        else:
            st.info("No resolved incidents to analyze")
        
        st.markdown("---")
        
        # Service analysis
        st.subheader("🔍 Service Analysis")
        
        # Count incidents by service
        from collections import Counter
        service_counts = Counter([i['service_name'] for i in incidents])
        
        import pandas as pd
        import plotly.express as px
        
        df = pd.DataFrame({
            'Service': list(service_counts.keys()),
            'Incidents': list(service_counts.values())
        })
        
        fig = px.bar(
            df,
            x='Service',
            y='Incidents',
            title='Incidents by Service',
            color='Incidents',
            color_continuous_scale='Reds'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Trends
        st.subheader("📈 Trends")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Average Incidents/Day", "12.5", delta="-2.3")
            st.metric("Peak Hour", "14:00 - 15:00")
        
        with col2:
            most_affected = df.iloc[0]['Service'] if len(df) > 0 and 'Service' in df.columns else "N/A"
            st.metric("Most Affected Service", most_affected)
            st.metric("Common Issue", "High CPU Usage")
    else:
        st.info("No data available for analytics")


# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p><strong>ASF-Guardian</strong> - Enterprise AI Incident & Auto-Healing Platform</p>
        <p>Built with Streamlit, FastAPI, and OpenAI | 
        <a href='https://github.com/ravigohel142996/ASF-Guardian-AI-Ops-Platform' target='_blank'>GitHub</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
