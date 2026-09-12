# System Architecture Documentation

Complete overview of the Canteen Management System architecture, design patterns, and component interactions.

---

## Architecture Overview

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (Streamlit)                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Login  │ Sales Entry │ Inventory │ Dashboard │ Reports  │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│              APPLICATION LAYER (Python/Streamlit)               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                     src/app.py                           │   │
│  │  • Authentication  • Sales Logic  • Inventory Logic      │   │
│  │  • Validation      • Data Process • Reporting            │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│              DATABASE LAYER (MySQL)                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  users Table  │  sales Table  │  inventory Table        │    │
│  │  Indexes      │  Constraints  │  Relationships          │    │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## System Components

### 1. **Presentation Layer** (Streamlit UI)

Located in: `src/app.py`

**Responsibilities**:
- Display user interface pages
- Handle user interactions and form inputs
- Validate user input before processing
- Format and display output data
- Manage page navigation via sidebar

**Key Pages & Components**:

```
src/app.py - Single File Application
│
├── LOGIN SYSTEM
│   ├── login_page()
│   │   ├── Username input
│   │   ├── Password input
│   │   └── Authentication
│   └── logout functionality
│
├── MAIN DASHBOARD
│   ├── show_dashboard()
│   ├── Key metrics (total sales, stock status, user count)
│   ├── Sales overview chart
│   ├── Inventory status visualization
│   └── Quick statistics
│
├── DATA ENTRY
│   ├── show_add_entry()
│   ├── Sales Entry Form
│   │   ├── Date picker
│   │   ├── Item selection
│   │   ├── Quantity input
│   │   ├── Price input
│   │   └── Payment mode selection
│   └── Inventory Entry Form
│       ├── Item name
│       ├── Stock in/out quantities
│       ├── Unit cost
│       └── Supplier name
│
├── BULK UPLOAD
│   ├── File upload widget (CSV/Excel)
│   ├── File validation
│   ├── Data preview
│   └── Batch import
│
├── ANALYTICS & REPORTS
│   ├── show_analytics()
│   ├── Sales trends chart
│   ├── Top products analysis
│   ├── Monthly sales report
│   ├── Category-wise breakdown
│   └── Inventory analysis
│
├── DATA MANAGEMENT
│   ├── show_data_management()
│   ├── Search functionality
│   ├── Pagination (10, 25, 50, 100 rows)
│   ├── View records
│   ├── Edit records
│   └── Delete records
│
└── SIDEBAR NAVIGATION
    ├── User info display
    ├── Logout button
    └── Page selection (Dashboard, Add Entry, Upload, Analytics, Manage Data)
```

---

### 2. **Application Layer** (Business Logic)

Located in: `src/app.py` (All business logic in single file)

**Core Functions**:

#### Authentication & Security
```python
hash_password(password)
  └─ SHA-256 hashing of passwords
  
verify_user(username, password)
  └─ Validate user credentials against database
  
create_default_user(conn)
  └─ Create admin user if not exists
  
check_user_exists(conn, username)
  └─ Check if username already exists
```

#### Database Operations
```python
init_connection()
  └─ Create MySQL connection using credentials from secrets.toml
  
create_tables(connection)
  └─ Auto-create tables: users, sales, inventory
  
insert_sale(conn, date, item, category, qty, price, mode, customer_type)
  └─ Add sales transaction to database
  
insert_inventory(conn, date, item, stock_in, stock_used, unit_cost, supplier)
  └─ Add inventory record to database
  
get_sales_data(conn)
  └─ Fetch all sales records
  
get_inventory_data(conn)
  └─ Fetch all inventory records
  
delete_sale(conn, sale_id)
  └─ Delete specific sales record
  
delete_inventory(conn, inventory_id)
  └─ Delete specific inventory record
```

#### Data Processing & Analytics
```python
calculate_sales_metrics(sales_df)
  └─ Compute total sales, daily avg, etc.
  
get_low_stock_items(conn, threshold=20)
  └─ Get items below minimum stock level
  
get_top_products(sales_df, limit=10)
  └─ Identify best-selling items
  
calculate_monthly_trends(sales_df)
  └─ Generate monthly sales analysis
```

#### File Operations
```python
process_upload(uploaded_file, file_type)
  └─ Handle CSV/Excel file uploads
  └─ Parse and validate data
  └─ Insert into database
```

#### Display Functions
```python
show_dashboard(conn)
  └─ Display main dashboard with metrics and charts
  
show_add_entry(conn)
  └─ Display forms for manual data entry
  
show_analytics(conn)
  └─ Display reports and visualizations
  
show_data_management(conn)
  └─ Display searchable, paginated data tables with CRUD options
```

