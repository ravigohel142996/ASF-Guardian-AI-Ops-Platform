"""
Database models for ASF-Guardian AI Ops Platform
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Incident(Base):
    """Incident model for tracking system issues"""
    __tablename__ = 'incidents'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(50), nullable=False)  # critical, high, medium, low
    status = Column(String(50), nullable=False)  # open, investigating, resolved, closed
    service_name = Column(String(100), nullable=False)
    detected_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    auto_recovered = Column(Boolean, default=False)
    recovery_action = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    metric_value = Column(Float, nullable=True)
    threshold_value = Column(Float, nullable=True)
    
    def to_dict(self):
        """Convert incident to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'severity': self.severity,
            'status': self.status,
            'service_name': self.service_name,
            'detected_at': self.detected_at.isoformat() if self.detected_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'auto_recovered': self.auto_recovered,
            'recovery_action': self.recovery_action,
            'error_message': self.error_message,
            'metric_value': self.metric_value,
            'threshold_value': self.threshold_value
        }


class RecoveryAction(Base):
    """Recovery action logs"""
    __tablename__ = 'recovery_actions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    incident_id = Column(Integer, nullable=False)
    action_type = Column(String(100), nullable=False)  # restart, scale, rollback, etc.
    action_details = Column(Text, nullable=False)
    status = Column(String(50), nullable=False)  # success, failed, pending
    executed_at = Column(DateTime, default=datetime.utcnow)
    error_message = Column(Text, nullable=True)
    
    def to_dict(self):
        """Convert recovery action to dictionary"""
        return {
            'id': self.id,
            'incident_id': self.incident_id,
            'action_type': self.action_type,
            'action_details': self.action_details,
            'status': self.status,
            'executed_at': self.executed_at.isoformat() if self.executed_at else None,
            'error_message': self.error_message
        }


class SystemMetric(Base):
    """System metrics for monitoring"""
    __tablename__ = 'system_metrics'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String(100), nullable=False)
    metric_name = Column(String(100), nullable=False)  # cpu, memory, disk, response_time
    metric_value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_healthy = Column(Boolean, default=True)
    
    def to_dict(self):
        """Convert metric to dictionary"""
        return {
            'id': self.id,
            'service_name': self.service_name,
            'metric_name': self.metric_name,
            'metric_value': self.metric_value,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'is_healthy': self.is_healthy
        }


# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./asf_guardian.db')
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database with tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_session():
    """Get database session (non-generator version)"""
    return SessionLocal()


if __name__ == "__main__":
    init_db()
