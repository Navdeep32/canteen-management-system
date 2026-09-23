# Utility Scripts

This folder contains utility scripts used for database setup, and verification of the Canteen Management System.

## Script Structure

```text
scripts/
└── database/
   ├── test_connection.py
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

### 2. Check Database Schema

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

### 2. Start the application

```bash
streamlit run src/app.py
```

### 3. Verify the database structure

```bash
python scripts/database/check_database_schema.py
```

The application can then be accessed at:

```text
http://localhost:8501
```

---

## Quick Reference

| Script                     | Purpose                                         |
| -------------------------- | ----------------------------------------------- |
| `test_connection.py`       | Test MySQL connection and database availability |
| `check_database_schema.py` | Inspect database structure and sample data      |

---

**Project:** Canteen Sales & Inventory Management System
**Technology:** Python, MySQL, Streamlit, Pandas, Matplotlib
**Type:** Academic Project