---

### 3. **Data Layer** (MySQL Database)

Located in: MySQL Server (database: `canteen`)

**Table Structures**:

#### Users Table
```sql
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Columns**:
- `user_id`: Unique identifier
- `username`: Login username (unique)
- `password_hash`: SHA-256 hashed password
- `role`: User role (admin, staff, manager)
- `created_at`: Account creation timestamp

#### Sales Table
```sql
CREATE TABLE sales (
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
)
```

**Columns**:
- `sale_id`: Unique transaction ID
- `date_of_sale`: Date of transaction
- `item_name`: Product name
- `category`: Product category
- `quantity_sold`: Units sold
- `unit_price`: Price per unit
- `total_amount`: Total sale amount (qty × price)
- `payment_mode`: Cash, Card, UPI, etc.
- `customer_type`: Student, Faculty, Visitor
- `created_at`: Record creation timestamp

#### Inventory Table
```sql
CREATE TABLE inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    date_of_entry DATE NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    stock_in INT NOT NULL,
    stock_used INT NOT NULL,
    remaining_stock INT NOT NULL,
    unit_cost DECIMAL(10, 2),
    supplier_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Columns**:
- `inventory_id`: Unique record ID
- `date_of_entry`: Date of inventory update
- `item_name`: Product name
- `stock_in`: Quantity received
- `stock_used`: Quantity used/sold
- `remaining_stock`: Current stock level
- `unit_cost`: Cost per unit
- `supplier_name`: Vendor/supplier name
- `created_at`: Record creation timestamp

---

## Configuration & Secrets

### Database Configuration

Location: `.streamlit/secrets.toml` (NOT committed to Git)

```toml
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_mysql_password"
DB_NAME = "canteen"
```

**Access in Code**:
```python
host = st.secrets.get("DB_HOST", "localhost")
user = st.secrets.get("DB_USER", "root")
password = st.secrets.get("DB_PASSWORD", "")
database = st.secrets.get("DB_NAME", "canteen")
```

---

## Data Flow Diagrams

### 1. User Login Flow

```
┌──────────────┐
│ User enters  │
│ credentials  │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ Validate input       │ (check not empty)
│ (check format)       │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Hash password        │ (SHA-256)
│ with hashlib         │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Query database:      │
│ SELECT from users    │ (match username)
│ WHERE username = ?   │
└──────┬───────────────┘
       │
       ├─ User found ──┐
       │               │
       │               ▼
       │          ┌──────────────────┐
       │          │ Compare hashes   │
       │          └──────┬───────────┘
       │                 │
       │                 ├─ Match  ─────┐
       │                 │              │
       │                 │              ▼
       │                 │      ┌──────────────────┐
       │                 │      │ Set session      │
       │                 │      │ st.session_state │
       │                 │      │['logged_in']=True│
       │                 │      └──────┬───────────┘
       │                 │             │
       │                 │             ▼
       │                 │      ┌──────────────────┐
       │                 │      │ Show Dashboard   │
       │                 │      └──────────────────┘
       │                 │
       │                 └─ No Match ──┐
       │                               │
       └─ User not found ─────┬────────┘
                              │
                              ▼
                        ┌──────────────────┐
                        │ Show error       │
                        │ message          │
                        │ Return to login  │
                        └──────────────────┘
```

### 2. Sales Entry Flow

```
┌────────────────────┐
│ User fills form    │ (date, item, qty, price, etc.)
└────────┬───────────┘
         │
         ▼
┌───────────────────┐
│ Validate data:    │
│ • Date format ✓   |
│ • Qty > 0 ✓       |
│ • Price > 0 ✓     |
│ • Required fields │
└────────┬──────────┘
         │
         ▼
┌────────────────────┐
│ Calculate total:   │
│ total = qty × price│
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│ INSERT INTO sales  │
│ (all fields)       │
└────────┬───────────┘
         │
         ├─ Success ─┐
         │           │
         │           ▼
         │     ┌──────────────────┐
         │     │ Show success msg │
         │     │ Clear form       │
         │     │ Refresh list     │
         │     └──────────────────┘
         │
         └─ Error ──┐
                    │
                    ▼
            ┌──────────────────┐
            │ Show error msg   │
            │ Keep data entered│
            └──────────────────┘
```

### 3. File Upload Flow

