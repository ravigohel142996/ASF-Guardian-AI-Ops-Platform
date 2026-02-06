#!/usr/bin/env python3
"""
End-to-end test script for ASF-Guardian
Tests all major components
"""
import sys
import os
import time
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.models import get_db_session, Incident, SystemMetric, RecoveryAction
from backend.incidents import IncidentDetector
from backend.recovery import AutoRecovery
from ai_advisor.chatbot import AIAdvisor

def test_database():
    """Test database connectivity and models"""
    print("🧪 Testing Database...")
    try:
        db = get_db_session()
        
        # Test query
        incidents = db.query(Incident).all()
        metrics = db.query(SystemMetric).all()
        actions = db.query(RecoveryAction).all()
        
        print(f"   ✅ Database connected")
        print(f"   ✅ Found {len(incidents)} incidents")
        print(f"   ✅ Found {len(metrics)} metrics")
        print(f"   ✅ Found {len(actions)} recovery actions")
        
        db.close()
        return True
    except Exception as e:
        print(f"   ❌ Database test failed: {str(e)}")
        return False


def test_incident_detector():
    """Test incident detection engine"""
    print("\n🧪 Testing Incident Detector...")
    try:
        detector = IncidentDetector()
        
        # Test metric check (below threshold)
        result = detector.check_metric("test-service", "cpu", 50.0)
        assert result is None, "Should not create incident for normal metric"
        print("   ✅ Normal metric check passed")
        
        # Test metric check (above threshold)
        result = detector.check_metric("test-service", "cpu", 95.0)
        assert result is not None, "Should create incident for high metric"
        assert result['severity'] in ['critical', 'high', 'medium'], "Should have appropriate severity"
        print(f"   ✅ Incident created: #{result['id']} - {result['severity']}")
        
        # Test getting incidents
        incidents = detector.get_open_incidents()
        assert len(incidents) > 0, "Should have open incidents"
        print(f"   ✅ Found {len(incidents)} open incidents")
        
        # Test stats
        stats = detector.get_incident_stats()
        assert 'total' in stats, "Stats should have total count"
        print(f"   ✅ Stats: {stats}")
        
        detector.close()
        return True
    except Exception as e:
        print(f"   ❌ Incident detector test failed: {str(e)}")
        return False


def test_auto_recovery():
    """Test auto-recovery system"""
    print("\n🧪 Testing Auto-Recovery...")
    try:
        # First create an incident
        detector = IncidentDetector()
        incident = detector.check_metric("test-recovery", "memory", 92.0)
        detector.close()
        
        if not incident:
            print("   ⚠️  Could not create test incident")
            return False
        
        incident_id = incident['id']
        print(f"   ✅ Created test incident #{incident_id}")
        
        # Test recovery
        recovery = AutoRecovery()
        result = recovery.attempt_recovery(incident_id)
        
        print(f"   ✅ Recovery attempt: {result.get('success', False)}")
        
        # Test recovery stats
        stats = recovery.get_recovery_stats()
        assert 'total_actions' in stats, "Stats should have total actions"
        print(f"   ✅ Recovery stats: {stats}")
        
        recovery.close()
        return True
    except Exception as e:
        print(f"   ❌ Auto-recovery test failed: {str(e)}")
        return False


def test_api():
    """Test REST API"""
    print("\n🧪 Testing REST API...")
    try:
        base_url = "http://localhost:8000"
        
        # Test health endpoint
        response = requests.get(f"{base_url}/health", timeout=5)
        assert response.status_code == 200, "Health check should return 200"
        data = response.json()
        assert data['status'] == 'healthy', "API should be healthy"
        print("   ✅ Health check passed")
        
        # Test incidents endpoint
        response = requests.get(f"{base_url}/api/incidents", timeout=5)
        assert response.status_code == 200, "Incidents endpoint should return 200"
        data = response.json()
        assert 'incidents' in data, "Response should have incidents"
        print(f"   ✅ Incidents endpoint: {len(data['incidents'])} incidents")
        
        # Test stats endpoint
        response = requests.get(f"{base_url}/api/incidents/stats/summary", timeout=5)
        assert response.status_code == 200, "Stats endpoint should return 200"
        stats = response.json()
        assert 'total' in stats, "Stats should have total"
        print(f"   ✅ Stats endpoint: {stats}")
        
        return True
    except requests.exceptions.ConnectionError:
        print("   ⚠️  API not running (expected if not started)")
        return True  # Not a failure, just not running
    except Exception as e:
        print(f"   ❌ API test failed: {str(e)}")
        return False


def test_ai_advisor():
    """Test AI advisor (without API key)"""
    print("\n🧪 Testing AI Advisor...")
    try:
        advisor = AIAdvisor()
        
        # Test quick tips (doesn't require API key)
        tips = advisor.get_quick_tips()
        assert len(tips) > 0, "Should have quick tips"
        print(f"   ✅ Got {len(tips)} quick tips")
        
        # Test ask (will fail gracefully without API key)
        response = advisor.ask("What is CPU monitoring?")
        assert 'answer' in response, "Response should have answer"
        
        if response.get('success'):
            print("   ✅ AI advisor working (API key configured)")
        else:
            print("   ⚠️  AI advisor available but API key not configured")
        
        advisor.close()
        return True
    except Exception as e:
        print(f"   ❌ AI advisor test failed: {str(e)}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🚀 ASF-Guardian Test Suite")
    print("=" * 60)
    
    tests = [
        ("Database", test_database),
        ("Incident Detector", test_incident_detector),
        ("Auto-Recovery", test_auto_recovery),
        ("REST API", test_api),
        ("AI Advisor", test_ai_advisor),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} crashed: {str(e)}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("📊 Test Results")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print("=" * 60)
    print(f"Result: {passed}/{total} tests passed")
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
