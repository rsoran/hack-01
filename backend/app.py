import os
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from config import config
from meal_planner import MealPlanner

# Initialize Flask app with static and template folders
static_folder = os.path.join(os.path.dirname(__file__), 'static')
if not os.path.exists(os.path.join(static_folder, 'index.html')):
    static_folder = os.path.join(os.path.dirname(__file__), '..', 'frontend')
app = Flask(__name__, static_folder=static_folder, static_url_path='')

# Load configuration
config_name = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Enable CORS
CORS(app)

# Initialize meal planner
meal_planner = MealPlanner()


@app.route('/', methods=['GET'])
def index():
    """Serve index.html"""
    try:
        return send_from_directory(static_folder, 'index.html')
    except:
        return jsonify({'error': 'Frontend not found'}), 404


@app.route('/<path:path>', methods=['GET'])
def serve_static(path):
    """Serve static files"""
    try:
        return send_from_directory(static_folder, path)
    except:
        # Return index.html for unmatched routes (for SPA routing)
        try:
            return send_from_directory(static_folder, 'index.html')
        except:
            return jsonify({'error': 'Endpoint not found'}), 404


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'cooking-todo-app'}), 200


@app.route('/api/generate-meal-plan', methods=['POST'])
def generate_meal_plan():
    """
    Generate a meal plan based on user input
    
    Expected JSON body:
    {
        "day_description": "string",
        "preferences": ["string"],
        "budget": number
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'day_description' not in data:
            return jsonify({'error': 'Missing required field: day_description'}), 400
        
        day_description = data.get('day_description')
        preferences = data.get('preferences', [])
        budget = data.get('budget', None)
        
        # Generate meal plan
        meal_plan = meal_planner.generate_meal_plan(day_description, preferences, budget)
        
        return jsonify(meal_plan), 200
    
    except Exception as e:
        print(f"Error in generate_meal_plan: {e}")
        return jsonify({'error': 'Failed to generate meal plan'}), 500


@app.route('/api/meal-plan-example', methods=['GET'])
def get_example_meal_plan():
    """Get an example meal plan"""
    example = {
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
        "grocery_list": ["oats", "berries", "milk", "honey", "chicken breast", "mixed greens", "tomato", "cucumber", "pasta", "tomato sauce", "garlic", "parmesan"],
        "estimated_cost": 500.00,
        "budget_feasible": True
    }
    return jsonify(example), 200


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
