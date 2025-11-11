import streamlit as st
import pandas as pd
# --- NEW: Import our shared database and calculator ---
from database import calculate_recipe_cost

st.set_page_config(layout="wide")
st.title("📊 Pricing Tracker")

# Check if we have any saved recipes
if 'saved_recipes' not in st.session_state or not st.session_state.saved_recipes:
    st.info("You haven't saved any recipes yet. Please go to the 'Food Cost Calculator' page to save a recipe.")
else:
    st.info("This table recalculates all your recipes *live* using the current ingredient prices from your database.")

    # --- This is the core logic ---
    # We will build a list of data to show in a table
    tracker_data = []

    # Loop through every recipe you've saved
    for recipe_name, recipe_data in st.session_state.saved_recipes.items():
        
        # --- HERE IS THE MAGIC ---
        # Recalculate the cost using the *current* ingredient prices
        # from database.py.
        recalculated_results = calculate_recipe_cost(
            recipe_data['items'],
            recipe_data['servings'],
            recipe_data['target_percent']
        )
        
        # Add the data to our list
        tracker_data.append({
            "Product": recipe_name,
            "Cost Per Serving (₱)": recalculated_results['cost_per_serving'],
            "Suggested Price (₱)": recalculated_results['suggested_price'],
            "Target Food Cost %": f"{recipe_data['target_percent']}%",
            "Servings": recipe_data['servings']
        })

    # --- Display the data in a table ---
    if tracker_data:
        df = pd.DataFrame(tracker_data)
        st.dataframe(df, use_container_width=True)

        # --- Show Key Metrics ---
        st.header("Summary")
        avg_cost = df['Cost Per Serving (₱)'].mean()
        avg_price = df['Suggested Price (₱)'].mean()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Products", len(df))
        col2.metric("Average Cost", f"₱{avg_cost:.2f}")
        col3.metric("Average Price", f"₱{avg_price:.2f}")
