# Database Schema Documentation

Complete documentation of the Canteen Management System database structure.

## Database Overview

**Database Name**: `canteen`  
**Database Type**: MySQL (5.7+ or 8.0+)  
**Total Tables**: 3 (Users, Sales, Inventory)  
**Charset**: UTF8MB4 (supports all characters)

---

## Table 1: USERS

Stores user account information for authentication and access control.

### Structure

```sql
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Column Details

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| `user_id` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier |
| `username` | VARCHAR(100) | UNIQUE, NOT NULL | Login username (must be unique) |
| `password_hash` | VARCHAR(255) | NOT NULL | SHA-256 hashed password |
| `role` | VARCHAR(50) | NOT NULL | User role (admin, staff, manager) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |

### Indexes

```sql
CREATE UNIQUE INDEX idx_username ON users(username);
CREATE INDEX idx_role ON users(role);
```

### Sample Data

```sql
INSERT INTO users (username, password_hash, role) VALUES
('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin');
```

**Note**: The hash `240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9` is SHA-256 of `admin123`

### Security Notes

- Passwords stored as SHA-256 hashes (never plain text)
- Never expose password_hash in responses
- Implement password strength requirements
- Usernames must be unique

---

## Table 2: SALES

Records all sales transactions made in the canteen.

### Structure

```sql
CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    date_of_sale DATE NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    quantity_sold INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_mode VARCHAR(50),
    customer_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Column Details

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| `sale_id` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique sale identifier |
| `date_of_sale` | DATE | NOT NULL | Date when sale occurred |
| `item_name` | VARCHAR(255) | NOT NULL | Name of item sold (e.g., "Samosa", "Tea") |
| `category` | VARCHAR(100) | | Category (e.g., "Snacks", "Beverages", "Lunch") |
| `quantity_sold` | INT | NOT NULL | Number of units sold (must be > 0) |
| `unit_price` | DECIMAL(10,2) | NOT NULL | Price per unit (must be > 0) |
| `total_amount` | DECIMAL(10,2) | NOT NULL | quantity_sold × unit_price |
| `payment_mode` | VARCHAR(50) | | Payment method (Cash, Card, UPI, Cheque) |
| `customer_type` | VARCHAR(50) | | Customer category (Student, Staff, Guest, Visitor) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |

### Indexes

```sql
CREATE INDEX idx_date_of_sale ON sales(date_of_sale);
CREATE INDEX idx_category ON sales(category);
CREATE INDEX idx_item_name ON sales(item_name);
```

### Sample Data

```sql
INSERT INTO sales (date_of_sale, item_name, category, quantity_sold, unit_price, total_amount, payment_mode, customer_type)
VALUES 
('2024-01-15', 'Samosa', 'Snacks', 10, 5.00, 50.00, 'Cash', 'Student'),
('2024-01-15', 'Tea', 'Beverages', 25, 10.00, 250.00, 'Card', 'Staff'),
('2024-01-15', 'Lunch Combo', 'Lunch', 5, 80.00, 400.00, 'UPI', 'Visitor');
```

### Business Rules

- `total_amount` = `quantity_sold` × `unit_price`
- `date_of_sale` must not be in the future
- `quantity_sold` must be > 0
- `unit_price` must be > 0
- All fields required except `payment_mode` and `customer_type`

### Useful Queries

**Daily Sales Total**:
```sql
SELECT DATE(date_of_sale) as date, SUM(total_amount) as daily_total
FROM sales
GROUP BY DATE(date_of_sale)
ORDER BY date DESC;
```

**Top Selling Items**:
```sql
SELECT item_name, SUM(quantity_sold) as total_qty, SUM(total_amount) as revenue
FROM sales
GROUP BY item_name
ORDER BY total_qty DESC
LIMIT 10;
```

