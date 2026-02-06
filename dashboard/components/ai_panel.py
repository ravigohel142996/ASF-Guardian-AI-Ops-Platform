"""
AI Advisor Panel Component
Chat interface and recommendation cards
"""
import streamlit as st
from datetime import datetime
from dashboard.config import COLORS


def render_ai_chat_interface():
    """Render AI chat interface with history"""
    st.markdown('<div class="section-header">🤖 AI Advisor Chat</div>', unsafe_allow_html=True)
    
    # Initialize chat history
    if 'ai_messages' not in st.session_state:
        st.session_state.ai_messages = [
            {
                'role': 'assistant',
                'content': 'Hello! I\'m your AI Ops advisor. I can help you analyze incidents, suggest remediation steps, and provide best practices. How can I assist you today?',
                'timestamp': datetime.now()
            }
        ]
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat history
    for msg in st.session_state.ai_messages:
        role_label = "You" if msg['role'] == 'user' else "AI Advisor"
        role_class = "chat-message-user" if msg['role'] == 'user' else "chat-message-assistant"
        icon = "👤" if msg['role'] == 'user' else "🤖"
        
        st.markdown(f"""
        <div class="chat-message {role_class}">
            <div style="display: flex; gap: 0.75rem;">
                <div style="font-size: 1.5rem;">{icon}</div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; margin-bottom: 0.5rem;">{role_label}</div>
                    <div style="color: var(--text-secondary);">{msg['content']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Ask me anything about your infrastructure...")
    
    if user_input:
        # Add user message
        st.session_state.ai_messages.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now()
        })
        
        # Simulate AI response (in production, this would call the AI service)
        ai_response = generate_ai_response(user_input)
        
        st.session_state.ai_messages.append({
            'role': 'assistant',
            'content': ai_response,
            'timestamp': datetime.now()
        })
        
        st.rerun()
    
    # Clear chat button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.ai_messages = []
            st.rerun()


def generate_ai_response(user_input):
    """Generate simulated AI response (placeholder for actual AI integration)"""
    responses = {
        'incident': 'Based on the incident pattern, I recommend checking the database connection pool settings and increasing the timeout values.',
        'cpu': 'High CPU usage can be caused by inefficient queries or resource-intensive processes. I suggest profiling the application and optimizing hot paths.',
        'memory': 'Memory leaks are often caused by unclosed connections or growing caches. Enable memory profiling and monitor heap growth.',
        'default': 'I understand your concern. Let me analyze the current system state and provide recommendations based on historical patterns.'
    }
    
    user_input_lower = user_input.lower()
    
    for key, response in responses.items():
        if key in user_input_lower:
            return response
    
    return responses['default']


def render_recommendation_cards():
    """Render AI-generated recommendation cards"""
    st.markdown('<div class="section-subheader">💡 AI Recommendations</div>', unsafe_allow_html=True)
    
    recommendations = [
        {
            'title': 'Optimize Database Connection Pool',
            'priority': 'high',
            'impact': 'High',
            'effort': 'Medium',
            'description': 'Current connection pool size is insufficient during peak hours. Increasing from 20 to 50 connections will reduce timeout errors by ~80%.',
            'action': 'Update db.max_connections in production.yaml'
        },
        {
            'title': 'Enable Auto-Scaling for Web Tier',
            'priority': 'medium',
            'impact': 'Medium',
            'effort': 'Low',
            'description': 'CPU utilization reaches 85% during traffic spikes. Auto-scaling will improve response times and prevent service degradation.',
            'action': 'Configure horizontal pod autoscaler with target CPU at 70%'
        },
        {
            'title': 'Implement Circuit Breaker Pattern',
            'priority': 'medium',
            'impact': 'High',
            'effort': 'High',
            'description': 'Payment service failures cascade to other services. Circuit breaker will isolate failures and improve system resilience.',
            'action': 'Add circuit breaker middleware to API gateway'
        }
    ]
    
    for rec in recommendations:
        priority_color = {
            'high': 'var(--danger-color)',
            'medium': 'var(--warning-color)',
            'low': 'var(--success-color)'
        }.get(rec['priority'], 'var(--info-color)')
        
        st.markdown(f"""
        <div class="glass-card" style="border-left: 4px solid {priority_color}; margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                <div>
                    <h3 style="margin: 0; color: var(--text-primary); font-size: 1.1rem;">{rec['title']}</h3>
                    <div style="display: flex; gap: 1rem; margin-top: 0.5rem;">
                        <span class="badge" style="background: {priority_color}20; color: {priority_color}; border-color: {priority_color};">
                            {rec['priority'].upper()} PRIORITY
                        </span>
                        <span style="color: var(--text-secondary); font-size: 0.85rem;">Impact: {rec['impact']}</span>
                        <span style="color: var(--text-secondary); font-size: 0.85rem;">Effort: {rec['effort']}</span>
                    </div>
                </div>
            </div>
            <p style="color: var(--text-secondary); margin-bottom: 1rem; line-height: 1.6;">
                {rec['description']}
            </p>
            <div style="background: rgba(255, 255, 255, 0.03); padding: 0.75rem; border-radius: 8px; border-left: 3px solid var(--primary-color);">
                <strong style="color: var(--primary-color); font-size: 0.85rem;">ACTION:</strong>
                <code style="color: var(--text-secondary); margin-left: 0.5rem; font-size: 0.85rem;">{rec['action']}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_quick_insights():
    """Render quick insights panel"""
    st.markdown('<div class="section-subheader">⚡ Quick Insights</div>', unsafe_allow_html=True)
    
    insights = [
        {
            'icon': '📈',
            'title': 'Incident Trend',
            'value': '↓ 23%',
            'description': 'Incidents decreased compared to last week'
        },
        {
            'icon': '⚡',
            'title': 'Recovery Speed',
            'value': '28 min',
            'description': 'Average time to recovery (MTTR)'
        },
        {
            'icon': '🎯',
            'title': 'Success Rate',
            'value': '87%',
            'description': 'Auto-recovery success rate'
        },
        {
            'icon': '🔥',
            'title': 'Top Issue',
            'value': 'High CPU',
            'description': 'Most common incident type'
        }
    ]
    
    cols = st.columns(4)
    
    for idx, insight in enumerate(insights):
        with cols[idx]:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center; padding: 1.25rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{insight['icon']}</div>
                <div style="font-size: 0.8rem; color: var(--text-secondary); text-transform: uppercase; margin-bottom: 0.5rem;">
                    {insight['title']}
                </div>
                <div style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.5rem;">
                    {insight['value']}
                </div>
                <div style="font-size: 0.75rem; color: var(--text-secondary);">
                    {insight['description']}
                </div>
            </div>
            """, unsafe_allow_html=True)


def render_ai_analysis_panel(incident_id=None):
    """Render AI incident analysis panel"""
    st.markdown('<div class="section-subheader">🔍 Incident Analysis</div>', unsafe_allow_html=True)
    
    if incident_id:
        st.markdown(f"""
        <div class="glass-card">
            <h4 style="color: var(--text-primary); margin-bottom: 1rem;">Incident #{incident_id} Analysis</h4>
            
            <div style="margin-bottom: 1.5rem;">
                <strong style="color: var(--primary-color);">Root Cause:</strong>
                <p style="color: var(--text-secondary); margin-top: 0.5rem; line-height: 1.6;">
                    Database connection pool exhaustion due to slow queries and high concurrent requests during peak hours.
                </p>
            </div>
            
            <div style="margin-bottom: 1.5rem;">
                <strong style="color: var(--primary-color);">Impact Assessment:</strong>
                <p style="color: var(--text-secondary); margin-top: 0.5rem; line-height: 1.6;">
                    - Response time increased by 300%<br>
                    - 15% of requests failed with timeout errors<br>
                    - Affected 3 downstream services
                </p>
            </div>
            
            <div style="margin-bottom: 1.5rem;">
                <strong style="color: var(--primary-color);">Recommended Actions:</strong>
                <ol style="color: var(--text-secondary); margin-top: 0.5rem; line-height: 1.8; padding-left: 1.5rem;">
                    <li>Immediately increase connection pool size from 20 to 50</li>
                    <li>Optimize top 5 slow queries identified in logs</li>
                    <li>Implement connection pooling monitoring</li>
                    <li>Add alerts for connection pool utilization > 80%</li>
                </ol>
            </div>
            
            <div>
                <strong style="color: var(--primary-color);">Prevention Strategy:</strong>
                <p style="color: var(--text-secondary); margin-top: 0.5rem; line-height: 1.6;">
                    Enable auto-scaling for database read replicas and implement query caching for frequently accessed data.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Select an incident to view AI-powered analysis")
