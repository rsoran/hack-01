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
            self.model = genai.GenerativeModel('gemini-1.5-flash')
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
    "grocery_list": [
        {{"item": "onion", "quantity": "100g", "estimated_cost": 10.00}},
        {{"item": "milk", "quantity": "1 packet", "estimated_cost": 30.00}}
    ],
    "estimated_cost": 40.00,
    "substitutions": [
        {{"original": "item", "substitute": "alternative", "reason": "explanation"}}
    ],
    "budget_feasible": true,
    "notes": "any additional notes"
}}

Important: All estimated costs must be in Rupees (₹). Ensure that every item in the grocery list is an object containing 'item', 'quantity', and 'estimated_cost' in Rupees, and that the sum of these estimated costs matches the overall 'estimated_cost'. If the budget is specified, do your best to design a meal plan where the overall estimated_cost is within the budget.

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
        # Default base cost
        estimated_cost = 400.00
        
        # Scale estimated cost dynamically if a budget is provided
        if budget is not None:
            try:
                target_budget = float(budget)
                if target_budget > 0:
                    # Set estimated cost to be 90% of budget, capped at 400
                    estimated_cost = min(target_budget * 0.9, 400.00)
                    if estimated_cost < 20.00:
                        estimated_cost = target_budget
            except ValueError:
                pass

        # Base grocery list items with relative weight factors for scaling
        base_items = [
            {"item": "Oats", "quantity": "100g", "weight": 20},
            {"item": "Berries", "quantity": "50g", "weight": 50},
            {"item": "Milk", "quantity": "500ml", "weight": 30},
            {"item": "Honey", "quantity": "2 tbsp", "weight": 15},
            {"item": "Chicken breast", "quantity": "250g", "weight": 100},
            {"item": "Mixed greens", "quantity": "100g", "weight": 30},
            {"item": "Tomato", "quantity": "2 units", "weight": 10},
            {"item": "Cucumber", "quantity": "1 unit", "weight": 10},
            {"item": "Olive oil", "quantity": "3 tbsp", "weight": 15},
            {"item": "Pasta", "quantity": "200g", "weight": 40},
            {"item": "Tomato sauce", "quantity": "1 cup", "weight": 30},
            {"item": "Garlic", "quantity": "3 cloves", "weight": 5},
            {"item": "Parmesan cheese", "quantity": "50g", "weight": 40},
            {"item": "Basil", "quantity": "a few leaves", "weight": 5}
        ]
        
        total_weight = sum(item["weight"] for item in base_items)
        
        # Scale each item's cost proportionally to match estimated_cost
        grocery_list = []
        for item in base_items:
            item_cost = round((item["weight"] / total_weight) * estimated_cost, 2)
            grocery_list.append({
                "item": item["item"],
                "quantity": item["quantity"],
                "estimated_cost": item_cost
            })
            
        # Adjust potential rounding difference on the last item to make sum exactly match estimated_cost
        calculated_sum = sum(item["estimated_cost"] for item in grocery_list)
        diff = round(estimated_cost - calculated_sum, 2)
        if diff != 0 and grocery_list:
            grocery_list[-1]["estimated_cost"] = round(grocery_list[-1]["estimated_cost"] + diff, 2)

        is_feasible = True
        if budget is not None:
            try:
                is_feasible = float(budget) >= estimated_cost
            except ValueError:
                pass

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
            "grocery_list": grocery_list,
            "estimated_cost": round(estimated_cost, 2),
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
            "budget_feasible": is_feasible,
            "notes": "All meals can be prepared at home for better cost efficiency"
        }
