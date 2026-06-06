# 🍳 Cooking To-Do List Generator

A simple AI-powered micro-app that helps users generate personalized cooking to-do lists based on their day. Built with Flask backend and vanilla JavaScript frontend, fully containerized with Docker.

## Features

- 🤖 **AI-Powered Meal Planning**: Uses Google Generative AI (Gemini) to generate personalized meal plans
- 🥣 **Structured Meal Planning**: Generates breakfast, lunch, and dinner plans tailored to your day
- 📋 **Smart Grocery List**: Automatically generates and organizes grocery lists
- 💰 **Budget Analysis**: Analyzes meal feasibility within your budget
- 🔄 **Alternative Substitutions**: Suggests healthy alternatives for ingredients
- 📱 **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- 🐳 **Docker Ready**: Fully containerized for easy deployment

## Project Structure

```
Cooking-TODO/
├── backend/
│   ├── app.py              # Flask application entry point
│   ├── config.py           # Configuration management
│   ├── meal_planner.py     # AI meal planning logic
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── styles.css          # Styling
│   └── script.js           # Frontend logic
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker Compose configuration
├── nginx.conf              # Nginx reverse proxy configuration
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── .dockerignore           # Docker build ignore rules
└── README.md               # This file
```

## Prerequisites

### For Local Development
- Python 3.11 or higher
- pip (Python package manager)

### For Docker
- Docker
- Docker Compose (optional but recommended)

## Quick Start

### Option 1: Local Development

#### 1. Clone/Navigate to the project
```bash
cd path/to/Cooking-TODO
```

#### 2. Create environment file
```bash
cp .env.example .env
```

#### 3. Update `.env` with your configuration
```bash
# Get your Google API key from: https://makersuite.google.com/app/apikey
FLASK_ENV=development
GOOGLE_API_KEY=your-google-api-key-here
SECRET_KEY=your-secret-key
```

#### 4. Set up Python virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 5. Install dependencies
```bash
cd backend
pip install -r requirements.txt
cd ..
```

#### 6. Run the application
```bash
cd backend
python app.py
```

The application will start at `http://localhost:5000`

#### 7. Open in browser
Navigate to `http://localhost:5000` to access the frontend

---

### Option 2: Docker (Recommended for Production)

#### 1. Create environment file
```bash
cp .env.example .env
```

#### 2. Update `.env` with your configuration
```bash
GOOGLE_API_KEY=your-google-api-key-here
SECRET_KEY=your-secret-key
```

#### 3. Build and run with Docker Compose
```bash
docker-compose up -d
```

#### 4. Access the application
- Frontend: `http://localhost:5000` (via Nginx proxy)
- API: `http://localhost:5000/api/`
- Backend (direct): `http://localhost:5000` (only backend service)

#### 5. View logs
```bash
docker-compose logs -f
```

#### 6. Stop the application
```bash
docker-compose down
```

---

## API Documentation

### Endpoints

#### Health Check
```
GET /health
```
Returns the service status.

**Response:**
```json
{
  "status": "healthy",
  "service": "cooking-todo-app"
}
```

#### Generate Meal Plan
```
POST /api/generate-meal-plan
```
Generates a personalized meal plan based on user input.

**Request Body:**
```json
{
  "day_description": "Busy work day, need quick meals",
  "preferences": ["vegetarian", "gluten-free"],
  "budget": 30.00
}
```

**Response:**
```json
{
  "breakfast": {
    "meal": "Oatmeal with Berries",
    "time": "7:00 AM",
    "ingredients": ["oats", "berries", "milk", "honey"],
    "prep_time_minutes": 10
  },
  "lunch": {
    "meal": "Grilled Chicken Salad",
    "time": "12:30 PM",
    "ingredients": ["chicken breast", "mixed greens", "tomato", "cucumber"],
    "prep_time_minutes": 15
  },
  "dinner": {
    "meal": "Pasta with Marinara",
    "time": "6:30 PM",
    "ingredients": ["pasta", "tomato sauce", "garlic", "parmesan"],
    "prep_time_minutes": 25
  },
  "grocery_list": ["oats", "berries", "milk", "honey", ...],
  "estimated_cost": 28.50,
  "budget_feasible": true,
  "substitutions": [
    {
      "original": "chicken breast",
      "substitute": "tofu",
      "reason": "vegetarian alternative"
    }
  ],
  "notes": "All meals can be prepared at home for better cost efficiency"
}
```

#### Get Example Meal Plan
```
GET /api/meal-plan-example
```
Returns an example meal plan without calling the AI.

---

## Environment Variables

Create a `.env` file in the root directory:

