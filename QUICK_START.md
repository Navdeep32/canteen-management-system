# Quick Start Guide

## Prerequisites

Make sure the following are installed:

* Python 3.8+
* MySQL Server
* Git

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Navdeep32/canteen-management-system.git
cd canteen-management-system
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the MySQL Database

Open MySQL and run:

```sql
CREATE DATABASE canteen;
```

### 5. Configure Database Credentials

Create:

```text
.streamlit/secrets.toml
```

Add your MySQL credentials:

```toml
DB_HOST = "localhost"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_NAME = "canteen"
```

### 6. Test the Database Connection

```bash
python scripts/database/test_connection.py
```

If required, set up the users table:

```bash
python scripts/database/setup_users_table.py
```

### 7. Run the Application

```bash
streamlit run src/app.py
```

Open the application at:

```text
http://localhost:8501
```

### Default Development Login

```text
Username: admin
Password: admin123
```

These credentials are intended only for the academic/development version.

## Troubleshooting

### MySQL Connection Error

* Make sure MySQL Server is running.
* Check the credentials in `.streamlit/secrets.toml`.
* Run the database connection test:

```bash
python scripts/database/test_connection.py
```

### Missing Python Package

Run:

```bash
pip install -r requirements.txt
```

### Database or Table Issues

Check the database structure with:

```bash
python scripts/database/check_database_schema.py
```

For additional issues, see [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).
