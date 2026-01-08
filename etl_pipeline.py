import pandas as pd
import mysql.connector
from mysql.connector import Error
import os

# --- Database Configuration ---
# Update 'password' with your MySQL password
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password', 
    'database': 'fleximart'
}

def clean_phone_number(phone):
    """Standardizes phone numbers to +91-XXXXXXXXXX format"""
    if pd.isna(phone):
        return None
    # Remove characters like ' ', '-', '+91'
    clean_p = str(phone).replace(' ', '').replace('-', '').replace('+91', '')
    
    # Check if we have 10 valid digits
    if clean_p.isdigit() and len(clean_p) == 10:
        return f"+91-{clean_p}"
    return clean_p # Return original if we can't fix it

def run_etl_process():
    print("--- Starting FlexiMart ETL Pipeline ---")
    
    # 1. Extraction
    try:
        print("Extracting CSV data...")
        # Reading raw files
        customers = pd.read_csv('../data/customers_raw.csv')
        products = pd.read_csv('../data/products_raw.csv')
        sales = pd.read_csv('../data/sales_raw.csv')
    except FileNotFoundError:
        print("Error: CSV files not found in data/ folder.")
        return

    # 2. Transformation
    print("Transforming and cleaning data...")
    
    # --- Customer Cleaning ---
    # Remove duplicates based on Email
    customers.drop_duplicates(subset=['email'], keep='first', inplace=True)
    # Fix Phone numbers
    customers['phone'] = customers['phone'].apply(clean_phone_number)
    # Fix Null Cities
    customers['city'] = customers['city'].fillna('Unknown')
    # Format Names
    customers['first_name'] = customers['first_name'].str.title()
    customers['last_name'] = customers['last_name'].str.title()

    # --- Product Cleaning ---
    # Standardize Category (electronics -> Electronics)
    products['category'] = products['category'].str.strip().str.capitalize()
    # Handle Null Prices (Fill with category average or 0)
    products['price'] = products['price'].fillna(0)
    products['stock_quantity'] = products['stock_quantity'].fillna(0)

    # --- Sales Cleaning ---
    # Fix Dates (Handle various formats)
    sales['order_date'] = pd.to_datetime(sales['order_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Drop rows with missing critical IDs
    sales.dropna(subset=['customer_id', 'product_id'], inplace=True)
    sales.drop_duplicates(inplace=True)

    # 3. Loading
    print("Loading data into MySQL...")
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            cursor = conn.cursor()
            
            # Setup Tables (Idempotent)
            cursor.execute("CREATE DATABASE IF NOT EXISTS fleximart")
            cursor.execute("USE fleximart")
            
            # Note: In a real run, table creation SQL usually goes here or is pre-run.
            # Inserting Customers
            for _, row in customers.iterrows():
                sql = """INSERT INTO customers (first_name, last_name, email, phone, city, registration_date)
                         VALUES (%s, %s, %s, %s, %s, %s)
                         ON DUPLICATE KEY UPDATE city=VALUES(city)"""
                val = (row['first_name'], row['last_name'], row['email'], row['phone'], row['city'], row['registration_date'])
                cursor.execute(sql, val)

            # Inserting Products
            for _, row in products.iterrows():
                sql = """INSERT INTO products (product_name, category, price, stock_quantity)
                         VALUES (%s, %s, %s, %s)
                         ON DUPLICATE KEY UPDATE price=VALUES(price)"""
                val = (row['product_name'], row['category'], row['price'], row['stock_quantity'])
                cursor.execute(sql, val)
            
            conn.commit()
            print("Data loaded successfully.")
            
            # Generate Report
            with open('data_quality_report.txt', 'w') as f:
                f.write(f"ETL Report\n==========\n")
                f.write(f"Customers Processed: {len(customers)}\n")
                f.write(f"Products Processed: {len(products)}\n")
                f.write(f"Sales Processed: {len(sales)}\n")
                f.write("Status: Success")
            
            cursor.close()
            conn.close()
            
    except Error as e:
        print(f"Database Error: {e}")

if __name__ == "__main__":
    run_etl_process()