**Sales by Category (Last 30 days)**:
```sql
SELECT category, SUM(total_amount) as category_total, COUNT(*) as transaction_count
FROM sales
WHERE date_of_sale >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY category
ORDER BY category_total DESC;
```

**Monthly Sales**:
```sql
SELECT YEAR(date_of_sale) as year, MONTH(date_of_sale) as month, SUM(total_amount) as monthly_total
FROM sales
GROUP BY YEAR(date_of_sale), MONTH(date_of_sale)
ORDER BY year DESC, month DESC;
```

---

## Table 3: INVENTORY

Tracks inventory movements and current stock levels.

### Structure

```sql
CREATE TABLE IF NOT EXISTS inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    date_of_entry DATE NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    stock_in INT NOT NULL,
    stock_used INT NOT NULL,
    remaining_stock INT NOT NULL,
    unit_cost DECIMAL(10, 2),
    supplier_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Column Details

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| `inventory_id` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique inventory record ID |
| `date_of_entry` | DATE | NOT NULL | Date of inventory transaction |
| `item_name` | VARCHAR(255) | NOT NULL | Name of item |
| `stock_in` | INT | NOT NULL | Quantity received/added (≥ 0) |
| `stock_used` | INT | NOT NULL | Quantity used/consumed (≥ 0) |
| `remaining_stock` | INT | NOT NULL | Current stock level = stock_in - stock_used |
| `unit_cost` | DECIMAL(10,2) | | Cost per unit for inventory valuation |
| `supplier_name` | VARCHAR(255) | | Name of supplier/vendor |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record creation time |

### Indexes

```sql
CREATE INDEX idx_date_of_entry ON inventory(date_of_entry);
CREATE INDEX idx_item_name ON inventory(item_name);
CREATE INDEX idx_supplier_name ON inventory(supplier_name);
```

### Sample Data

```sql
INSERT INTO inventory (date_of_entry, item_name, stock_in, stock_used, remaining_stock, unit_cost, supplier_name)
VALUES 
('2024-01-15', 'Samosa', 50, 10, 40, 3.50, 'Local Baker'),
('2024-01-15', 'Tea', 200, 25, 175, 8.00, 'Tea Supplier'),
('2024-01-15', 'Bread', 30, 5, 25, 15.00, 'Bakery Co.'),
('2024-01-15', 'Milk', 100, 20, 80, 25.00, 'Dairy Farm');
```

### Business Rules

- `remaining_stock` = `stock_in` - `stock_used`
- `stock_in` must be ≥ 0
- `stock_used` must be ≥ 0
- `remaining_stock` must be ≥ 0
- Alert when `remaining_stock` < 20 (low stock threshold)
- All critical fields required

### Useful Queries

**Current Stock Levels**:
```sql
SELECT item_name, remaining_stock, unit_cost, 
       (remaining_stock * unit_cost) as inventory_value
FROM inventory
ORDER BY item_name;
```

**Low Stock Items** (Less than 20 units):
```sql
SELECT item_name, remaining_stock, supplier_name
FROM inventory
WHERE remaining_stock < 20
ORDER BY remaining_stock ASC;
```

**Total Inventory Value**:
```sql
SELECT SUM(remaining_stock * unit_cost) as total_inventory_value
FROM inventory;
```

**Stock Usage Report**:
```sql
SELECT item_name, SUM(stock_in) as total_received, SUM(stock_used) as total_used, remaining_stock
FROM inventory
GROUP BY item_name
ORDER BY item_name;
```

**Items Running Out Soon**:
```sql
SELECT item_name, remaining_stock, supplier_name
FROM inventory
WHERE remaining_stock < 30
ORDER BY remaining_stock ASC
LIMIT 10;
```

---

## Database Views (Optional)

### View for Sales Analysis

```sql
CREATE VIEW sales_summary AS
SELECT 
    YEAR(date_of_sale) as year,
    MONTH(date_of_sale) as month,
    category,
    SUM(total_amount) as total_revenue,
    SUM(quantity_sold) as total_quantity,
    COUNT(*) as transaction_count
