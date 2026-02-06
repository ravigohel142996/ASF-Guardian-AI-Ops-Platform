# ASF-Guardian 🚀

**Enterprise AI Incident & Auto-Healing Platform**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Overview

ASF-Guardian is a production-ready, enterprise-grade AI Ops platform that combines intelligent incident detection, automated recovery, and AI-powered advisory capabilities to minimize downtime and maximize system reliability.

## ✨ Features

### 🔍 Incident Detection Engine
- Real-time system monitoring (CPU, Memory, Disk, Response Time)
- Intelligent threshold-based alerting
- Multi-service monitoring support
- Automatic severity classification

### 🔄 Auto-Recovery System
- Automated incident resolution
- Multiple recovery strategies per incident type
- Success tracking and reporting
- Configurable recovery actions

### 📊 Incident History Database
- Complete incident lifecycle tracking
- Historical trend analysis
- SQLite/Supabase support
- Advanced filtering and search

### 📧 Email Alert System
- Real-time incident notifications
- Beautiful HTML email templates
- Severity-based alerting
- Daily summary reports

### 🤖 AI Advisor Chatbot
- OpenAI-powered intelligent assistance
- Root cause analysis
- Recovery recommendations
- Best practices guidance

### 🚀 REST API (FastAPI)
- RESTful architecture
- Comprehensive API documentation (Swagger/OpenAPI)
- Authentication ready
- CORS enabled

### ⚙️ Background Workers
- Celery-based task queue
- Scheduled health checks
- Async incident processing
- Redis-backed job management

### 📈 Admin Panel & SaaS Dashboard
- Modern, responsive UI built with Streamlit
- Real-time metrics and charts
- Interactive incident management
- AI chat interface
- Advanced analytics

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **Backend API** | FastAPI |
| **Database** | SQLite / Supabase |
| **Task Queue** | Celery + Redis |
| **AI** | OpenAI API |
| **Email** | SMTP |
| **Deployment** | Render + Streamlit Cloud |
| **Monitoring** | psutil |

## 📁 Project Structure

```
ASF-Guardian/
│
├── backend/              # FastAPI backend
│   ├── api.py           # REST API endpoints
│   ├── incidents.py     # Incident detection logic
│   └── recovery.py      # Auto-recovery system
│
├── dashboard/           # Streamlit frontend
│   ├── app.py          # Main dashboard app
│   └── monitor.py      # UI components
│
├── ai_advisor/          # AI capabilities
│   └── chatbot.py      # OpenAI-powered advisor
│
├── workers/             # Background tasks
│   └── monitor.py      # Celery workers
│
├── database/            # Data models
│   └── models.py       # SQLAlchemy models
│
├── alerts/              # Notification system
│   └── mailer.py       # Email alerts
│
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── deploy.md           # Deployment guide
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Redis server
- OpenAI API key (for AI features)
- SMTP server access (for email alerts)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ravigohel142996/ASF-Guardian-AI-Ops-Platform.git
cd ASF-Guardian-AI-Ops-Platform
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**

Create a `.env` file in the root directory:
```env
# OpenAI
OPENAI_API_KEY=your_openai_api_key

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
ALERT_EMAIL=admin@company.com

# Redis
REDIS_URL=redis://localhost:6379/0

# Database
DATABASE_URL=sqlite:///./asf_guardian.db
```

5. **Initialize database**
```bash
python -c "from database.models import init_db; init_db()"
```

6. **Start the services**

**Terminal 1 - Backend API:**
```bash
cd backend
uvicorn api:app --reload --port 8000
```

**Terminal 2 - Celery Worker:**
```bash
celery -A workers.monitor worker --loglevel=info
```

**Terminal 3 - Celery Beat (Scheduler):**
```bash
celery -A workers.monitor beat --loglevel=info
```

**Terminal 4 - Dashboard:**
```bash
streamlit run dashboard/app.py
```

7. **Access the application**
- Dashboard: http://localhost:8501
- API Docs: http://localhost:8000/docs
- API Health: http://localhost:8000/health

## 📖 Usage

### Creating Test Incidents

Use the dashboard's "Create Test Incident" feature or call the API directly:

```bash
curl -X POST "http://localhost:8000/api/incidents/check" \
  -H "Content-Type: application/json" \
  -d '{
    "service_name": "web-api",
    "metric_name": "cpu",
    "metric_value": 95.5
  }'
```

### Triggering Manual Recovery

```bash
curl -X POST "http://localhost:8000/api/recovery/attempt" \
  -H "Content-Type: application/json" \
  -d '{"incident_id": 1}'
```

### Chatting with AI Advisor

Use the dashboard's AI Advisor page or integrate with your own client using the AIAdvisor class.

## 🎯 Key Capabilities

### Incident Detection
- Monitors system metrics continuously
- Compares against configurable thresholds
- Creates incidents automatically
- Classifies severity intelligently

### Auto-Recovery
- Attempts recovery automatically
- Multiple strategies per incident type
- Tracks success rates
- Learns from historical data

### AI Advisory
- Provides root cause analysis
- Suggests remediation steps
- Offers preventive recommendations
- Answers DevOps questions

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/incidents` | GET | List all incidents |
| `/api/incidents/{id}` | GET | Get incident details |
| `/api/incidents/check` | POST | Check metric and create incident |
| `/api/incidents/stats/summary` | GET | Get incident statistics |
| `/api/recovery/attempt` | POST | Trigger manual recovery |
| `/api/recovery/history` | GET | Get recovery history |
| `/api/recovery/stats` | GET | Get recovery statistics |

Full API documentation available at `/docs` when the backend is running.

## 🌐 Deployment

See [deploy.md](deploy.md) for detailed deployment instructions for:
- Render (Backend API)
- Streamlit Cloud (Dashboard)
- Redis hosting options
- Production configuration

## 🔒 Security

- Environment variables for sensitive data
- HTTPS in production
- CORS configuration
- Input validation
- SQL injection protection

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Ravi Gohel**

- GitHub: [@ravigohel142996](https://github.com/ravigohel142996)
- LinkedIn: [Ravi Gohel](https://linkedin.com/in/ravigohel142996)

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- Streamlit for the beautiful dashboard capabilities
- OpenAI for AI-powered features
- Celery for robust task queuing

## 📞 Support

For support, email ravigohel142996@gmail.com or open an issue on GitHub.

---

**⭐ If you find this project useful, please consider giving it a star on GitHub! ⭐**

Built with ❤️ for the DevOps community
