# 🍳 Cooking To-Do List Generator

A modern, AI-powered web application that helps users generate personalized cooking to-do lists and structured meal plans. Built with a Flask backend, a premium vanilla JavaScript frontend, and fully optimized for seamless deployment to **Vercel**.

## Features

- 🤖 **AI-Powered Meal Planning**: Uses Google Generative AI (Gemini 1.5 Flash) to generate personalized meal plans based on your day.
- 🥣 **Structured Meal Planning**: Generates breakfast, lunch, and dinner plans tailored to your busy schedule.
- 📋 **Smart Grocery List**: Generates an interactive grocery checklist containing specific quantities and prices in Rupees (₹).
- 💰 **Budget Analysis**: Checks and details if the overall estimated meal costs are within your specified daily budget.
- 🔄 **Substitutions**: Suggests healthy and easy substitutions for specific ingredients.
- 📱 **Premium Responsive UI**: Features a modern dark glassmorphic interface with floating gradient effects.
- ⚡ **Edge Optimized**: Runs as a lightweight serverless application on Vercel.

---

## Project Structure

```
Cooking-TODO/
├── api/
│   └── index.py            # Vercel serverless function entry point
├── backend/
│   ├── app.py              # Flask application logic
│   ├── config.py           # Configuration management
│   ├── meal_planner.py     # AI meal planning engine
│   └── requirements.txt    # Backend dependencies
├── frontend/
│   ├── index.html          # Web application structure
│   ├── styles.css          # Premium glassmorphic styling
│   └── script.js           # Client-side routing and DOM manipulation
├── vercel.json             # Vercel deployment routing configuration
├── requirements.txt        # Root-level serverless dependencies
├── .env.example            # Environment variables template
└── README.md               # Application documentation
```

---

## Local Development Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Installation & Execution

1. **Clone and navigate to the project directory**:
   ```bash
   cd path/to/Cooking-TODO
   ```

2. **Set up a Python virtual environment**:
   ```bash
   # Create environment
   python -m venv venv

   # Activate environment (Windows)
   venv\Scripts\activate

   # Activate environment (macOS/Linux)
   source venv/bin/activate
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the environment**:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Update `.env` with your Google Gemini API key:
     ```env
     GOOGLE_API_KEY=your-gemini-api-key-here
     ```

5. **Run the development server**:
   ```bash
   cd backend
   python app.py
   ```
   The application will start at `http://localhost:5000`.

---

## Deploying to Vercel

This application is configured for deployment to **Vercel** as a Python Serverless project.

### Deployment Steps

1. **Push the repository to GitHub**.
2. **Import the repository into Vercel**:
   - Go to your Vercel dashboard and click **Add New** > **Project**.
   - Import your repository.
3. **Configure Environment Variables**:
   In the project configuration settings on Vercel, add the following variables:
   - `GOOGLE_API_KEY`: Your Google Gemini API Key.
   - `SECRET_KEY`: A secure random string for Flask session signing.
4. **Deploy**:
   - Click **Deploy**. Vercel will automatically build the static assets from `frontend/` and route requests to the Flask serverless function inside `api/index.py`.

---

## License

This project is licensed under the MIT License - feel free to use it for personal or commercial projects.