```
┌──────────────────┐
│ User selects CSV │
│ or Excel file    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Read file using: │
│ • pd.read_csv()  │
│ • pd.read_excel()│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Validate data:   │
│ • Column names   │
│ • Data types     │
│ • Required cols  │
└────────┬─────────┘
         │
         ├─ Valid ─┐
         │         │
         │         ▼
         │    ┌──────────────────┐
         │    │ Process each row │
         │    │ INSERT into DB   │
         │    │ (batch insert)   │
         │    └────────┬─────────┘
         │             │
         │             ▼
         │    ┌──────────────────┐
         │    │ Show results:    │
         │    │ X rows imported  │
         │    │ Y rows failed    │
         │    └──────────────────┘
         │
         └─ Invalid ─┐
                     │
                     ▼
            ┌──────────────────┐
            │ Show error:      │
            │ Missing columns, │
            │ wrong format,    │
            │ etc.             │
            └──────────────────┘
```

### 4. Dashboard Analytics Flow

```
┌──────────────────┐
│ User opens       │
│ Dashboard page   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Fetch data from  │
│ database:        │
│ • All sales      │
│ • All inventory  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Process with     │
│ pandas:          │
│ • Group data     │
│ • Calculate sums │
│ • Find trends    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Generate charts: │
│ • Matplotlib     │
│ • Sales trends   │
│ • Top products   │
│ • Metrics boxes  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Display in UI    │
│ • Charts render  │
│ • Metrics show   │
│ • Tables display │
└──────────────────┘
```

---

## Technology Stack

### Frontend
- **Streamlit 1.28.1**: Web application framework for Python
- **Streamlit Widgets**: Forms, buttons, inputs, displays
- **Sidebar Navigation**: Multi-page app structure

### Backend
- **Python 3.8+**: Programming language
- **Pandas 2.1.0**: Data manipulation and analysis
- **NumPy 1.24.3**: Numerical computations

### Database
- **MySQL 5.7+ or 8.0+**: Relational database
- **mysql-connector-python 8.2.0**: MySQL driver for Python

### Data Visualization
- **Matplotlib 3.8.1**: Static charts, plots, visualizations

### File Support
- **openpyxl 3.1.2**: Read/write Excel .xlsx files
- **xlrd 2.0.1**: Read Excel .xls files
- **Pandas CSV support**: Read/write CSV files

### Development Tools
- **Jupyter Notebook**: Data exploration and analysis
- **Git**: Version control

---

## Security Architecture

### Authentication Flow

```
┌─────────────────────┐
│ User Credentials    │
│ (username, pwd)     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Input Validation    │
│ • Not empty?        │
│ • Valid format?     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Hash Password       │
│ SHA-256             │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Query Database      │
│ Find user record    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Compare Password    │
│ Hash Match?         │
└────────┬────────────┘
         │
         ├─ YES ─┐
         │       │
         │       ▼
         │   ┌──────────────────┐
         │   │ Set Session:     │
         │   │ logged_in = True │
         │   │ Store user info  │
         │   └──────────────────┘
         │
         └─ NO ──┐
                 │
                 ▼
            ┌──────────────────┐
            │ Show error       │
            │ Return to login  │
            └──────────────────┘
```

### Data Security Measures

1. **Password Security**
   - Hashed with SHA-256
   - Never stored as plain text
   - Using Python's hashlib

2. **Database Security**
   - Credentials in `.streamlit/secrets.toml` (NOT in repo)
   - No hardcoded passwords in source code
   - Input validation prevents SQL injection
   - Parameterized queries using %s placeholders

3. **Session Management**
   - Session state stored in `st.session_state`
   - Login flag: `st.session_state['logged_in']`
   - User info cached in session
   - Logout clears session

4. **File Uploads**
   - Validate file extension (CSV, xlsx, xls only)
   - Validate file content structure
   - Sanitize data before inserting

---

## Deployment Architecture

### Development Environment
```
Local Machine
├── Python 3.8+ (with venv)
├── MySQL Server (local)
├── .streamlit/secrets.toml (local, not in git)
├── Source code (from GitHub)
└── streamlit run src/app.py
```

### Production Environment (Recommended)
```
Cloud Server (AWS/Google Cloud/Heroku)
├── Python 3.8+
├── MySQL (RDS, Cloud SQL, or managed service)
├── .streamlit/secrets.toml (via environment variables)
├── Streamlit Cloud OR Docker Container
├── SSL/TLS (HTTPS)
└── Monitoring & Logging
```

---

## Error Handling

### Error Categories

```
Application Errors
├── Validation Errors
│   ├── Empty fields
│   ├── Invalid data format
│   └── Out of range values
│
├── Database Errors
│   ├── Connection failed
│   ├── Query execution error
│   └── Constraint violation
│
├── Authentication Errors
│   ├── Invalid credentials
│   ├── User not found
│   └── Session expired
│
└── File Handling Errors
    ├── Invalid file format
    ├── Corrupted data
    └── File not found
```

### Error Handling Pattern

