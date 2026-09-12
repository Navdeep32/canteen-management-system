"""
Database Schema Checker
This script shows you the actual column names in your database
"""

import mysql.connector
from mysql.connector import Error
import pandas as pd

def check_schema():
    """Check and display database schema"""
    
    print("=" * 70)
    print("🔍 Database Schema Inspector")
    print("=" * 70)
    
    try:
        # Get credentials from user input (like test_connection.py does)
        print("Enter your MySQL credentials:")
        host = input("Host (default: localhost): ").strip() or "localhost"
        user = input("Username (default: root): ").strip() or "root"
        password = input("Password: ").strip()
        database = input("Database (default: canteen): ").strip() or "canteen"
        
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # Connect to database
        # connection = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     password="pswd",
        #     database="canteen"
        # )
        
        if connection.is_connected():
            print("\n✅ Connected to database: canteen")
            
            cursor = connection.cursor()
            
            # Check SALES table
            print("\n" + "=" * 70)
            print("📊 SALES TABLE STRUCTURE")
            print("=" * 70)
            
            cursor.execute("DESCRIBE sales")
            sales_columns = cursor.fetchall()
            
            print("\nColumns in SALES table:")
            for col in sales_columns:
                print(f"   • {col[0]:<20} | Type: {col[1]:<15}")
            
            # Show sample data
            cursor.execute("SELECT * FROM sales LIMIT 3")
            sales_sample = cursor.fetchall()
            
            print("\n📋 Sample SALES data (first 3 rows):")
            column_names = [desc[0] for desc in cursor.description]
            
            df_sales = pd.DataFrame(sales_sample, columns=column_names)
            print(df_sales.to_string())
            
            # Check INVENTORY table
            print("\n" + "=" * 70)
            print("📦 INVENTORY TABLE STRUCTURE")
            print("=" * 70)
            
            cursor.execute("DESCRIBE inventory")
            inventory_columns = cursor.fetchall()
            
            print("\nColumns in INVENTORY table:")
            for col in inventory_columns:
                print(f"   • {col[0]:<20} | Type: {col[1]:<15}")
            
            # Show sample data
            cursor.execute("SELECT * FROM inventory LIMIT 3")
            inventory_sample = cursor.fetchall()
            
            print("\n📋 Sample INVENTORY data (first 3 rows):")
            column_names_inv = [desc[0] for desc in cursor.description]
            
            df_inventory = pd.DataFrame(inventory_sample, columns=column_names_inv)
            print(df_inventory.to_string())
            
            # Check USERS table
            print("\n" + "=" * 70)
            print("👥 USERS TABLE STRUCTURE")
            print("=" * 70)
            
            cursor.execute("DESCRIBE users")
            users_columns = cursor.fetchall()
            
            print("\nColumns in USERS table:")
            for col in users_columns:
                print(f"   • {col[0]:<20} | Type: {col[1]:<15}")
            
            cursor.execute("SELECT user_id, username, role FROM users")
            users_data = cursor.fetchall()
            
            print("\n📋 Users in database:")
            for user in users_data:
                print(f"   • ID: {user[0]}, Username: {user[1]}, Role: {user[2]}")
            
            cursor.close()
            connection.close()
            
            print("\n" + "=" * 70)
            print("✅ Schema check complete!")
            print("=" * 70)
            
            print("\n💡 Expected columns by the app:")
            print("\nSALES table should have:")
            print("   • date_of_sale")
            print("   • item_name")
            print("   • category")
            print("   • quantity_sold")
            print("   • unit_price")
            print("   • total_amount")
            print("   • payment_mode")
            print("   • customer_type")
            
            print("\nINVENTORY table should have:")
            print("   • date_of_entry")
            print("   • item_name")
            print("   • stock_in")
            print("   • stock_used")
            print("   • remaining_stock")
            print("   • unit_cost")
            print("   • supplier_name")
            
    except Error as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    check_schema()
    
    print("\n\n🔧 If your columns are different, I'll create a fix script for you.")
    print("👋 Press Enter to exit...")
    input()