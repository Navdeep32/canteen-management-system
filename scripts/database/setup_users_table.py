"""
Quick Fix Script - Creates Users Table
Run this to add the missing users table to your existing database
"""

import mysql.connector
from mysql.connector import Error

def create_users_table():
    """Create users table in existing database"""
    
    print("=" * 60)
    print("🔧 Quick Fix - Creating Users Table")
    print("=" * 60)
    
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
            print("✅ Connected to MySQL")
            
            cursor = connection.cursor()
            
            # Create users table
            print("\n📝 Creating users table...")
            
            create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            cursor.execute(create_table_query)
            print("✅ Users table created")
            
            # Insert default admin user
            print("\n👤 Creating default admin user...")
            
            insert_user_query = """
            INSERT INTO users (username, password_hash, role) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE username=username
            """
            
            # Password 'admin123' hashed with SHA-256
            admin_data = (
                'admin',
                '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',
                'admin'
            )
            
            cursor.execute(insert_user_query, admin_data)
            connection.commit()
            print("✅ Admin user created")
            
            # Verify
            cursor.execute("SELECT username, role FROM users")
            users = cursor.fetchall()
            
            print("\n📋 Users in database:")
            for user in users:
                print(f"   • Username: {user[0]}, Role: {user[1]}")
            
            # Show all tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            print(f"\n📊 All tables in database:")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM `{table[0]}`")
                count = cursor.fetchone()[0]
                print(f"   • {table[0]}: {count} records")
            
            cursor.close()
            connection.close()
            
            print("\n" + "=" * 60)
            print("✅ SUCCESS! Database is now ready!")
            print("=" * 60)
            print("\n📝 Login Credentials:")
            print("   Username: admin")
            print("   Password: admin123")
            print("\n💡 Next step:")
            print("   Run: streamlit run app.py")
            print("=" * 60)
            
    except Error as e:
        print(f"\n❌ ERROR: {e}")
        print("\n🔧 Manual Solution:")
        print("   Run this SQL in MySQL:")
        print("""
   USE canteen;
   
   CREATE TABLE users (
       user_id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(100) UNIQUE NOT NULL,
       password_hash VARCHAR(255) NOT NULL,
       role VARCHAR(50) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   
   INSERT INTO users (username, password_hash, role) 
   VALUES ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin');
        """)

if __name__ == "__main__":
    create_users_table()
    
    print("\n👋 Press Enter to exit...")
    input()