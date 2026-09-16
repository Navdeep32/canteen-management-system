"""
Database Connection Test

Verifies the MySQL connection and checks the main tables
of the Canteen Management System database.
"""

import mysql.connector
from mysql.connector import Error


def test_connection():
    """Test MySQL database connection and verify main tables."""

    print("=" * 60)
    print("MySQL Connection Test")
    print("=" * 60)

    try:
        print("\nEnter your MySQL credentials:")
        host = input("Host (default: localhost): ").strip() or "localhost"
        user = input("Username (default: root): ").strip() or "root"
        password = input("Password: ").strip()
        database = input("Database (default: canteen): ").strip() or "canteen"

        print("\nTesting connection...")

        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if not connection.is_connected():
            print("\nERROR: Could not connect to MySQL.")
            return False

        print(f"\nConnected to MySQL server: {connection.get_server_info()}")
        print(f"Connected to database: {database}")

        cursor = connection.cursor()

        # Check available tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        print(f"\nFound {len(tables)} table(s):")

        for table in tables:
            table_name = table[0]

            cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
            count = cursor.fetchone()[0]

            print(f"   • {table_name}: {count} records")

        cursor.close()
        connection.close()

        print("\n" + "=" * 60)
        print("Database connection test completed successfully.")
        print("=" * 60)

        return True

    except Error as error:
        print(f"\nERROR: {error}")

        print("\nTroubleshooting:")
        print("   • Check that MySQL is running.")
        print("   • Verify the host, username, and password.")
        print("   • Make sure the database exists.")
        print("   • Check that the MySQL user has database access.")

        return False


if __name__ == "__main__":
    test_connection()
    input("\nPress Enter to exit...")
