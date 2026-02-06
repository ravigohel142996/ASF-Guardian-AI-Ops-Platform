# 🚀 ASF-Guardian Deployment Guide

## Prerequisites
- Python 3.9+
- OpenAI API Key
- Redis Server (for Celery)
- SMTP Server Access (for email alerts)

## 📦 Installation Steps

### 1. Clone Repository
```bash
git clone https://github.com/ravigohel142996/ASF-Guardian-AI-Ops-Platform.git
cd ASF-Guardian-AI-Ops-Platform
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
ALERT_EMAIL=admin@company.com

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Database
DATABASE_URL=sqlite:///./asf_guardian.db
```

### 5. Initialize Database
```bash
python -c "from database.models import init_db; init_db()"
```

## 🎯 Running the Application

### Start Backend API (Terminal 1)
```bash
cd backend
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### Start Celery Worker (Terminal 2)
```bash
celery -A workers.monitor worker --loglevel=info
```

### Start Celery Beat (Terminal 3)
```bash
celery -A workers.monitor beat --loglevel=info
```

### Start Dashboard (Terminal 4)
```bash
streamlit run dashboard/app.py --server.port 8501
```

## 🌐 Access Points

- **Dashboard**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

## ☁️ Cloud Deployment

### Deploy Backend on Render

1. Create new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Configure build settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.api:app --host 0.0.0.0 --port $PORT`
4. Add environment variables from `.env`
5. Deploy!

### Deploy Dashboard on Streamlit Cloud

1. Visit [Streamlit Cloud](https://streamlit.io/cloud)
2. Connect your GitHub repository
3. Set main file path: `dashboard/app.py`
4. Add secrets in Streamlit Cloud settings (same as `.env`)
5. Deploy!

### Redis Setup

For production, use:
- **Render Redis** (free tier available)
- **Redis Labs** (free tier available)
- **Upstash** (serverless Redis)

## 🔒 Security Notes

1. Never commit `.env` file to git
2. Use strong passwords for SMTP
3. Rotate API keys regularly
4. Use HTTPS in production
5. Set up proper CORS policies

## 📊 Monitoring

Once deployed, monitor:
- API response times in Render dashboard
- Celery task queues in Redis
- Application logs in respective platforms
- Database size and performance

## 🆘 Troubleshooting

### Celery not connecting to Redis
- Check Redis URL in `.env`
- Ensure Redis server is running
- Verify network connectivity

### Email alerts not sending
- Verify SMTP credentials
- Check firewall/security settings
- Use app-specific passwords for Gmail

### Database errors
- Ensure database is initialized
- Check file permissions for SQLite
- Verify DATABASE_URL is correct

## 🔄 Updates

To update the application:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
python -c "from database.models import init_db; init_db()"
# Restart all services
```

## 📞 Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/ravigohel142996/ASF-Guardian-AI-Ops-Platform/issues)
- Email: support@asfguardian.com

---

Built with ❤️ by Ravi
