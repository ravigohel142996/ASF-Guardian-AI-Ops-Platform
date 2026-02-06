# ASF-Guardian Enterprise Dashboard Deployment Guide

## Deployment Options

This guide covers multiple deployment strategies for the ASF-Guardian Enterprise Dashboard.

## Table of Contents

1. [Streamlit Cloud (Recommended for Dashboard)](#streamlit-cloud)
2. [Docker Deployment](#docker-deployment)
3. [AWS Deployment](#aws-deployment)
4. [Azure Deployment](#azure-deployment)
5. [Self-Hosted Server](#self-hosted-server)

---

## Streamlit Cloud

The easiest way to deploy the dashboard is using Streamlit Cloud.

### Prerequisites

- GitHub account
- Streamlit Cloud account (free tier available)

### Steps

1. **Fork/Clone Repository** to your GitHub account

2. **Sign in to Streamlit Cloud**
   - Go to https://streamlit.io/cloud
   - Sign in with GitHub

3. **Create New App**
   - Click "New app"
   - Select your repository
   - Branch: `main` or your feature branch
   - Main file path: `dashboard/app.py`

4. **Configure Secrets**
   
   Add secrets in Streamlit Cloud dashboard (Settings > Secrets):
   
   ```toml
   # API Configuration (optional)
   API_URL = "https://your-backend-api.com"
   
   # OpenAI (optional, for AI features)
   OPENAI_API_KEY = "sk-..."
   ```

5. **Deploy**
   - Click "Deploy"
   - Your app will be live at: `https://your-app-name.streamlit.app`

### Advantages
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Auto-deploys on git push
- ✅ Easy secrets management
- ✅ Built-in analytics

---

## Docker Deployment

### Dockerfile

Create `Dockerfile` in the project root:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run Streamlit
ENTRYPOINT ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  dashboard:
    build: .
    ports:
      - "8501:8501"
    environment:
      - API_URL=http://backend:8000
    volumes:
      - ./dashboard:/app/dashboard
    depends_on:
      - backend
      - redis
    networks:
      - asf-network

  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./asf_guardian.db
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ./backend:/app/backend
      - ./database:/app/database
    networks:
      - asf-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - asf-network

  celery-worker:
    build: .
    command: celery -A workers.monitor worker --loglevel=info
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    networks:
      - asf-network

networks:
  asf-network:
    driver: bridge
```

### Build and Run

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f dashboard

# Stop services
docker-compose down
```

Access the dashboard at: `http://localhost:8501`

---

## AWS Deployment

### Option 1: AWS Elastic Beanstalk

1. **Install EB CLI:**
```bash
pip install awsebcli
```

2. **Initialize EB:**
```bash
eb init -p python-3.10 asf-guardian-dashboard
```

3. **Create Environment:**
```bash
eb create asf-guardian-prod
```

4. **Deploy:**
```bash
eb deploy
```

5. **Open in Browser:**
```bash
eb open
```

### Option 2: AWS ECS (Fargate)

1. **Build and Push Docker Image:**
```bash
# Tag image
docker tag asf-guardian-dashboard:latest <your-ecr-repo>:latest

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <your-ecr-repo>

# Push image
docker push <your-ecr-repo>:latest
```

2. **Create ECS Task Definition:**
```json
{
  "family": "asf-guardian-dashboard",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "dashboard",
      "image": "<your-ecr-repo>:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ]
    }
  ]
}
```

3. **Create ECS Service with Load Balancer**

---

## Azure Deployment

### Azure App Service

1. **Create App Service:**
```bash
az webapp create \
  --resource-group asf-guardian-rg \
  --plan asf-guardian-plan \
  --name asf-guardian-dashboard \
  --runtime "PYTHON:3.10"
```

2. **Configure Deployment:**
```bash
az webapp config appsettings set \
  --resource-group asf-guardian-rg \
  --name asf-guardian-dashboard \
  --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

3. **Deploy:**
```bash
az webapp up --name asf-guardian-dashboard
```

---

## Self-Hosted Server

### Requirements

- Ubuntu 20.04+ or CentOS 8+
- Python 3.10+
- Nginx
- SSL certificate (Let's Encrypt recommended)

### Installation Steps

1. **Install Dependencies:**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx certbot python3-certbot-nginx
```

2. **Clone Repository:**
```bash
cd /opt
sudo git clone https://github.com/ravigohel142996/ASF-Guardian-AI-Ops-Platform.git
cd ASF-Guardian-AI-Ops-Platform
```

3. **Create Virtual Environment:**
```bash
sudo python3 -m venv venv
sudo ./venv/bin/pip install -r requirements.txt
```

4. **Create Systemd Service:**

Create `/etc/systemd/system/asf-guardian-dashboard.service`:

```ini
[Unit]
Description=ASF-Guardian Dashboard
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/ASF-Guardian-AI-Ops-Platform
Environment="PATH=/opt/ASF-Guardian-AI-Ops-Platform/venv/bin"
ExecStart=/opt/ASF-Guardian-AI-Ops-Platform/venv/bin/streamlit run dashboard/app.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

5. **Enable and Start Service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable asf-guardian-dashboard
sudo systemctl start asf-guardian-dashboard
```

6. **Configure Nginx:**

Create `/etc/nginx/sites-available/asf-guardian`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

7. **Enable Site:**
```bash
sudo ln -s /etc/nginx/sites-available/asf-guardian /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

8. **Setup SSL:**
```bash
sudo certbot --nginx -d your-domain.com
```

---

## Production Best Practices

### Security

1. **Environment Variables**
   - Never commit secrets to git
   - Use environment variables or secret managers
   - Rotate API keys regularly

2. **HTTPS**
   - Always use HTTPS in production
   - Use valid SSL certificates
   - Enable HSTS headers

3. **Authentication**
   - Implement user authentication
   - Use OAuth or SSO if possible
   - Enable session management

### Performance

1. **Caching**
   - Enable Streamlit caching for expensive operations
   - Use Redis for distributed caching
   - Implement CDN for static assets

2. **Monitoring**
   - Set up application monitoring (New Relic, Datadog)
   - Configure log aggregation (ELK stack, CloudWatch)
   - Enable health checks

3. **Scaling**
   - Use load balancer for multiple instances
   - Implement auto-scaling based on traffic
   - Optimize database queries

### Backup

1. **Database Backups**
   - Automated daily backups
   - Store in different region/cloud
   - Test restore procedures

2. **Configuration Backups**
   - Version control all configurations
   - Document environment setup
   - Maintain rollback procedures

---

## Monitoring and Maintenance

### Health Checks

Monitor these endpoints:
- Dashboard: `https://your-domain.com/_stcore/health`
- Backend API: `https://your-api-domain.com/health`

### Logs

View application logs:
```bash
# Systemd service
sudo journalctl -u asf-guardian-dashboard -f

# Docker
docker-compose logs -f dashboard

# Streamlit Cloud
Check logs in Streamlit Cloud dashboard
```

### Updates

Deploy updates:
```bash
# Pull latest code
git pull origin main

# Restart service
sudo systemctl restart asf-guardian-dashboard

# Or for Docker
docker-compose up -d --build
```

---

## Troubleshooting

### Common Issues

1. **Port Conflicts**
   - Change port in deployment configuration
   - Check for other services using port 8501

2. **Memory Issues**
   - Increase container memory limits
   - Optimize data loading and caching

3. **Connection Timeouts**
   - Increase proxy timeout settings
   - Configure WebSocket support

### Getting Help

- Documentation: https://github.com/ravigohel142996/ASF-Guardian-AI-Ops-Platform
- Issues: https://github.com/ravigohel142996/ASF-Guardian-AI-Ops-Platform/issues
- Email: support@asf-guardian.com

---

**Production deployment requires careful planning. Always test in staging before deploying to production!**