FROM sales
GROUP BY YEAR(date_of_sale), MONTH(date_of_sale), category;
```

### View for Inventory Status

```sql
CREATE VIEW inventory_status AS
SELECT 
    item_name,
    remaining_stock,
    unit_cost,
    (remaining_stock * unit_cost) as inventory_value,
    CASE 
        WHEN remaining_stock < 20 THEN 'Critical'
        WHEN remaining_stock < 50 THEN 'Low'
        ELSE 'Adequate'
    END as stock_status
FROM inventory
ORDER BY remaining_stock ASC;
```

---

## Data Types Reference

| Type | Usage | Size | Range/Notes |
|------|-------|------|------------|
| INT | Whole numbers | 4 bytes | -2,147,483,648 to 2,147,483,647 |
| VARCHAR(n) | Text (limited) | n+1 bytes | Up to 65,535 characters |
| DATE | Date only | 3 bytes | Format: YYYY-MM-DD |
| TIMESTAMP | Date + Time | 4 bytes | Auto-updates on changes |
| DECIMAL(10,2) | Money (precise) | 5 bytes | Up to 10 digits, 2 decimals |

---

## Database Constraints & Keys

### Primary Keys
```sql
PRIMARY KEY (user_id)      -- Auto-increments
PRIMARY KEY (sale_id)      -- Auto-increments
PRIMARY KEY (inventory_id) -- Auto-increments
```

### Unique Constraints
```sql
UNIQUE KEY (username)  -- No duplicate usernames
```

### Required Fields
```
users:      user_id, username, password_hash, role
sales:      sale_id, date_of_sale, item_name, quantity_sold, unit_price, total_amount
inventory:  inventory_id, date_of_entry, item_name, stock_in, stock_used, remaining_stock
```

---

## Database Setup Instructions

### Create Database and Tables

```bash
# 1. Login to MySQL
mysql -u root -p

# 2. Create database
CREATE DATABASE IF NOT EXISTS canteen;

# 3. Use database
USE canteen;

# 4. Create all tables (paste the CREATE TABLE statements from this document)
```

### Quick Setup (All-in-one)

```bash
mysql -u root -p -e "
CREATE DATABASE IF NOT EXISTS canteen;
USE canteen;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    date_of_sale DATE NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    quantity_sold INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_mode VARCHAR(50),
    customer_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    date_of_entry DATE NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    stock_in INT NOT NULL,
    stock_used INT NOT NULL,
    remaining_stock INT NOT NULL,
    unit_cost DECIMAL(10, 2),
    supplier_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE UNIQUE INDEX idx_username ON users(username);
CREATE INDEX idx_role ON users(role);
CREATE INDEX idx_date_of_sale ON sales(date_of_sale);
CREATE INDEX idx_category ON sales(category);
CREATE INDEX idx_item_name ON sales(item_name);
CREATE INDEX idx_date_of_entry ON inventory(date_of_entry);
CREATE INDEX idx_supplier_name ON inventory(supplier_name);
"
```

---

## Database Maintenance

### Regular Backups

```bash
# Backup database
mysqldump -u root -p canteen > canteen_backup.sql

# Backup with timestamp
mysqldump -u root -p canteen > canteen_backup_$(date +%Y%m%d_%H%M%S).sql

# Restore database
mysql -u root -p canteen < canteen_backup.sql
```

### Optimization

```sql
-- Optimize all tables
OPTIMIZE TABLE users;
OPTIMIZE TABLE sales;
OPTIMIZE TABLE inventory;

-- Check table integrity
CHECK TABLE users;
CHECK TABLE sales;
CHECK TABLE inventory;

-- Repair if needed (use carefully)
REPAIR TABLE users;
```

### View Table Sizes

```sql
-- Check database size
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb
FROM information_schema.tables
WHERE table_schema = 'canteen';

