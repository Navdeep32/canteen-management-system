"""
Database Schema Checker

Displays the structure and sample data of the main tables
in the Canteen Management System database.
"""

import mysql.connector
from mysql.connector import Error
import pandas as pd


def check_schema():
    """Check and display database schema."""

    print("=" * 70)
    print("Database Schema Inspector")
    print("=" * 70)

    try:
        print("\nEnter your MySQL credentials:")
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

        if connection.is_connected():
            print(f"\nConnected to database: {database}")

            cursor = connection.cursor()

            # Check SALES table
            print("\n" + "=" * 70)
            print("SALES TABLE STRUCTURE")
            print("=" * 70)

            cursor.execute("DESCRIBE sales")
            sales_columns = cursor.fetchall()

            print("\nColumns in SALES table:")
            for column in sales_columns:
                print(f"   • {column[0]:<20} | Type: {column[1]:<15}")

            cursor.execute("SELECT * FROM sales LIMIT 3")
            sales_sample = cursor.fetchall()

            print("\nSample SALES data (first 3 rows):")
            column_names = [description[0] for description in cursor.description]
            df_sales = pd.DataFrame(sales_sample, columns=column_names)
            print(df_sales.to_string())

            # Check INVENTORY table
            print("\n" + "=" * 70)
            print("INVENTORY TABLE STRUCTURE")
            print("=" * 70)

            cursor.execute("DESCRIBE inventory")
            inventory_columns = cursor.fetchall()

            print("\nColumns in INVENTORY table:")
            for column in inventory_columns:
                print(f"   • {column[0]:<20} | Type: {column[1]:<15}")

            cursor.execute("SELECT * FROM inventory LIMIT 3")
            inventory_sample = cursor.fetchall()

            print("\nSample INVENTORY data (first 3 rows):")
            column_names = [description[0] for description in cursor.description]
            df_inventory = pd.DataFrame(
                inventory_sample,
                columns=column_names
            )
            print(df_inventory.to_string())

            # Check USERS table
            print("\n" + "=" * 70)
            print("USERS TABLE STRUCTURE")
            print("=" * 70)

            cursor.execute("DESCRIBE users")
            users_columns = cursor.fetchall()

            print("\nColumns in USERS table:")
            for column in users_columns:
                print(f"   • {column[0]:<20} | Type: {column[1]:<15}")

            cursor.execute("SELECT user_id, username, role FROM users")
            users_data = cursor.fetchall()

            print("\nUsers in database:")
            for user_data in users_data:
                print(
                    f"   • ID: {user_data[0]}, "
                    f"Username: {user_data[1]}, "
                    f"Role: {user_data[2]}"
                )

            cursor.close()
            connection.close()

            print("\n" + "=" * 70)
            print("Schema check complete!")
            print("=" * 70)

    except Error as error:
        print(f"\nERROR: {error}")


if __name__ == "__main__":
    check_schema()
    input("\nPress Enter to exit...")
