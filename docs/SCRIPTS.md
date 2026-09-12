# Available Scripts Documentation

Complete guide to using utility scripts in the Canteen Management System.

---

## Overview

```
scripts/
├── database/
│   ├── test_connection.py          ✅ Run FIRST - Test MySQL connection
│   └── check_database_schema.py    ✅ Run ANYTIME - Verify database structure
│
└── maintenance/
    └── quick_fix.py                ✅ Run after app setup - Create admin user
```

---

## Script 1: test_connection.py

**Location**: `scripts/database/test_connection.py`

**Purpose**: Test MySQL connection and optionally create secrets file

**When to use**: 
- During initial setup
- When troubleshooting connection issues
- Before running the main application

### Usage

```bash
python scripts/database/test_connection.py
```

### Step-by-Step

1. **Run the script**:
   ```bash
   python scripts/database/test_connection.py
   ```

2. **Enter your MySQL credentials** (you'll be prompted):
   ```
   Host (default: localhost): localhost
   Username (default: root): root
   Password: your_mysql_password
   Database (default: canteen): canteen
   ```

3. **Expected successful output**:
   ```
   ============================================================
   🔍 MySQL Connection Test
   ============================================================
   
   📝 Enter your MySQL credentials:
   Host (default: localhost): 
   Username (default: root): 
   Password: 
   Database (default: canteen): 
   
   🔄 Testing connection...
   
   ✅ SUCCESS! Connected to MySQL Server version 8.0.33
   ✅ Connected to database: canteen
   
   📊 Found 3 tables:
      • users: 1 records
      • sales: 0 records
      • inventory: 0 records
   
   📈 Database Statistics:
      • Sales records: 0
      • Inventory records: 0
      • Users: 1
   
   ============================================================
   ✅ All tests passed! Your database is ready.
   ============================================================
   ```

### What It Does

✅ Tests MySQL server connection  
✅ Verifies database exists  
✅ Shows all tables and record counts  
✅ Displays database statistics  
✅ Optionally creates `.streamlit/secrets.toml`  
✅ Creates `.gitignore` if needed  

### Troubleshooting

**Error: "Access denied for user 'root'@'localhost'"**
- ❌ Wrong password
- ✅ Check your MySQL password and try again

**Error: "Unknown database 'canteen'"**
- ❌ Database doesn't exist
- ✅ Create it: `mysql -u root -p -e "CREATE DATABASE canteen;"`

**Error: "Can't connect to MySQL server"**
- ❌ MySQL is not running
- ✅ Windows: Start MySQL from Services
- ✅ Mac: `brew services start mysql`
- ✅ Linux: `sudo systemctl start mysql`

---

## Script 2: check_database_schema.py

**Location**: `scripts/database/check_database_schema.py`

**Purpose**: Inspect database structure and view sample data

**When to use**:
- Verify database setup is correct
- Check table columns match app requirements
- Inspect sample data
- Diagnose schema issues

### Usage

```bash
python scripts/database/check_database_schema.py
```

### Expected Output

```
======================================================================
🔍 Database Schema Inspector
======================================================================

✅ Connected to database: canteen

======================================================================
📊 SALES TABLE STRUCTURE
======================================================================

Columns in SALES table:
   • sale_id             | Type: int
   • date_of_sale        | Type: date
   • item_name           | Type: varchar(255)
   • category            | Type: varchar(100)
   • quantity_sold       | Type: int
   • unit_price          | Type: decimal(10,2)
   • total_amount        | Type: decimal(10,2)
   • payment_mode        | Type: varchar(50)
   • customer_type       | Type: varchar(50)
   • created_at          | Type: timestamp

📋 Sample SALES data (first 3 rows):
    sale_id  date_of_sale  item_name
        1    2024-01-15    Samosa
        2    2024-01-15    Tea

======================================================================
📦 INVENTORY TABLE STRUCTURE
======================================================================

Columns in INVENTORY table:
   • inventory_id        | Type: int
   • date_of_entry       | Type: date
   • item_name           | Type: varchar(255)
   • stock_in            | Type: int
   • stock_used          | Type: int
   • remaining_stock     | Type: int
   • unit_cost           | Type: decimal(10,2)
   • supplier_name       | Type: varchar(255)
   • created_at          | Type: timestamp

======================================================================
👥 USERS TABLE STRUCTURE
======================================================================

Columns in USERS table:
   • user_id             | Type: int
   • username            | Type: varchar(100)
   • password_hash       | Type: varchar(255)
   • role                | Type: varchar(50)
   • created_at          | Type: timestamp

📋 Users in database:
   • ID: 1, Username: admin, Role: admin

======================================================================
✅ Schema check complete!
======================================================================
```

### What It Does

✅ Shows all table columns and data types  
✅ Displays sample data from each table  
✅ Lists all users in database  
✅ Verifies table structure is correct  

### Troubleshooting

**Error: "Unknown database 'canteen'"**
- Create it: `mysql -u root -p -e "CREATE DATABASE canteen;"`

**Error: "Table doesn't exist"**
- Run app: `streamlit run src/app.py` (auto-creates tables)

---

## Script 3: quick_fix.py

**Location**: `scripts/maintenance/quick_fix.py`

**Purpose**: Create users table and add default admin user

**When to use**:
- During initial setup
- To reset admin user if forgotten

### Usage

```bash
python scripts/maintenance/quick_fix.py
```

### Expected Output

```
============================================================
🔧 Quick Fix - Creating Users Table
============================================================

✅ Connected to MySQL
📝 Creating users table...
✅ Users table created
👤 Creating default admin user...
✅ Admin user created

📋 Users in database:
   • Username: admin, Role: admin

📊 All tables in database:
   • users: 1 records
   • sales: 0 records
   • inventory: 0 records

============================================================
✅ SUCCESS! Database is now ready!
============================================================

📝 Login Credentials:
   Username: admin
   Password: admin123

💡 Next step:
   Run: streamlit run src/app.py
============================================================
```

### What It Does

✅ Creates users table (if doesn't exist)  
✅ Inserts default admin user (admin / admin123)  
✅ Shows all tables and record counts  

### Troubleshooting

**Error: "Access denied for user 'root'@'localhost'"**
- Update password in script: change `password="pswd"` to your actual password

**Error: "Unknown database 'canteen'"**
- Create it: `mysql -u root -p -e "CREATE DATABASE canteen;"`

**Error: "Duplicate entry 'admin' for key 'username'"**
- Admin already exists - just login with admin / admin123

---

## Recommended Setup Flow

### Step 1: Test Connection ⭐

```bash
python scripts/database/test_connection.py
```

### Step 2: Start the Application

```bash
streamlit run src/app.py
```

App will auto-create all tables on first run.

### Step 3: Create Admin User (Optional)

```bash
python scripts/maintenance/quick_fix.py
```

### Step 4: Verify Database Setup

```bash
python scripts/database/check_database_schema.py
```

### Step 5: Login at http://localhost:8501

- Username: `admin`
- Password: `admin123`

---

## Quick Reference

| Script | Purpose | When | Command |
|--------|---------|------|---------|
| test_connection.py | Test MySQL | Setup | `python scripts/database/test_connection.py` |
| check_database_schema.py | Inspect DB | Anytime | `python scripts/database/check_database_schema.py` |
| quick_fix.py | Create admin | Setup | `python scripts/maintenance/quick_fix.py` |

---

## Common Questions

**Q: Which script should I run first?**  
A: `test_connection.py` - tests MySQL and creates secrets file

**Q: What are default admin credentials?**  
A: Username: `admin` | Password: `admin123`

**Q: Can I change the credentials?**  
A: Yes! Edit the scripts and update the password hash

**Q: What if "Access denied" error?**  
A: Update the hardcoded password in the script to match your MySQL password

**Q: Do I need all 3 scripts?**  
A: No - only test_connection.py and quick_fix.py are essential. check_database_schema.py is for diagnostics

---

## Database Credentials Reference

### Where scripts get credentials:

**test_connection.py**:
- ✅ Prompts you to enter them interactively
- Creates `.streamlit/secrets.toml` file

**check_database_schema.py**:
- Hardcoded: `host="localhost"`, `user="root"`, `password="pswd"`, `database="canteen"`
- Update these in script if different

**quick_fix.py**:
- Hardcoded: `host="localhost"`, `user="root"`, `password="pswd"`, `database="canteen"`
- Update these in script if different

---

## Troubleshooting Checklist

- [ ] MySQL is running (`mysql -u root -p`)
- [ ] Database `canteen` exists (`SHOW DATABASES;`)
- [ ] All 3 tables created (`SHOW TABLES;`)
- [ ] Admin user exists (`SELECT * FROM users;`)
- [ ] Credentials are correct in scripts
- [ ] `.streamlit/secrets.toml` created with correct info
- [ ] Can login with admin / admin123

---

**Version**: 1.0  
**Last Updated**: July 2026  
**Database**: MySQL - canteen  
**Status**: ✅ Production Ready
