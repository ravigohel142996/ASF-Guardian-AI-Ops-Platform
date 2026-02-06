"""
Email Alert System
Sends email notifications for incidents and recovery actions
"""
from celery import Celery
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from database.models import get_db_session, Incident

# Initialize Celery
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
app = Celery('asf_mailer', broker=REDIS_URL, backend=REDIS_URL)

# Email configuration
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
ALERT_EMAIL = os.getenv('ALERT_EMAIL', 'admin@example.com')


class EmailAlert:
    """Email alert handler"""
    
    def __init__(self):
        self.smtp_host = SMTP_HOST
        self.smtp_port = SMTP_PORT
        self.smtp_user = SMTP_USER
        self.smtp_password = SMTP_PASSWORD
        self.alert_email = ALERT_EMAIL
    
    def send_email(self, subject: str, body: str, to_email: str = None):
        """
        Send email alert
        
        Args:
            subject: Email subject
            body: Email body (HTML)
            to_email: Recipient email (defaults to ALERT_EMAIL)
        """
        if not self.smtp_user or not self.smtp_password:
            print("⚠️ Email credentials not configured, skipping email")
            return False
        
        to_email = to_email or self.alert_email
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.smtp_user
            msg['To'] = to_email
            
            # Attach HTML body
            html_part = MIMEText(body, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            print(f"✅ Email sent to {to_email}: {subject}")
            return True
        
        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
            return False
    
    def format_incident_email(self, incident: dict, recovery_result: dict = None) -> str:
        """
        Format incident details into HTML email
        
        Args:
            incident: Incident details
            recovery_result: Optional recovery result
            
        Returns:
            str: HTML email body
        """
        severity_colors = {
            'critical': '#dc3545',
            'high': '#fd7e14',
            'medium': '#ffc107',
            'low': '#6c757d'
        }
        
        color = severity_colors.get(incident.get('severity', 'low'), '#6c757d')
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: {color}; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f4f4f4; }}
                .incident-box {{ background-color: white; padding: 15px; margin: 10px 0; border-left: 4px solid {color}; }}
                .label {{ font-weight: bold; color: #555; }}
                .value {{ color: #000; }}
                .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #777; }}
                .recovery {{ background-color: #d4edda; padding: 10px; margin: 10px 0; border-left: 4px solid #28a745; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚨 ASF-Guardian Alert</h1>
                <h2>{incident.get('title', 'System Incident')}</h2>
            </div>
            
            <div class="content">
                <div class="incident-box">
                    <p><span class="label">Incident ID:</span> <span class="value">#{incident.get('id', 'N/A')}</span></p>
                    <p><span class="label">Severity:</span> <span class="value" style="color: {color}; text-transform: uppercase;">{incident.get('severity', 'Unknown')}</span></p>
                    <p><span class="label">Service:</span> <span class="value">{incident.get('service_name', 'Unknown')}</span></p>
                    <p><span class="label">Status:</span> <span class="value">{incident.get('status', 'Unknown')}</span></p>
                    <p><span class="label">Description:</span> <span class="value">{incident.get('description', 'No description')}</span></p>
                    <p><span class="label">Detected At:</span> <span class="value">{incident.get('detected_at', 'Unknown')}</span></p>
                    
                    {f'<p><span class="label">Metric Value:</span> <span class="value">{incident.get("metric_value", "N/A")}</span></p>' if incident.get('metric_value') else ''}
                    {f'<p><span class="label">Threshold:</span> <span class="value">{incident.get("threshold_value", "N/A")}</span></p>' if incident.get('threshold_value') else ''}
                </div>
        """
        
        if recovery_result:
            if recovery_result.get('success'):
                html += f"""
                <div class="recovery">
                    <h3>✅ Auto-Recovery Successful</h3>
                    <p><span class="label">Action:</span> <span class="value">{recovery_result.get('action_type', 'Unknown')}</span></p>
                    <p>The system has automatically recovered from this incident.</p>
                </div>
                """
            else:
                html += f"""
                <div class="incident-box" style="border-left-color: #dc3545;">
                    <h3>❌ Auto-Recovery Failed</h3>
                    <p><span class="label">Error:</span> <span class="value">{recovery_result.get('error', 'Unknown error')}</span></p>
                    <p style="color: #dc3545; font-weight: bold;">Manual intervention required!</p>
                </div>
                """
        
        html += """
            </div>
            
            <div class="footer">
                <p>ASF-Guardian - Enterprise AI Incident & Auto-Healing Platform</p>
                <p>This is an automated alert from your monitoring system.</p>
            </div>
        </body>
        </html>
        """
        
        return html


@app.task(name='alerts.mailer.send_incident_alert')
def send_incident_alert(incident_id: int, recovery_result: dict = None):
    """
    Send email alert for an incident
    
    Args:
        incident_id: ID of the incident
        recovery_result: Optional recovery result
    """
    try:
        # Get incident details
        db = get_db_session()
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        db.close()
        
        if not incident:
            print(f"❌ Incident {incident_id} not found")
            return {'status': 'error', 'message': 'Incident not found'}
        
        incident_dict = incident.to_dict()
        
        # Create email
        mailer = EmailAlert()
        
        # Create subject
        if recovery_result and recovery_result.get('success'):
            subject = f"✅ [RESOLVED] {incident.severity.upper()}: {incident.title}"
        else:
            subject = f"🚨 [{incident.severity.upper()}] {incident.title}"
        
        # Format email body
        body = mailer.format_incident_email(incident_dict, recovery_result)
        
        # Send email
        success = mailer.send_email(subject, body)
        
        return {
            'status': 'success' if success else 'failed',
            'incident_id': incident_id,
            'email_sent': success
        }
    
    except Exception as e:
        print(f"❌ Error sending incident alert: {str(e)}")
        return {'status': 'error', 'message': str(e)}


@app.task(name='alerts.mailer.send_daily_summary')
def send_daily_summary():
    """Send daily summary of incidents"""
    try:
        from backend.incidents import IncidentDetector
        
        detector = IncidentDetector()
        stats = detector.get_incident_stats()
        recent_incidents = detector.get_incident_history(limit=10)
        detector.close()
        
        # Create summary email
        mailer = EmailAlert()
        
        subject = f"📊 ASF-Guardian Daily Summary - {datetime.utcnow().strftime('%Y-%m-%d')}"
        
        body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; }}
                .stats {{ display: flex; justify-content: space-around; padding: 20px; }}
                .stat-box {{ text-align: center; padding: 15px; background-color: #f8f9fa; border-radius: 5px; }}
                .stat-number {{ font-size: 32px; font-weight: bold; color: #007bff; }}
                .stat-label {{ color: #6c757d; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Daily Summary</h1>
                <p>{datetime.utcnow().strftime('%Y-%m-%d')}</p>
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">{stats.get('total', 0)}</div>
                    <div class="stat-label">Total Incidents</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{stats.get('open', 0)}</div>
                    <div class="stat-label">Open</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{stats.get('resolved', 0)}</div>
                    <div class="stat-label">Resolved</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{stats.get('auto_recovered', 0)}</div>
                    <div class="stat-label">Auto-Recovered</div>
                </div>
            </div>
            
            <div style="padding: 20px;">
                <h2>Recent Incidents</h2>
                <ul>
        """
        
        for incident in recent_incidents[:5]:
            body += f"<li>{incident.get('title')} - {incident.get('status')}</li>"
        
        body += """
                </ul>
            </div>
        </body>
        </html>
        """
        
        success = mailer.send_email(subject, body)
        
        return {'status': 'success' if success else 'failed'}
    
    except Exception as e:
        print(f"❌ Error sending daily summary: {str(e)}")
        return {'status': 'error', 'message': str(e)}


if __name__ == '__main__':
    # Test email
    mailer = EmailAlert()
    print("Email alert system initialized!")
