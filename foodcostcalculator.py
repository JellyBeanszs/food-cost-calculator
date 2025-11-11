# --- 1. THE INGREDIENT DATABASE ---
# We store our ingredients and their cost per unit (g or each).
# This is our Python version of the "Ingredients" sheet.
INGREDIENT_DB = {
    # 'Ingredient Name': cost_per_unit
    "Flour": 0.00097,       # Cost per gram
    "Ground Beef": 0.011,   # Cost per gram (updated from 0.0011)
    "Buns": 0.40,           # Cost per each
    "Ketchup": 0.001,       # Cost per gram
    "Cheese Slice": 0.25    # Cost per each
}

# --- 2. THE CALCULATION FUNCTION ---
# This function does all the work. It takes a recipe and servings
# and returns the calculated costs.
def calculate_recipe_cost(recipe_items, servings):
    """
    Calculates the total cost and per-serving cost of a recipe.
    """
    total_recipe_cost = 0.0
    print("--- Recipe Cost Breakdown ---")

    for item in recipe_items:
        name = item['name']
        qty = item['qty']
        
        # Look up the ingredient's cost in our database
        if name in INGREDIENT_DB:
            cost_per_unit = INGREDIENT_DB[name]
            # Calculate the cost for this specific ingredient
            line_cost = cost_per_unit * qty
            
            print(f"  > {name}: {qty} units @ ${cost_per_unit:.4f}/unit = ${line_cost:.2f}")
            
            # Add this ingredient's cost to the total
            total_recipe_cost += line_cost
        else:
            print(f"  > WARNING: '{name}' not found in Ingredient DB. Skipping.")

    # Calculate the final cost per serving
    cost_per_serving = total_recipe_cost / servings

    # Return the results as a dictionary for easy use
    return {
        'total_cost': total_recipe_cost,
        'cost_per_serving': cost_per_serving,
        'servings': servings
    }

# --- 3. CREATE A RECIPE AND RUN THE CALCULATION ---

# This is our Python version of the "Recipes" sheet.
# It's a list, where each item is a dictionary.
burger_recipe = [
    {'name': 'Ground Beef', 'qty': 150},  # 150g
    {'name': 'Buns', 'qty': 1},           # 1 each
    {'name': 'Ketchup', 'qty': 10},         # 10g
    {'name': 'Cheese Slice', 'qty': 1}     # 1 each
]

# --- RUN IT! ---
print("Calculating cost for: Burger (1 Serving)\n")
recipe_results = calculate_recipe_cost(recipe_items=burger_recipe, servings=1)

# Print the final summary
print("\n--- Final Summary ---")
print(f"Total Recipe Cost: ${recipe_results['total_cost']:.2f}")
print(f"Cost per Serving:  ${recipe_results['cost_per_serving']:.2f}")