```python
try:
    # Attempt operation
    connection = init_connection()
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()
    
except mysql.connector.Error as e:
    st.error(f"Database Error: {e}")
    
except ValueError as e:
    st.error(f"Invalid Input: {e}")
    
except Exception as e:
    st.error(f"Unexpected Error: {e}")
    
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
```

---

## Performance Optimization

### Database Optimization
- Indexes on frequently queried columns
- Appropriate data types (INT for numbers, DATE for dates)
- Connection pooling ready for scale

### Application Optimization
- Pandas for efficient data processing
- Caching via Streamlit's `@st.cache_data` decorator
- Pagination for large datasets (10/25/50/100 rows)
- Lazy loading of data on demand

### UI Optimization
- Streamlit automatic caching
- Lightweight matplotlib charts
- Efficient page navigation with sidebar
- Progress indicators for long operations

---

## Scalability Considerations

### Current Architecture (Small to Medium Scale)
- Single server deployment
- MySQL on same or dedicated server
- Suitable for 100-1000 active users
- Daily transaction volume: 1000-10000 records

### Scaling Strategies

**For Database**:
- Read replicas for reporting queries
- Connection pooling
- Archive old data to separate tables
- Index optimization

**For Application**:
- Horizontal scaling with load balancer
- Caching layer (Redis)
- Async task queue (Celery) for bulk operations
- Microservices for reporting

**For Infrastructure**:
- Cloud deployment (AWS/Google Cloud)
- Auto-scaling groups
- CDN for static assets
- Database replication

---

## Monitoring & Maintenance

### Key Metrics to Monitor
- Database query performance
- Application response time
- Error rates and types
- User activity and login frequency
- Disk space usage
- Database size growth

### Backup Strategy
```bash
# Daily backup
mysqldump -u root -p canteen > backup_$(date +%Y%m%d).sql

# Weekly cloud backup
aws s3 cp backup_*.sql s3://your-bucket/backups/
```

### Recovery Procedure
1. Stop the Streamlit application
2. Restore database from latest backup
3. Verify data integrity
4. Restart application
5. Confirm normal operation

---

## Future Enhancements

```
Planned Features
├── Machine Learning
│   ├── Demand forecasting
│   ├── Sales prediction
│   └── Anomaly detection
│
├── Advanced Reporting
│   ├── Custom report builder
│   ├── Scheduled reports
│   └── Email delivery
│
├── Integration
│   ├── Accounting system
│   ├── Payment gateway
│   ├── Email notifications
│   └── SMS alerts
│
├── Mobile
│   ├── Mobile app
│   ├── QR code scanning
│   └── Offline mode
│
└── Admin Features
    ├── User role management
    ├── Audit logs
    ├── System configuration
    └── Performance dashboards
```

---

## File Structure Reference

```
canteen-management-system/
│
├── src/
│   └── app.py              # Main application (all code in one file)
│
├── data/
│   ├── raw/                # Original data files (excluded from git)
│   ├── cleaned/            # Processed data (excluded from git)
│   └── sample/             # Sample data for testing (included in git)
│       ├── sales_6_months.csv
│       └── inventory_6_months.csv
│
├── notebooks/              # Jupyter analysis
│   ├── 01_sql_import.ipynb
│   └── 02_data_cleaning.ipynb
│
├── scripts/                # Utility scripts
│   ├── database/
│   │   ├── test_connection.py
│   │   └── check_database_schema.py
│   └── maintenance/
│       └── quick_fix.py
│
├── docs/                   # Documentation
│   ├── ARCHITECTURE.md
│   ├── DATABASE_SCHEMA.md
│   ├── USER_GUIDE.md
│   ├── SCRIPTS.md
│   └── TROUBLESHOOTING.md
│
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml        # NOT in git (in .gitignore)
│
├── README.md               # Project overview
├── QUICK_START.md          # Setup guide
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore rules
├── LICENSE                 # MIT License
└── [other config files]
```

---

## Key Takeaways

1. **Single File Architecture**: All code in `src/app.py` for simplicity
2. **Security First**: Passwords hashed, secrets protected, input validated
3. **MySQL Database**: Three tables (users, sales, inventory) with proper structure
4. **Streamlit UI**: Clean sidebar navigation with multiple functional pages
5. **Easy Setup**: Auto-creates tables on first run, no manual SQL needed
6. **Data Support**: CSV and Excel file uploads with validation
7. **Professional Features**: Analytics, reports, dashboards, data management
8. **Scalable**: Ready for growth with proper optimization strategies

---

**Version**: 1.0  
**Last Updated**: July 2026  
**Architecture Pattern**: Single-file Streamlit application with MySQL backend  
**Status**: Production Ready