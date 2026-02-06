"""
AI Advisor Chatbot
OpenAI-powered intelligent assistant for incident analysis and recommendations
"""
import openai
import os
from typing import List, Dict
from database.models import get_db_session, Incident, RecoveryAction

# Configure OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY


class AIAdvisor:
    """AI-powered advisor for incident management"""
    
    def __init__(self):
        self.model = "gpt-3.5-turbo"
        self.max_tokens = 500
        self.temperature = 0.7
        self.db = get_db_session()
    
    def get_incident_context(self, incident_id: int = None) -> str:
        """
        Get context about incidents for the AI
        
        Args:
            incident_id: Optional specific incident ID
            
        Returns:
            str: Context string for AI
        """
        if incident_id:
            incident = self.db.query(Incident).filter(Incident.id == incident_id).first()
            if incident:
                recovery_actions = self.db.query(RecoveryAction).filter(
                    RecoveryAction.incident_id == incident_id
                ).all()
                
                context = f"""
                Incident #{incident.id}:
                - Title: {incident.title}
                - Severity: {incident.severity}
                - Status: {incident.status}
                - Service: {incident.service_name}
                - Description: {incident.description}
                - Detected: {incident.detected_at}
                - Auto-recovered: {incident.auto_recovered}
                """
                
                if recovery_actions:
                    context += "\nRecovery Actions Attempted:\n"
                    for action in recovery_actions:
                        context += f"- {action.action_type}: {action.status}\n"
                
                return context
        else:
            # Get recent incidents summary
            recent = self.db.query(Incident).order_by(
                Incident.detected_at.desc()
            ).limit(5).all()
            
            context = "Recent Incidents:\n"
            for inc in recent:
                context += f"- #{inc.id}: {inc.title} ({inc.severity}, {inc.status})\n"
            
            return context
    
    def ask(self, question: str, incident_id: int = None) -> dict:
        """
        Ask the AI advisor a question
        
        Args:
            question: User's question
            incident_id: Optional incident ID for context
            
        Returns:
            dict: AI response with answer and suggestions
        """
        if not OPENAI_API_KEY:
            return {
                'success': False,
                'message': 'OpenAI API key not configured',
                'answer': 'Please configure your OpenAI API key to use the AI Advisor.'
            }
        
        try:
            # Get incident context
            context = self.get_incident_context(incident_id)
            
            # Create system prompt
            system_prompt = """
            You are an expert DevOps and SRE AI advisor for ASF-Guardian, 
            an enterprise incident management and auto-healing platform.
            
            Your role is to:
            1. Analyze incidents and provide root cause analysis
            2. Suggest remediation actions and best practices
            3. Recommend preventive measures
            4. Explain technical concepts clearly
            5. Provide actionable insights
            
            Always be concise, professional, and focus on practical solutions.
            """
            
            # Create user prompt with context
            user_prompt = f"""
            Context:
            {context}
            
            Question: {question}
            
            Please provide a helpful, actionable response.
            """
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            answer = response.choices[0].message.content.strip()
            
            return {
                'success': True,
                'answer': answer,
                'context': context,
                'model': self.model
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Error: {str(e)}',
                'answer': 'Sorry, I encountered an error processing your question. Please try again.'
            }
    
    def analyze_incident(self, incident_id: int) -> dict:
        """
        Perform AI-powered analysis of an incident
        
        Args:
            incident_id: ID of the incident to analyze
            
        Returns:
            dict: Analysis results
        """
        incident = self.db.query(Incident).filter(Incident.id == incident_id).first()
        
        if not incident:
            return {
                'success': False,
                'message': 'Incident not found'
            }
        
        question = f"""
        Analyze this incident and provide:
        1. Likely root cause
        2. Impact assessment
        3. Recommended actions
        4. Prevention strategies
        """
        
        return self.ask(question, incident_id)
    
    def suggest_recovery(self, incident_id: int) -> dict:
        """
        Get AI suggestions for incident recovery
        
        Args:
            incident_id: ID of the incident
            
        Returns:
            dict: Recovery suggestions
        """
        question = """
        What are the best recovery strategies for this incident?
        Prioritize them and explain why.
        """
        
        return self.ask(question, incident_id)
    
    def get_prevention_tips(self, service_name: str = None) -> dict:
        """
        Get preventive maintenance tips
        
        Args:
            service_name: Optional service name to focus on
            
        Returns:
            dict: Prevention tips
        """
        if service_name:
            question = f"What are best practices for preventing incidents in {service_name}?"
        else:
            question = "What are general best practices for preventing system incidents?"
        
        return self.ask(question)
    
    def chat(self, messages: List[Dict[str, str]]) -> dict:
        """
        Have a multi-turn conversation with the AI
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            
        Returns:
            dict: AI response
        """
        if not OPENAI_API_KEY:
            return {
                'success': False,
                'message': 'OpenAI API key not configured'
            }
        
        try:
            # Add system message if not present
            if not any(msg['role'] == 'system' for msg in messages):
                system_msg = {
                    "role": "system",
                    "content": """You are an expert DevOps AI advisor for ASF-Guardian.
                    Help users with incident management, system monitoring, and DevOps best practices."""
                }
                messages = [system_msg] + messages
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            answer = response.choices[0].message.content.strip()
            
            return {
                'success': True,
                'answer': answer,
                'model': self.model
            }
        
        except Exception as e:
            return {
                'success': False,
                'message': f'Error: {str(e)}'
            }
    
    def get_quick_tips(self) -> List[str]:
        """Get quick tips for using the platform"""
        return [
            "💡 Configure alert thresholds based on your baseline metrics",
            "🔄 Review auto-recovery success rates regularly",
            "📊 Monitor trends to predict future incidents",
            "⚡ Set up email alerts for critical incidents",
            "🎯 Use AI advisor for root cause analysis",
            "📈 Track MTTR (Mean Time To Recovery) metrics",
            "🔒 Implement monitoring for security metrics",
            "🚀 Automate common recovery actions"
        ]
    
    def close(self):
        """Close database connection"""
        self.db.close()


def demo_ai_advisor():
    """Demo the AI advisor capabilities"""
    advisor = AIAdvisor()
    
    print("🤖 ASF-Guardian AI Advisor Demo\n")
    
    # Example questions
    questions = [
        "What should I do if CPU usage is consistently high?",
        "How can I prevent memory leaks in production?",
        "What are signs of a DDoS attack?"
    ]
    
    for q in questions:
        print(f"Q: {q}")
        response = advisor.ask(q)
        if response['success']:
            print(f"A: {response['answer']}\n")
        else:
            print(f"Error: {response['message']}\n")
    
    advisor.close()


if __name__ == "__main__":
    demo_ai_advisor()
