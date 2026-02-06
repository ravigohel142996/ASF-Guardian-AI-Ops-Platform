# ASF-Guardian Enterprise Dashboard

Professional AI Ops Platform Dashboard built with Streamlit.

## Version 2.0.0

Complete redesign with enterprise-grade UI, glassmorphism design, and modular architecture.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run dashboard/app.py
```

Access at: http://localhost:8501

## Features

### 🎨 Professional Design
- Glassmorphism UI with dark theme
- Clean, minimal, corporate aesthetic
- Responsive layout for all devices
- Smooth animations and transitions

### 📊 Dashboard Sections
1. **Dashboard Overview** - KPI cards, quick insights, recent incidents
2. **System Overview** - Health/risk charts, system load, cost analysis
3. **Incident Management** - Filterable table, status cards, timeline
4. **AI Advisor** - Chat interface, recommendations, analysis
5. **Auto-Healing** - Configuration, logs, recovery metrics
6. **Admin Panel** - Users, billing, notifications
7. **Settings** - General, security, integrations

### 🧱 Architecture

```
dashboard/
├── app.py              # Main application
├── config.py           # Configuration & constants
├── styles.css          # Custom CSS styling
├── sample_data.py      # Demo data generator
└── components/
    ├── navbar.py       # Navigation
    ├── cards.py        # KPI cards
    ├── charts.py       # Plotly visualizations
    ├── tables.py       # Data tables
    └── ai_panel.py     # AI features
```

## Configuration

### Colors & Theme

Edit `config.py` to customize:

```python
COLORS = {
    'primary': '#2196F3',      # Your primary color
    'secondary': '#00BCD4',    # Your secondary color
    'accent': '#9C27B0',       # Your accent color
    # ...
}
```

### Company Branding

Update in `config.py`:

```python
APP_CONFIG = {
    'name': 'Your Company',
    'version': '2.0.0',
    'company': 'Your Company Inc',
    'tagline': 'Your Tagline',
    'support_email': 'support@yourcompany.com'
}
```

## Demo Mode

The dashboard includes sample data generators and runs standalone without requiring the backend API. Perfect for:
- Demos and presentations
- UI development
- Testing layouts

## Production Mode

To connect to the backend API:

1. Set environment variable:
   ```bash
   export API_URL=https://your-api-domain.com
   ```

2. Or create `.env` file:
   ```env
   API_URL=https://your-api-domain.com
   ```

3. Restart the dashboard

## Components

### KPI Cards
Professional metric cards with:
- Large icons
- Trend indicators
- Hover effects
- Glassmorphism styling

### Charts
Interactive Plotly visualizations:
- Line charts (health vs risk)
- Area charts (system load)
- Bar charts (costs)
- Pie charts (distribution)
- Gauges (success rates)
- Heatmaps (service health)

### Tables
Professional data tables with:
- Severity badges
- Status indicators
- Filters and search
- Sortable columns
- Responsive design

### AI Panel
Intelligent features:
- Chat interface with history
- Recommendation cards
- Quick insights
- Incident analysis

## Customization

### Adding New Pages

1. Add page logic in `app.py`:
```python
elif selected_page == "your_page":
    st.markdown('<div class="section-header">Your Page</div>', unsafe_allow_html=True)
    # Your page content
```

2. Add navigation in `components/navbar.py`:
```python
pages = {
    "🔧 Your Page": "your_page",
    # ...
}
```

### Custom Styling

Edit `styles.css` to modify:
- Colors (CSS variables)
- Spacing and layout
- Typography
- Animations
- Component styles

### Sample Data

Modify `sample_data.py` to adjust:
- Metric ranges
- Incident types
- User data
- Cost values

## Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Performance

- Modular components for efficient rendering
- Sample data cached during session
- Optimized chart rendering
- Minimal dependencies

## Deployment

See [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md) for:
- Streamlit Cloud
- Docker
- AWS/Azure
- Self-hosted server

## Documentation

- [Setup Guide](../SETUP_GUIDE.md) - Detailed setup instructions
- [Deployment Guide](../DEPLOYMENT_GUIDE.md) - Production deployment
- [Config Reference](config.py) - Configuration options
- [Component Guide](components/) - Component documentation

## Troubleshooting

### Port Already in Use
```bash
streamlit run dashboard/app.py --server.port 8502
```

### CSS Not Loading
```bash
streamlit cache clear
```

### Import Errors
```bash
pip install -r requirements.txt --upgrade
```

## Support

- GitHub Issues: [Report a bug](https://github.com/ravigohel142996/ASF-Guardian-AI-Ops-Platform/issues)
- Email: support@asf-guardian.com

## License

MIT License - See LICENSE file for details

---

**Built with ❤️ for the DevOps Community**
