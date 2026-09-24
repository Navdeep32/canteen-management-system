# Troubleshooting Guide

Common issues and basic solutions for the Canteen Management System.

---

## 1. Application Won't Start

### Possible causes

* Streamlit is not installed
* Required dependencies are missing
* Another Streamlit process is already running
* There is an error in the application code

### Try

```bash
pip install -r requirements.txt
streamlit run src/app.py
```

If port `8501` is already in use, stop the existing Streamlit process and run the application again.

---

## 2. Database Connection Error

### Symptoms

The application cannot connect to MySQL or displays a database connection error.

### Check

1. Make sure MySQL is running.
2. Verify that the `canteen` database exists.
3. Check the database credentials configured for the application.
4. Test the connection using:

```bash
python scripts/database/test_connection.py
```

If the database does not exist, create it in MySQL:

```sql
CREATE DATABASE canteen;
```

---

## 3. Tables Not Found

### Symptoms

The application reports that a table such as `users`, `sales`, or `inventory` does not exist.

### Try

First, verify the database structure:

```bash
python scripts/database/check_database_schema.py
```

If the `users` table is missing, run the user table setup script:

```bash
python scripts/database/setup_users_table.py
```

Then verify the database structure again:

```bash
python scripts/database/check_database_schema.py
```

For other missing tables, make sure the `canteen` database exists and start the application:

```bash
streamlit run src/app.py
```

The application may create the required application tables during startup.

---

## 4. Data Is Not Saving

### Possible causes

* Database connection issue
* Required form fields are missing
* Invalid input values
* Database table is unavailable

### Try

1. Check that all required fields are completed.
2. Verify the MySQL connection.
3. Refresh the application and try again.
4. Check the database using the schema inspection script.

```bash
python scripts/database/test_connection.py
```

---

## 5. File Upload Issues

### Possible causes

* Unsupported file format
* Incorrect column names
* Invalid or missing data
* Incorrect date or numeric formats

### Try

* Check that the uploaded file uses the format supported by the application.
* Verify that the column names match the expected format.
* Check the uploaded data for missing or invalid values.
* Try uploading a smaller test file first.

Refer to the application/user documentation for the expected file structure.

---

## 6. Charts or Reports Are Empty

### Possible causes

* No data exists for the selected period
* Filters exclude all records
* Database query returned no records

### Try

1. Check whether sales or inventory records exist.
2. Reset the selected filters.
3. Select a wider date range.
4. Refresh the page.

---

## 7. Database Schema Verification

If the application behaves unexpectedly, inspect the database structure using:

```bash
python scripts/database/check_database_schema.py
```

This helps verify:

* Table names
* Column names
* Data types
* Sample records
* Existing users

---

## Useful Commands

### Start the application

```bash
streamlit run src/app.py
```

### Test database connection

```bash
python scripts/database/test_connection.py
```

### Check database schema

```bash
python scripts/database/check_database_schema.py
```

### Setup users table

```bash
python scripts/database/setup_users_table.py
```

---

## Quick Reference

| Issue                     | First Thing to Check                    |
| ------------------------- | --------------------------------------- |
| Application won't start   | Dependencies and Streamlit              |
| Database connection error | MySQL and database credentials          |
| Tables not found          | Run the application and check schema    |
| Data not saving           | Required fields and database connection |
| File upload fails         | File format and column structure        |
| Charts are empty          | Data availability and filters           |

---

**Project:** Canteen Sales & Inventory Management System
**Technology:** Python, MySQL, Streamlit, Pandas, Matplotlib
**Type:** Academic Project
