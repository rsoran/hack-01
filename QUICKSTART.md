# Quick Start Guide

## ⚡ Get Running in 2 Minutes

### With Docker (Recommended)

```bash
# 1. Set your API key
# Edit .env file and add your Google API key

# 2. Start the app
docker-compose up -d

# 3. Open browser
# http://localhost:5000
```

### Without Docker (Local Development)

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate (Windows)

# 2. Install dependencies
cd backend
pip install -r requirements.txt

# 3. Set API key
# Edit ../.env file

# 4. Run server
python app.py

# 5. Open browser
# http://localhost:5000
```

## 📋 File Structure

```
├── backend/              # Python Flask API
│   ├── app.py           # Main application
│   ├── meal_planner.py  # AI logic
│   ├── config.py        # Configuration
│   └── requirements.txt # Dependencies
│
├── frontend/            # Web UI
│   ├── index.html       # HTML
│   ├── styles.css       # Styling
│   └── script.js        # JavaScript
│
├── Dockerfile           # Container image
├── docker-compose.yml   # Container orchestration
├── nginx.conf           # Reverse proxy config
├── .env                 # Environment variables
└── readme.md            # Full documentation
```

## 🔑 Required Configuration

1. Get Google API Key:
   - Visit: https://makersuite.google.com/app/apikey
   - Create a new API key
   - Copy it

2. Update `.env`:
   ```
   GOOGLE_API_KEY=your-key-here
   ```

## 🧪 Test It

Once running, visit: `http://localhost:5000`

Then:
1. Describe your day in the text area
2. Select preferences (optional)
3. Set budget (optional)
4. Click "Generate Meal Plan"

## 🐛 Troubleshooting

**Port 5000 already in use?**
```bash
# Change port in docker-compose.yml
ports:
  - "8000:5000"  # Use 8000 instead
```

**API key not working?**
- Verify at: https://console.cloud.google.com/
- Make sure Generative AI API is enabled

**Docker issues?**
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up
```

## 📝 Features

✅ AI-powered meal planning
✅ Grocery list generation
✅ Budget analysis
✅ Alternative suggestions
✅ Print/Download support
✅ Mobile responsive
✅ Production-ready Docker setup

## 🚀 Deploy to Production

See full README.md for:
- Kubernetes deployment
- Environment-specific configs
- SSL/HTTPS setup
- Performance optimization
- Security best practices

---

Need help? See `readme.md` for comprehensive documentation.
