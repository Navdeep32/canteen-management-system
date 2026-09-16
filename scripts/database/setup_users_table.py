"""
Users Table Setup Utility

Creates the users table in the Canteen Management System database
and adds a default admin user if no users exist.
"""

import hashlib

import mysql.connector
from mysql.connector import Error


def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def setup_users_table():
    """Create the users table and default admin user."""

    print("=" * 60)
    print("Users Table Setup")
    print("=" * 60)

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

        if not connection.is_connected():
            print("\nERROR: Could not connect to the database.")
            return

        print(f"\nConnected to database: {database}")

        cursor = connection.cursor()

        # Create users table if it does not exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(50) DEFAULT 'staff',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()
        print("Users table is ready.")

        # Check whether any users already exist
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]

        if user_count == 0:
            cursor.execute(
                """
                INSERT INTO users (username, password_hash, role)
                VALUES (%s, %s, %s)
                """,
                ("admin", hash_password("admin123"), "admin")
            )

            connection.commit()
            print("Default admin user created.")
            print("Username: admin")
            print("Password: admin123")
        else:
            print(f"Users table already contains {user_count} user(s).")
            print("No default user was created.")

        cursor.close()
        connection.close()

        print("\n" + "=" * 60)
        print("Users table setup completed.")
        print("=" * 60)

    except Error as error:
        print(f"\nERROR: {error}")


if __name__ == "__main__":
    setup_users_table()
    input("\nPress Enter to exit...")
