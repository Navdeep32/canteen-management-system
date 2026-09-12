"""
Database Connection Test Script
Run this script to verify your MySQL connection before running the main app
"""

import mysql.connector
from mysql.connector import Error

def test_connection():
    """Test MySQL database connection"""
    
    print("=" * 60)
    print("🔍 MySQL Connection Test")
    print("=" * 60)
    
    # Get credentials
    print("\n📝 Enter your MySQL credentials:")
    host = input("Host (default: localhost): ").strip() or "localhost"
    user = input("Username (default: root): ").strip() or "root"
    password = input("Password: ").strip()
    database = input("Database (default: canteen): ").strip() or "canteen"  
    
    print("\n🔄 Testing connection...")
    
    try:
        # Attempt connection
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"\n✅ SUCCESS! Connected to MySQL Server version {db_info}")
            
            # Get cursor
            cursor = connection.cursor()
            
            # Check database
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"✅ Connected to database: {record[0]}")
            
            # Check tables
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            
            print(f"\n📊 Found {len(tables)} tables:")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM `{table[0]}`;")
                count = cursor.fetchone()[0]
                print(f"   • {table[0]}: {count} records")
            
            # Test query
            cursor.execute("SELECT COUNT(*) FROM sales;")
            sales_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM inventory;")
            inventory_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM users;")
            users_count = cursor.fetchone()[0]
            
            print(f"\n📈 Database Statistics:")
            print(f"   • Sales records: {sales_count}")
            print(f"   • Inventory records: {inventory_count}")
            print(f"   • Users: {users_count}")
            
            cursor.close()
            connection.close()
            
            print("\n" + "=" * 60)
            print("✅ All tests passed! Your database is ready.")
            print("=" * 60)
            print("\n💡 Next steps:")
            print("   1. Create .streamlit/secrets.toml with your credentials")
            print("   2. Run: streamlit run app.py")
            print("   3. Login with: admin / admin123")
            print("\n")
            
            return True
            
    except Error as e:
        print(f"\n❌ ERROR: {e}")
        print("\n🔧 Troubleshooting tips:")
        
        if "Access denied" in str(e):
            print("   • Check your username and password")
            print("   • Make sure MySQL user has proper permissions")
            
        elif "Unknown database" in str(e):
            print("   • Database doesn't exist. Run setup_database.sql first")
            print("   • Or create manually: CREATE DATABASE canteen_db;")
            
        elif "Can't connect" in str(e):
            print("   • Is MySQL running?")
            print("   • Windows: Check Services")
            print("   • Mac: brew services start mysql")
            print("   • Linux: sudo systemctl start mysql")
            
        else:
            print("   • Check if MySQL is installed and running")
            print("   • Verify host and port settings")
            print("   • Check firewall settings")
        
        print("\n")
        return False

def create_secrets_template():
    """Create a template secrets.toml file"""
    
    print("\n📝 Would you like to create .streamlit/secrets.toml? (y/n): ", end="")
    response = input().strip().lower()
    
    if response == 'y':
        import os
        
        # Get credentials
        print("\n📝 Enter your credentials:")
        host = input("Host (default: localhost): ").strip() or "localhost"
        user = input("Username (default: root): ").strip() or "root"
        password = input("Password: ").strip()
        database = input("Database (default: canteen): ").strip() or "canteen"  

        # Create directory if needed
        if not os.path.exists('.streamlit'):
            os.makedirs('.streamlit')
            print("✅ Created .streamlit directory")
        
        # Create secrets.toml
        secrets_content = f'''# Streamlit secrets configuration
# DO NOT commit this file to git!

DB_HOST = "{host}"
DB_USER = "{user}"
DB_PASSWORD = "{password}"
DB_NAME = "{database}"
'''
        
        with open('.streamlit/secrets.toml', 'w') as f:
            f.write(secrets_content)
        
        print("✅ Created .streamlit/secrets.toml")
        print("⚠️  Remember: Never commit this file to version control!")
        
        # Create .gitignore if needed
        if not os.path.exists('.gitignore'):
            with open('.gitignore', 'w') as f:
                f.write('.streamlit/secrets.toml\n')
                f.write('__pycache__/\n')
                f.write('*.pyc\n')
            print("✅ Created .gitignore")

if __name__ == "__main__":
    success = test_connection()
    
    if success:
        create_secrets_template()
    
    print("\n👋 Test complete. Press Enter to exit...")
    input()