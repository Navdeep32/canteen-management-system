# Utility Scripts

This folder contains utility scripts used for database setup, connectivity testing, and verification of the Canteen Management System.

## Script Structure

```text
scripts/
└── database/
   ├── test_connection.py
   ├── setup_users_table.py
   └── check_database_schema.py

```

---

## Database Scripts

### 1. Test Database Connection

**File:** `scripts/database/test_connection.py`

**Purpose:**
Tests the MySQL connection and verifies that the `canteen` database is accessible.

**Use for:**

* Initial project setup
* Checking database connectivity
* Troubleshooting connection issues

**Run:**

```bash
python scripts/database/test_connection.py
```

The script prompts for MySQL connection details and checks the database, tables, and basic record counts. It can also create the Streamlit secrets file used by the application.

---

### 2. Setup Users Table

**File:** `scripts/database/setup_users_table.py`

**Purpose:**

Creates the `users` table required for user authentication and adds a default admin user if no users exist.

> If no users exist, the script creates a default development account:
>
> **Username:** `admin`  
> **Password:** `admin123`
>
> These credentials are intended only for local/academic use and should be changed before any real deployment.

**Use for:**

* Creating the `users` table
* Fixing a missing `users` table
* Creating the default admin account
* Verifying users and database tables

**Run:**

```bash
python scripts/database/setup_users_table.py
```

The script connects to the `canteen` MySQL database, creates the `users` table if it does not already exist, and adds the default admin account if required. It then displays the users and tables available in the database.

---

### 3. Check Database Schema

**File:** `scripts/database/check_database_schema.py`

**Purpose:**
Inspects the database structure and displays sample data for verification.

**Use for:**

* Verifying database setup
* Checking table structure
* Inspecting sample records
* Troubleshooting schema issues

**Run:**

```bash
python scripts/database/check_database_schema.py
```

The script displays the columns and data types of the main tables and provides sample database information.

---

## Recommended Setup Flow

### 1. Test the database connection

```bash
python scripts/database/test_connection.py
```

### 2. Setup the users table

```bash
python scripts/database/setup_users_table.py
```

This ensures that the `users` table required for application login is available.

### 3. Verify the database structure

```bash
python scripts/database/check_database_schema.py
```

### 4. Start the application

```bash
streamlit run src/app.py
```

The application can then be accessed at:

```text
http://localhost:8501
```

---

## Quick Reference

| Script                     | Purpose                                          |
| -------------------------- | ------------------------------------------------ |
| `test_connection.py`       | Test MySQL connection and database availability  |
| `setup_users_table.py`     | Create the users table and default admin account |
| `check_database_schema.py` | Inspect database structure and sample data       |

---

**Project:** Canteen Sales & Inventory Management System
**Technology:** Python, MySQL, Streamlit, Pandas, Matplotlib
**Type:** Academic Project