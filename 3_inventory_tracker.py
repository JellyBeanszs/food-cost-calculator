import streamlit as st
import pandas as pd
# Import the database from the parent folder
from database import INGREDIENT_DB

st.set_page_config(layout="wide")
st.title("📦 Smart Ingredient Inventory")

# --- Process the Database ---
# We will build a list of data to show in a table
inventory_data = []
total_inventory_value = 0
stock_status_counts = {"In Stock": 0, "Low Stock": 0, "Out of Stock": 0}

# Loop through every ingredient in our main database
for name, data in INGREDIENT_DB.items():
    current_stock = data.get('current_stock_g', 0)
    min_stock = data.get('min_stock_g', 0)
    cost_per_unit = data.get('cost_per_base_unit', 0)
    base_unit = data.get('base_unit', 'g')
    
    # Calculate Stock Status
    if current_stock <= 0:
        status = "🔴 Out of Stock"
        stock_status_counts["Out of Stock"] += 1
    elif current_stock <= min_stock:
        status = "🟠 Low Stock"
        stock_status_counts["Low Stock"] += 1
    else:
        status = "🟢 In Stock"
        stock_status_counts["In Stock"] += 1
        
    # Calculate Inventory Value (Stock * Cost)
    inventory_value = current_stock * cost_per_unit
    total_inventory_value += inventory_value
    
    # Add to our list
    inventory_data.append({
        "Ingredient": name,
        "Stock Status": status,
        "Current Stock": f"{current_stock} {base_unit}",
        "Min Stock": f"{min_stock} {base_unit}",
        "Inventory Value (₱)": inventory_value,
        "Unit Cost (₱)": f"{cost_per_unit} / {base_unit}",
        "SKU": data.get('sku', '-'),
        "Supplier": data.get('supplier', '-')
    })

# --- Display the Dashboard ---

# 1. Top Metrics (like in your picture)
st.header("Inventory Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Inventory Value", f"₱{total_inventory_value:,.2f}")
col2.metric("In Stock", stock_status_counts["In Stock"])
col3.metric("Low Stock", stock_status_counts["Low Stock"])
col4.metric("Out of Stock", stock_status_counts["Out of Stock"])

# 2. The Main Inventory Table
st.header("Inventory Details")
df = pd.DataFrame(inventory_data)
st.dataframe(
    df,
    use_container_width=True,
    column_config={
        "Inventory Value (₱)": st.column_config.NumberColumn(format="₱%.2f")
    },
    hide_index=True
)

st.info("To update stock levels or prices, please edit the `database.py` file.")
