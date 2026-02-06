"""
FastAPI Backend API
Main REST API for ASF-Guardian Platform
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from backend.incidents import IncidentDetector
from backend.recovery import AutoRecovery
from database.models import init_db

# Initialize FastAPI app
app = FastAPI(
    title="ASF-Guardian API",
    description="Enterprise AI Incident & Auto-Healing Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()
    print("🚀 ASF-Guardian API started successfully!")


# Pydantic models for request/response
class MetricCheck(BaseModel):
    service_name: str
    metric_name: str
    metric_value: float


class IncidentUpdate(BaseModel):
    status: str
    recovery_action: Optional[str] = None


class RecoveryRequest(BaseModel):
    incident_id: int


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "ASF-Guardian API",
        "version": "1.0.0"
    }


# Incident endpoints
@app.post("/api/incidents/check")
async def check_metric(metric: MetricCheck, background_tasks: BackgroundTasks):
    """
    Check a metric and create incident if threshold exceeded
    
    Args:
        metric: Metric information to check
        
    Returns:
        dict: Result of metric check
    """
    try:
        detector = IncidentDetector()
        incident = detector.check_metric(
            metric.service_name,
            metric.metric_name,
            metric.metric_value
        )
        detector.close()
        
        if incident:
            # Trigger auto-recovery in background
            background_tasks.add_task(trigger_auto_recovery, incident['id'])
            
            return {
                "status": "incident_created",
                "incident": incident,
                "message": "Threshold exceeded, incident created"
            }
        
        return {
            "status": "healthy",
            "message": "Metric within normal range"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/incidents")
async def get_incidents(status: Optional[str] = None, limit: int = 50):
    """
    Get all incidents
    
    Args:
        status: Filter by status (open, investigating, resolved, closed)
        limit: Maximum number of incidents to return
        
    Returns:
        list: List of incidents
    """
    try:
        detector = IncidentDetector()
        
        if status == 'open':
            incidents = detector.get_open_incidents()
        else:
            incidents = detector.get_incident_history(limit=limit)
        
        detector.close()
        return {"incidents": incidents, "count": len(incidents)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/incidents/{incident_id}")
async def get_incident(incident_id: int):
    """
    Get incident by ID
    
    Args:
        incident_id: ID of the incident
        
    Returns:
        dict: Incident details
    """
    try:
        detector = IncidentDetector()
        incident = detector.get_incident_by_id(incident_id)
        detector.close()
        
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")
        
        return incident
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/incidents/{incident_id}")
async def update_incident(incident_id: int, update: IncidentUpdate):
    """
    Update incident status
    
    Args:
        incident_id: ID of the incident
        update: Update information
        
    Returns:
        dict: Updated incident
    """
    try:
        detector = IncidentDetector()
        incident = detector.update_incident_status(
            incident_id,
            update.status,
            update.recovery_action
        )
        detector.close()
        
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")
        
        return incident
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/incidents/stats/summary")
async def get_incident_stats():
    """
    Get incident statistics
    
    Returns:
        dict: Incident statistics
    """
    try:
        detector = IncidentDetector()
        stats = detector.get_incident_stats()
        detector.close()
        
        return stats
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Recovery endpoints
@app.post("/api/recovery/attempt")
async def attempt_recovery(request: RecoveryRequest):
    """
    Manually trigger recovery for an incident
    
    Args:
        request: Recovery request with incident ID
        
    Returns:
        dict: Recovery result
    """
    try:
        recovery = AutoRecovery()
        result = recovery.attempt_recovery(request.incident_id)
        recovery.close()
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/recovery/history")
async def get_recovery_history(incident_id: Optional[int] = None):
    """
    Get recovery action history
    
    Args:
        incident_id: Optional incident ID to filter by
        
    Returns:
        dict: Recovery history
    """
    try:
        recovery = AutoRecovery()
        history = recovery.get_recovery_history(incident_id)
        recovery.close()
        
        return {"history": history, "count": len(history)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/recovery/stats")
async def get_recovery_stats():
    """
    Get recovery statistics
    
    Returns:
        dict: Recovery statistics
    """
    try:
        recovery = AutoRecovery()
        stats = recovery.get_recovery_stats()
        recovery.close()
        
        return stats
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Background task for auto-recovery
def trigger_auto_recovery(incident_id: int):
    """Background task to trigger auto-recovery"""
    try:
        recovery = AutoRecovery()
        result = recovery.attempt_recovery(incident_id)
        recovery.close()
        
        print(f"🔄 Auto-recovery triggered for incident {incident_id}: {result}")
    
    except Exception as e:
        print(f"❌ Auto-recovery failed for incident {incident_id}: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
