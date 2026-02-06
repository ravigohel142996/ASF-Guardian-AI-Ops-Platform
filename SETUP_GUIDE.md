# ASF-Guardian Enterprise Dashboard Setup Guide

## Overview

This guide will help you set up and run the ASF-Guardian Enterprise Dashboard locally or in production.

## Prerequisites

- Python 3.9 or higher
- pip package manager
- Git (for cloning the repository)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ravigohel142996/ASF-Guardian-AI-Ops-Platform.git
cd ASF-Guardian-AI-Ops-Platform
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Dashboard

### Standalone Dashboard (Demo Mode)

The dashboard includes sample data generators and can run independently without the backend API:

```bash
streamlit run dashboard/app.py
```

The dashboard will be available at: **http://localhost:8501**

### With Backend API

To connect the dashboard to the full backend system:

1. **Start the Backend API:**
```bash
cd backend
uvicorn api:app --reload --port 8000
```

2. **Start Redis (for background tasks):**
```bash
redis-server
```

3. **Start Celery Worker:**
```bash
celery -A workers.monitor worker --loglevel=info
```

4. **Start Celery Beat (Scheduler):**
```bash
celery -A workers.monitor beat --loglevel=info
```

5. **Start the Dashboard:**
```bash
streamlit run dashboard/app.py
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# API Configuration
API_URL=http://localhost:8000

# OpenAI (for AI Advisor)
OPENAI_API_KEY=your_openai_api_key

# Email Alerts
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

### Customizing the Dashboard

#### Colors and Theme

Edit `dashboard/config.py` to customize colors:

```python
COLORS = {
    'primary': '#2196F3',      # Change primary color
    'secondary': '#00BCD4',     # Change secondary color
    'accent': '#9C27B0',        # Change accent color
    # ... more colors
}
```

#### Company Information

Update company details in `dashboard/config.py`:

```python
APP_CONFIG = {
    'name': 'Your Company Name',
    'version': '2.0.0',
    'company': 'Your Company',
    'tagline': 'Your Tagline',
    'support_email': 'support@yourcompany.com'
}
```

#### Custom Styling

Modify `dashboard/styles.css` to adjust the visual appearance:

```css
:root {
    --primary-color: #2196F3;  /* Your primary color */
    --bg-primary: #0A1929;      /* Background color */
    /* ... more CSS variables */
}
```

## Dashboard Features

### Pages

1. **Dashboard** - Overview with KPI cards and quick insights
2. **System Overview** - Detailed charts for health, load, and costs
3. **Incident Management** - View and filter incidents with advanced search
4. **AI Advisor** - Chat interface with AI-powered recommendations
5. **Auto-Healing** - Configure recovery rules and view logs
6. **Admin Panel** - User management, billing, and notifications
7. **Settings** - General settings, security, and integrations

### Key Components

- **KPI Cards** - Real-time metrics with glass-morphism design
- **Charts** - Interactive Plotly visualizations
- **Tables** - Sortable, filterable data tables
- **AI Chat** - Intelligent incident analysis and recommendations
- **Recovery Logs** - Audit trail of auto-healing actions

## Troubleshooting

### Port Already in Use

If port 8501 is already in use, specify a different port:

```bash
streamlit run dashboard/app.py --server.port 8502
```

### Module Not Found Errors

Ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### CSS Not Loading

Clear Streamlit cache:

```bash
streamlit cache clear
```

Or delete the cache directory:
```bash
rm -rf ~/.streamlit/cache
```

### API Connection Issues

1. Verify the backend API is running: `http://localhost:8000/health`
2. Check the `API_URL` environment variable
3. Review firewall/network settings

## Performance Optimization

### For Large Deployments

1. **Enable Caching:**
   - Sample data is generated on each page load by default
   - In production, connect to real API endpoints for better performance

2. **Database Optimization:**
   - Use PostgreSQL instead of SQLite for production
   - Add proper indexes on frequently queried fields

3. **Streamlit Configuration:**
   
   Create `.streamlit/config.toml`:
   
   ```toml
   [server]
   maxUploadSize = 200
   enableCORS = false
   enableXsrfProtection = true
   
   [theme]
   base = "dark"
   
   [browser]
   gatherUsageStats = false
   ```

## Browser Compatibility

The dashboard is optimized for modern browsers:

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Mobile Support

The dashboard is responsive and works on tablets and mobile devices (landscape mode recommended for best experience).

## Next Steps

- Review the [Deployment Guide](DEPLOYMENT_GUIDE.md) for production deployment
- Check the [API Documentation](http://localhost:8000/docs) for backend integration
- Explore [Customization Options](dashboard/config.py) to brand the dashboard

## Support

For issues or questions:
- Email: support@asf-guardian.com
- GitHub Issues: https://github.com/ravigohel142996/ASF-Guardian-AI-Ops-Platform/issues
- Documentation: https://github.com/ravigohel142996/ASF-Guardian-AI-Ops-Platform

---

**Built with ❤️ for the DevOps Community**
