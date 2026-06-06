import os
import json
import re
from datetime import datetime

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class MealPlanner:
    """AI-powered meal planning service"""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if self.api_key and genai:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    def generate_meal_plan(self, day_description, preferences=None, budget=None):
        """
        Generate a meal plan based on user's day and preferences
        
        Args:
            day_description: Description of the user's day (e.g., "Busy work day, need quick meals")
            preferences: List of dietary preferences/restrictions
            budget: Budget for meals in rupees
        
        Returns:
            Dictionary with meals, grocery list, substitutions, and budget analysis
        """
        
        prompt = self._build_prompt(day_description, preferences, budget)
        
        try:
            if self.model:
                response = self.model.generate_content(prompt)
                result = self._parse_response(response.text)
            else:
                result = self._generate_fallback_plan(day_description, preferences, budget)
            
            return result
        except Exception as e:
            print(f"Error generating meal plan: {e}")
            return self._generate_fallback_plan(day_description, preferences, budget)
    
    def _build_prompt(self, day_description, preferences, budget):
        """Build the AI prompt for meal planning"""
        prompt = f"""Based on the following user profile, generate a personalized meal plan for today:

User's Day: {day_description}
Dietary Preferences: {', '.join(preferences) if preferences else 'No specific preferences'}
Budget: ₹{budget if budget else 'No specific budget'} for the day

Please provide a response in the following JSON format:
{{
    "breakfast": {{
        "meal": "meal name",
        "time": "estimated time",
        "ingredients": ["ingredient1", "ingredient2"],
        "prep_time_minutes": 15
    }},
    "lunch": {{
        "meal": "meal name",
        "time": "estimated time",
        "ingredients": ["ingredient1", "ingredient2"],
        "prep_time_minutes": 20
    }},
    "dinner": {{
        "meal": "meal name",
        "time": "estimated time",
        "ingredients": ["ingredient1", "ingredient2"],
        "prep_time_minutes": 30
    }},
    "grocery_list": ["item1", "item2"],
    "estimated_cost": 500.00,
    "substitutions": [
        {{"original": "item", "substitute": "alternative", "reason": "explanation"}}
    ],
    "budget_feasible": true,
    "notes": "any additional notes"
}}

Provide ONLY the JSON response, no additional text."""
        return prompt
    
    def _parse_response(self, response_text):
        """Parse JSON response from AI model"""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
        
        return self._generate_fallback_plan("", [], None)
    
    def _generate_fallback_plan(self, day_description, preferences, budget):
        """Generate a fallback meal plan when AI is unavailable"""
        return {
            "breakfast": {
                "meal": "Oatmeal with Berries",
                "time": "7:00 AM",
                "ingredients": ["oats", "berries", "milk", "honey"],
                "prep_time_minutes": 10
            },
            "lunch": {
                "meal": "Grilled Chicken Salad",
                "time": "12:30 PM",
                "ingredients": ["chicken breast", "mixed greens", "tomato", "cucumber", "olive oil"],
                "prep_time_minutes": 15
            },
            "dinner": {
                "meal": "Pasta with Marinara",
                "time": "6:30 PM",
                "ingredients": ["pasta", "tomato sauce", "garlic", "parmesan cheese", "basil"],
                "prep_time_minutes": 25
            },
            "grocery_list": [
                "oats", "berries", "milk", "honey",
                "chicken breast", "mixed greens", "tomato", "cucumber", "olive oil",
                "pasta", "tomato sauce", "garlic", "parmesan cheese", "basil"
            ],
            "estimated_cost": 500.00,
            "substitutions": [
                {
                    "original": "chicken breast",
                    "substitute": "tofu or beans",
                    "reason": "vegetarian alternative"
                },
                {
                    "original": "pasta",
                    "substitute": "rice or quinoa",
                    "reason": "gluten-free option"
                }
            ],
            "budget_feasible": True,
            "notes": "All meals can be prepared at home for better cost efficiency"
        }
