// Configuration
const API_BASE_URL = '';

// DOM Elements
const mealPlanForm = document.getElementById('mealPlanForm');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const formSection = document.querySelector('.form-section');

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    mealPlanForm.addEventListener('submit', handleFormSubmit);
});

/**
 * Handle form submission
 */
async function handleFormSubmit(e) {
    e.preventDefault();

    // Get form data
    const dayDescription = document.getElementById('dayDescription').value.trim();
    const preferences = Array.from(document.querySelectorAll('input[name="preferences"]:checked'))
        .map(checkbox => checkbox.value);
    const budget = document.getElementById('budget').value ? parseFloat(document.getElementById('budget').value) : null;

    // Validate
    if (!dayDescription) {
        showError('Please describe your day');
        return;
    }

    // Show loading, hide others
    showLoading();

    try {
        // Call API
        const response = await fetch(`${API_BASE_URL}/api/generate-meal-plan`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                day_description: dayDescription,
                preferences: preferences,
                budget: budget
            })
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const mealPlan = await response.json();

        // Display results
        displayMealPlan(mealPlan);
        showResults();
    } catch (error) {
        console.error('Error:', error);
        showError('Failed to generate meal plan. Please try again.');
    }
}

/**
 * Display meal plan data
 */
function displayMealPlan(mealPlan) {
    // Breakfast
    displayMeal('breakfastContent', mealPlan.breakfast);

    // Lunch
    displayMeal('lunchContent', mealPlan.lunch);

    // Dinner
    displayMeal('dinnerContent', mealPlan.dinner);

    // Grocery List
    displayGroceryList(mealPlan.grocery_list);

    // Budget Info
    displayBudgetInfo(mealPlan);

    // Substitutions
    displaySubstitutions(mealPlan.substitutions);

    // Notes
    if (mealPlan.notes) {
        displayNotes(mealPlan.notes);
    }

    // Store current plan for export
    window.currentMealPlan = mealPlan;
}

/**
 * Display a single meal
 */
function displayMeal(elementId, meal) {
    const content = document.getElementById(elementId);
    
    let html = `
        <div class="meal-details">
            <p><strong>Meal:</strong> ${meal.meal}</p>
            <p><strong>Time:</strong> ${meal.time}</p>
            <p><strong>Prep Time:</strong> ${meal.prep_time_minutes} minutes</p>
            <p><strong>Ingredients:</strong></p>
            <div class="ingredients-list">
    `;

    meal.ingredients.forEach(ingredient => {
        html += `<span class="ingredient-tag">${ingredient}</span>`;
    });

    html += `</div></div>`;
    content.innerHTML = html;
}

/**
 * Display grocery list
 */
function displayGroceryList(groceryList) {
    const groceryListElement = document.getElementById('groceryList');
    groceryListElement.innerHTML = '';

    groceryList.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'grocery-item';
        
        let displayStr = '';
        if (item && typeof item === 'object') {
            const name = item.item || '';
            const qty = item.quantity ? ` (${item.quantity})` : '';
            const cost = item.estimated_cost ? ` - ₹${item.estimated_cost}` : '';
            displayStr = `${name}${qty}${cost}`;
        } else {
            displayStr = item;
        }
        
        itemDiv.textContent = displayStr;
        itemDiv.style.cursor = 'pointer';
        
        // Toggle checked state on click
        itemDiv.addEventListener('click', () => {
            itemDiv.style.opacity = itemDiv.style.opacity === '0.5' ? '1' : '0.5';
            itemDiv.style.textDecoration = itemDiv.style.textDecoration === 'line-through' ? 'none' : 'line-through';
        });

        groceryListElement.appendChild(itemDiv);
    });
}

/**
 * Display budget information
 */
function displayBudgetInfo(mealPlan) {
    const budgetInfo = document.getElementById('budgetInfo');
    
    const estimatedCost = mealPlan.estimated_cost || 'Not available';
    const isFeasible = mealPlan.budget_feasible;
    const feasibilityText = isFeasible ? 
        '<span style="color: var(--success-color);">✓ Within Budget</span>' : 
        '<span style="color: var(--warning-color);">⚠ May Exceed Budget</span>';

    budgetInfo.innerHTML = `
        <p><strong>Estimated Cost:</strong> ₹${estimatedCost}</p>
        <p><strong>Budget Feasible:</strong> ${feasibilityText}</p>
    `;
}

/**
 * Display substitutions
 */
function displaySubstitutions(substitutions) {
    const substitutionsDiv = document.getElementById('substitutions');
    substitutionsDiv.innerHTML = '';

    if (!substitutions || substitutions.length === 0) {
        substitutionsDiv.innerHTML = '<p>No substitutions suggested</p>';
        return;
    }

    substitutions.forEach(sub => {
        const subDiv = document.createElement('div');
        subDiv.className = 'substitution-item';
        subDiv.innerHTML = `
            <p><strong>Original:</strong> <span class="original">${sub.original}</span></p>
            <p><strong>Substitute:</strong> <span class="substitute">${sub.substitute}</span></p>
            <p><strong>Reason:</strong> ${sub.reason}</p>
        `;
        substitutionsDiv.appendChild(subDiv);
    });
}

/**
 * Display notes
 */
function displayNotes(notes) {
    const notesSection = document.getElementById('notesSection');
    notesSection.innerHTML = `
        <h4>💡 Notes</h4>
        <p>${notes}</p>
    `;
    notesSection.classList.remove('hidden');
}

/**
 * Show loading state
 */
function showLoading() {
    formSection.style.display = 'none';
    loadingSpinner.classList.remove('hidden');
    resultsSection.classList.add('hidden');
    errorSection.classList.add('hidden');
}

/**
 * Show results
 */
function showResults() {
    loadingSpinner.classList.add('hidden');
    resultsSection.classList.remove('hidden');
    errorSection.classList.add('hidden');
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Show error
 */
function showError(message) {
    loadingSpinner.classList.add('hidden');
    resultsSection.classList.add('hidden');
    errorSection.classList.remove('hidden');
    document.getElementById('errorMessage').textContent = message;
    formSection.style.display = 'block';
}

/**
 * Reset form and go back to input
 */
function resetForm() {
    mealPlanForm.reset();
    formSection.style.display = 'block';
    loadingSpinner.classList.add('hidden');
    resultsSection.classList.add('hidden');
    errorSection.classList.add('hidden');
    window.currentMealPlan = null;
    formSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Print meal plan
 */
function printMealPlan() {
    window.print();
}

/**
 * Download meal plan as JSON
 */
function downloadMealPlan() {
    if (!window.currentMealPlan) {
        alert('No meal plan to download');
        return;
    }

    const dataStr = JSON.stringify(window.currentMealPlan, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `meal-plan-${new Date().toISOString().split('T')[0]}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
}
