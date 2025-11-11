import streamlit as st
import pandas as pd
# --- NEW: Import our shared database and calculator ---
from database import INGREDIENT_DB, calculate_recipe_cost

# --- 3. THE STREAMLIT WEB INTERFACE ---
st.set_page_config(layout="wide")
st.title("🍳 Food Cost Calculator")

# Initialize session_state
if 'current_recipe' not in st.session_state:
    st.session_state.current_recipe = []
if 'saved_recipes' not in st.session_state:
    st.session_state.saved_recipes = {} # We'll use a dictionary
if 'results' not in st.session_state:
    st.session_state.results = None

# --- We create two main columns ---
col1, col2 = st.columns([1, 1]) # 50/50 split

# --- COLUMN 1: INPUTS ---
with col1:
    st.header("1. Build Your Recipe")
    
    recipe_name = st.text_input("Recipe Name", "New Recipe (e.g., Burger)")
    
    with st.container(border=True):
        col1a, col1b, col1c = st.columns([3, 1, 1])
        with col1a:
            # Dropdown now reads from our imported INGREDIENT_DB
            ingredient_name = st.selectbox("Select Ingredient", options=INGREDIENT_DB.keys(), label_visibility="collapsed")
        with col1b:
            quantity = st.number_input("Quantity", min_value=0.0, step=0.1, format="%.2f", label_visibility="collapsed")
        with col1c:
            all_units = ['g', 'kg', 'tsp', 'tbsp', 'cup', 'ml', 'l', 'each']
            unit = st.selectbox("Unit", options=all_units, label_visibility="collapsed")
        
        if st.button("Add Ingredient", use_container_width=True):
            if quantity > 0:
                st.session_state.current_recipe.append(
                    {'name': ingredient_name, 'qty': quantity, 'unit': unit}
                )

    st.subheader("Current Recipe Items")
    with st.container(height=200, border=True):
        if not st.session_state.current_recipe:
            st.info("Your recipe is empty.")
        else:
            for i, item in enumerate(st.session_state.current_recipe):
                st.write(f"  - **{item['qty']} {item['unit']}** of **{item['name']}**")
    
    st.header("2. Set Price & Calculate")
    with st.container(border=True):
        input_col1, input_col2 = st.columns(2)
        with input_col1:
            servings = st.number_input("Servings this recipe makes?", min_value=1, value=1)
        with input_col2:
            target_food_cost = st.number_input("Target Food Cost %", min_value=1, max_value=100, value=30, step=1)
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("Calculate Cost", use_container_width=True, type="primary"):
                if st.session_state.current_recipe:
                    # We now use the imported calculate_recipe_cost function
                    st.session_state.results = calculate_recipe_cost(
                        st.session_state.current_recipe, servings, target_food_cost
                    )
                else:
                    st.error("Cannot calculate an empty recipe.")
        
        with btn_col2:
            if st.button("Clear Recipe", use_container_width=True):
                st.session_state.current_recipe = []
                st.session_state.results = None
                st.rerun()

# --- COLUMN 2: RESULTS (THE DASHBOARD) ---
with col2:
    st.header("3. Results Dashboard")
    
    if st.session_state.results:
        results = st.session_state.results
        
        st.subheader("Price Summary")
        with st.container(border=True):
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            metric_col1.metric("Total Cost", f"₱{results['total_cost']:.2f}")
            metric_col2.metric("Cost Per Serving", f"₱{results['cost_per_serving']:.2f}")
            metric_col3.metric(
                f"Suggested Price (at {target_food_cost}%)", 
                f"₱{results['suggested_price']:.2f}"
            )
            
            if st.button("Save Recipe to Tracker", use_container_width=True, type="primary"):
                if recipe_name and recipe_name != "New Recipe (e.g., Burger)":
                    st.session_state.saved_recipes[recipe_name] = {
                        'items': st.session_state.current_recipe,
                        'servings': servings,
                        'target_percent': target_food_cost,
                        # We save the *inputs*, not the old results
                    }
                    st.success(f"'{recipe_name}' saved to Pricing Tracker!")
                else:
                    st.error("Please enter a valid Recipe Name before saving.")

        
        st.subheader("Top 10 Item Costs")
        with st.container(border=True):
            if results['chart_data']:
                df = pd.DataFrame(results['chart_data'])
                df_grouped = df.groupby('Ingredient')['Cost'].sum().reset_index()
                df_sorted = df_grouped.sort_values(by='Cost', ascending=False)
                st.bar_chart(df_sorted.head(10), x='Ingredient', y='Cost')
            else:
                st.info("No cost data to display.")

        st.subheader("Cost Breakdown")
        with st.container(height=300, border=True):
            for line in results['breakdown']:
                if "ERROR" in line:
                    st.error(line)
                else:
                    st.code(line)
    
    else:
        st.info("Your results will appear here after you click 'Calculate Cost'.")
