# --- 1. THE INGREDIENT DATABASE ---
# THIS IS YOUR "SINGLE SOURCE OF TRUTH"
# We've added SKU, Supplier, and Stock fields
INGREDIENT_DB = {
    "Flour (All-Purpose)": {
        "base_unit": "g",
        "cost_per_base_unit": 0.054,  # Cost per Gram
        "conversions": {
            "g": 1, "kg": 1000, "cup": 120, "tbsp": 7.5, "tsp": 2.5
        },
        # --- NEW INVENTORY FIELDS ---
        "sku": "FLOUR-01",
        "supplier": "ManilaBake Co.",
        "current_stock_g": 10000,  # 10,000 grams (10kg)
        "min_stock_g": 2000      # 2,000 grams (2kg)
    },
    "Sugar (White)": {
        "base_unit": "g",
        "cost_per_base_unit": 0.07,   # Cost per Gram
        "conversions": {
            "g": 1, "kg": 1000, "cup": 200, "tbsp": 12.5, "tsp": 4
        },
        # --- NEW INVENTORY FIELDS ---
        "sku": "SUG-01",
        "supplier": "Sweet Supply",
        "current_stock_g": 8000,
        "min_stock_g": 2000
    },
    "Buns": {
        "base_unit": "each",
        "cost_per_base_unit": 22.0,  # Cost per Bun
        "conversions": { "each": 1 },
        # --- NEW INVENTORY FIELDS ---
        "sku": "BUN-01",
        "supplier": "Corner Bakery",
        "current_stock_g": 50,    # 50 "each"
        "min_stock_g": 12     # 12 "each"
    },
    "Cheese Slice": {
        "base_unit": "each",
        "cost_per_base_unit": 14.0,  # Cost per Slice
        "conversions": { "each": 1 },
        # --- NEW INVENTORY FIELDS ---
        "sku": "CHE-01",
        "supplier": "ManilaBake Co.",
        "current_stock_g": 0,     # 0 "each"
        "min_stock_g": 20
    },
    "Salt (Fine)": {
        "base_unit": "g",
        "cost_per_base_unit": 0.02, # Cost per Gram
        "conversions": {
            "g": 1, "kg": 1000, "tbsp": 18, "tsp": 6
        },
        # --- NEW INVENTORY FIELDS ---
        "sku": "SAL-01",
        "supplier": "Sweet Supply",
        "current_stock_g": 500,
        "min_stock_g": 500
    }
}

# --- 2. THE CALCULATION FUNCTION ---
# This function does NOT change. It's still perfect.
def calculate_recipe_cost(recipe_items, servings, target_cost_percent):
    total_recipe_cost = 0.0
    breakdown = [] 
    cost_data_for_chart = [] 

    for item in recipe_items:
        name = item['name']
        qty = item['qty']
        unit = item['unit']
        
        if name in INGREDIENT_DB:
            data = INGREDIENT_DB[name]
            base_cost = data['cost_per_base_unit'] 
            
            if unit in data['conversions']:
                conversion_factor = data['conversions'][unit]
                total_base_units = qty * conversion_factor
                line_cost = total_base_units * base_cost
                
                line_text = f"  > {name}: {qty} {unit} @ ₱{line_cost:.2f}"
                breakdown.append(line_text)
                cost_data_for_chart.append({'Ingredient': name, 'Cost': line_cost})
                
                total_recipe_cost += line_cost
            else:
                line_text = f"  > ERROR: Unit '{unit}' is not valid for '{name}'."
                breakdown.append(line_text)
        else:
            line_text = f"  > ERROR: '{name}' not found in DB."
            breakdown.append(line_text)

    cost_per_serving = total_recipe_cost / servings if servings > 0 else 0
    target_decimal = target_cost_percent / 100
    suggested_price = cost_per_serving / target_decimal if target_decimal > 0 else 0

    return {
        'total_cost': total_recipe_cost,
        'cost_per_serving': cost_per_serving,
        'suggested_price': suggested_price,
        'breakdown': breakdown,
        'chart_data': cost_data_for_chart,
        'target_percent': target_cost_percent
    }