-- Count records in each table
SELECT 
    'users' as table_name, COUNT(*) as record_count FROM users
UNION ALL
SELECT 'sales', COUNT(*) FROM sales
UNION ALL
SELECT 'inventory', COUNT(*) FROM inventory;
```

---

## Monitoring & Performance

### Monitor Query Performance

```sql
-- Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;

-- Check indexes
SHOW INDEX FROM users;
SHOW INDEX FROM sales;
SHOW INDEX FROM inventory;

-- Analyze query execution
EXPLAIN SELECT * FROM sales WHERE date_of_sale = CURDATE();
```

### Common Optimization Tips

1. **Always use indexes** on frequently searched columns
2. **Use DATE for date-only** fields (not DATETIME)
3. **Specify needed columns** in SELECT (not SELECT *)
4. **Archive old data** to keep tables fast
5. **Regular OPTIMIZE TABLE** maintenance
6. **Use LIMIT** when possible
7. **Avoid wildcard queries** in WHERE clause

---

## Troubleshooting

### Check Database Exists

```bash
mysql -u root -p
SHOW DATABASES;
```

### View Table Structure

```sql
USE canteen;
DESCRIBE users;
DESCRIBE sales;
DESCRIBE inventory;
```

### Check for Errors

```sql
-- Check for NULL values in required fields
SELECT * FROM sales WHERE item_name IS NULL;
SELECT * FROM inventory WHERE item_name IS NULL;

-- Find duplicate usernames
SELECT username, COUNT(*) FROM users GROUP BY username HAVING COUNT(*) > 1;
```

### Reset Auto Increment

```sql
-- If needed (be careful)
ALTER TABLE users AUTO_INCREMENT = 1;
ALTER TABLE sales AUTO_INCREMENT = 1;
ALTER TABLE inventory AUTO_INCREMENT = 1;
```

---

## User Roles & Permissions

### Role Types

**Admin**:
- Full access to all tables
- Can create/modify/delete any record
- Can manage users
- Can view all reports

**Staff**:
- Can create sales entries
- Can create inventory entries
- Can view own entries
- Can view reports

**Manager**:
- Can view all data
- Can create/modify own entries
- Can approve entries
- Can generate reports

---

## Future Enhancements

Potential tables to add:

```sql
-- Supplier Management
CREATE TABLE suppliers (
    supplier_id INT PRIMARY KEY AUTO_INCREMENT,
    supplier_name VARCHAR(100) UNIQUE NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Category Management
CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit Log
CREATE TABLE audit_log (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(100),
    table_name VARCHAR(50),
    record_id INT,
    action_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

---

## Support & Help

### Useful Commands

```bash
# Check MySQL version
mysql --version

# Test connection
mysql -u root -p -h localhost

# Access database directly
mysql -u root -p canteen

# Exit MySQL
exit; or quit;
```

### Common Issues

**Connection Refused**:
- Ensure MySQL server is running
- Check host and port settings
- Verify username and password

**Unknown Database**:
- Run: `CREATE DATABASE canteen;`
- Verify database was created: `SHOW DATABASES;`

**Table Doesn't Exist**:
- Check database selected: `USE canteen;`
- List tables: `SHOW TABLES;`
- Create missing tables

---

## Quick Reference

### Create Fresh Database

```bash
mysql -u root -p

DROP DATABASE IF EXISTS canteen;
CREATE DATABASE canteen;
USE canteen;

-- Paste all CREATE TABLE statements here
```

### View All Data

```sql
SELECT * FROM users;
SELECT * FROM sales LIMIT 10;
SELECT * FROM inventory LIMIT 10;
```

### Delete All Data (Be Careful!)

```sql
DELETE FROM sales;
DELETE FROM inventory;
DELETE FROM users;
```

---

**Version**: 1.0  
**Last Updated**: July 2026  
**Database**: MySQL 5.7+  
**Status**: ✅ Production Ready  
**Database Name**: canteen