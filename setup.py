#!/usr/bin/env python3
"""
Setup script for ASF-Guardian
Initializes database and generates demo data
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.models import init_db
from backend.incidents import generate_demo_incidents


def setup():
    """Initialize ASF-Guardian platform"""
    print("🚀 Setting up ASF-Guardian...")
    print()
    
    # Step 1: Initialize database
    print("📊 Step 1: Initializing database...")
    try:
        init_db()
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize database: {str(e)}")
        return False
    
    print()
    
    # Step 2: Generate demo data
    print("📝 Step 2: Generating demo data...")
    try:
        generate_demo_incidents()
        print("✅ Demo data generated successfully!")
    except Exception as e:
        print(f"❌ Failed to generate demo data: {str(e)}")
        return False
    
    print()
    print("=" * 60)
    print("✅ ASF-Guardian setup completed successfully!")
    print("=" * 60)
    print()
    print("🎯 Next steps:")
    print()
    print("1. Configure your .env file (copy from .env.example)")
    print("2. Start the backend API:")
    print("   cd backend && uvicorn api:app --reload")
    print()
    print("3. Start the dashboard:")
    print("   streamlit run dashboard/app.py")
    print()
    print("4. (Optional) Start Celery worker:")
    print("   celery -A workers.monitor worker --loglevel=info")
    print()
    print("📚 For more details, see deploy.md")
    print()
    
    return True


if __name__ == "__main__":
    success = setup()
    sys.exit(0 if success else 1)
