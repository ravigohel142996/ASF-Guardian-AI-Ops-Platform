# 🚀 Quick Start Guide - ASF-Guardian

Get ASF-Guardian up and running in 5 minutes!

## Prerequisites
- Python 3.9 or higher
- Git

## Installation (3 Steps)

### 1️⃣ Clone and Setup
```bash
git clone https://github.com/ravigohel142996/ASF-Guardian-AI-Ops-Platform.git
cd ASF-Guardian-AI-Ops-Platform
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2️⃣ Initialize Database
```bash
python setup.py
```

### 3️⃣ Start the Platform
```bash
# Terminal 1 - Backend API
cd backend
uvicorn api:app --reload --port 8000

# Terminal 2 - Dashboard (in new terminal)
streamlit run dashboard/app.py
```

That's it! 🎉

## Access Points

- **Dashboard**: http://localhost:8501
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## First Steps

1. **Dashboard Home** - View system overview and metrics
2. **Create Test Incident** - Go to "Incidents" tab → "Create Test Incident"
3. **Watch Auto-Recovery** - See the system automatically attempt recovery
4. **Try AI Advisor** - Ask questions in the AI Advisor tab

## Optional Configuration

For full features, create a `.env` file:

```env
# OpenAI API (for AI Advisor)
OPENAI_API_KEY=your_key_here

# Email Alerts (for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
ALERT_EMAIL=admin@example.com

# Redis (for background workers)
REDIS_URL=redis://localhost:6379/0
```

## Background Workers (Optional)

For automated monitoring:

```bash
# Terminal 3 - Celery Worker
celery -A workers.monitor worker --loglevel=info

# Terminal 4 - Celery Beat (Scheduler)
celery -A workers.monitor beat --loglevel=info
```

## Testing

Run the test suite:
```bash
python test_platform.py
```

## Demo Features

### Without Configuration
✅ Incident detection and creation
✅ Manual recovery actions
✅ REST API
✅ Dashboard with charts
✅ Incident history

### With OpenAI API Key
✅ AI-powered incident analysis
✅ Recovery recommendations
✅ ChatGPT-style advisor

### With SMTP + Redis
✅ Email alerts
✅ Automated monitoring
✅ Background recovery

## Common Issues

### Port Already in Use
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn backend.api:app --port 8001
```

### Module Not Found
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Database Errors
```bash
# Reinitialize database
rm asf_guardian.db
python setup.py
```

## Next Steps

1. 📖 Read [README.md](README.md) for detailed features
2. 🚀 See [deploy.md](deploy.md) for production deployment
3. 🔧 Customize thresholds in the Settings page
4. 📊 Explore Analytics for trends and insights

## Need Help?

- 📧 Email: ravigohel142996@gmail.com
- 💬 GitHub Issues: [Report a bug](https://github.com/ravigohel142996/ASF-Guardian-AI-Ops-Platform/issues)
- 📚 Full Docs: [README.md](README.md)

---

**Happy Monitoring! 🛡️**