```env
# Flask Configuration
FLASK_ENV=production                    # development or production
PORT=5000                              # Port to run on
SECRET_KEY=your-secret-key-here        # Change in production!

# Google Generative AI
GOOGLE_API_KEY=your-api-key-here       # Get from https://makersuite.google.com/app/apikey

# Database (optional)
DATABASE_URL=sqlite:///app.db

# CORS Configuration
CORS_ORIGINS=http://localhost:5000

# Logging
LOG_LEVEL=INFO
```

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f web
```

### Using Docker Directly

```bash
# Build image
docker build -t cooking-todo-app .

# Run container
docker run -d \
  --name cooking-todo \
  -p 5000:5000 \
  -e GOOGLE_API_KEY=your-api-key \
  -e SECRET_KEY=your-secret-key \
  cooking-todo-app
```

### Production Deployment

For production deployment:

1. **Use environment variables** instead of `.env` file
2. **Enable HTTPS** by configuring SSL certificates in Nginx
3. **Set `FLASK_ENV=production`**
4. **Update `SECRET_KEY`** to a strong random value
5. **Configure proper logging and monitoring**
6. **Use a production database** instead of SQLite

Example with SSL:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## Features in Detail

### Meal Planning Flow

1. **User Input**: User describes their day (busy, relaxed, etc.)
2. **Preferences**: Select dietary preferences (vegetarian, vegan, gluten-free, etc.)
3. **Budget**: Set daily budget for meals
4. **AI Generation**: Google Gemini AI generates personalized meal plan
5. **Results Display**:
   - Individual meal cards with ingredients and prep times
   - Consolidated grocery list
   - Budget analysis and feasibility check
   - Alternative ingredient suggestions
   - Additional notes

### Frontend Features

- ✅ Real-time form validation
- ✅ Loading spinner during processing
- ✅ Error handling and user feedback
- ✅ Interactive grocery list (click to mark done)
- ✅ Print functionality
- ✅ Download meal plan as JSON
- ✅ Responsive mobile design
- ✅ Accessibility features

### Backend Features

- ✅ Flask REST API
- ✅ CORS support
- ✅ Error handling
- ✅ Health check endpoint
- ✅ Fallback meal plans when AI is unavailable
- ✅ Configuration management
- ✅ Environment-based settings

---

## Troubleshooting

### Issue: API Key not working
- Verify your Google API key is valid
- Check if Generative AI API is enabled in Google Cloud Console
- Ensure `.env` file is properly formatted

### Issue: Docker container won't start
```bash
# Check logs
docker-compose logs

# Rebuild without cache
docker-compose build --no-cache
```

### Issue: CORS errors
- Verify `CORS_ORIGINS` environment variable includes your domain
- Check that API requests have correct headers

### Issue: Port already in use
```bash
# Change port in docker-compose.yml
ports:
  - "8000:5000"  # Map to different port
```

---

## Development Guide

### Adding New Features

1. **Backend**: Add new endpoints to `backend/app.py`
2. **Meal Planner**: Extend logic in `backend/meal_planner.py`
3. **Frontend**: Update HTML in `frontend/index.html` and logic in `frontend/script.js`
4. **Styles**: Add CSS to `frontend/styles.css`

### Running Tests (Future Enhancement)

```bash
cd backend
pytest tests/
```

---

## Performance Optimization

- **Nginx Caching**: Static assets cached for 1 hour
- **Gzip Compression**: Enabled for text-based responses
- **Image Optimization**: Use optimized Docker base image (Python 3.11-slim)
- **Database**: SQLite by default, upgrade to PostgreSQL for production

---

## Security Considerations

- 🔒 **HTTPS**: Recommended for production
- 🔑 **API Keys**: Never commit `.env` to version control
- 🛡️ **Headers**: Security headers configured in Nginx
- ✅ **Input Validation**: All inputs validated on backend
- 🔐 **CORS**: Restricted to specified origins

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## License

MIT License - feel free to use this project for personal or commercial use.

---

## Support

For issues, questions, or suggestions:
1. Check the Troubleshooting section
2. Review API documentation
3. Check Docker logs for errors

---

## Future Enhancements

- [ ] User authentication and profiles
- [ ] Save favorite meal plans
- [ ] Recipe integration with detailed instructions
- [ ] Nutrition tracking
- [ ] Shopping list sync with mobile app
- [ ] Multi-language support
- [ ] Advanced dietary restrictions
- [ ] Integration with grocery delivery services

---

## Acknowledgments

- Built for the H2C PromptWars Hackathon
- Powered by Google Generative AI (Gemini)
- Frontend inspiration from modern design practices

---

**Last Updated**: June 6, 2026

🚀 Happy cooking!
