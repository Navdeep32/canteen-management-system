# Quick Start Guide

## Prerequisites

- Python 3.8+
- MySQL Server running
- Git

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/canteen-management-system.git
cd canteen-management-system
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create MySQL Database

```bash
mysql -u root -p

CREATE DATABASE canteen;
EXIT;
```

### 5. Create Secrets File

```bash
mkdir .streamlit
```

Create `.streamlit/secrets.toml` with:

```toml
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_mysql_password"
DB_NAME = "canteen"
```

Replace `your_mysql_password` with your actual MySQL password.

⚠️ **Never commit this file to GitHub!** (Already in .gitignore)

### 6. Test Connection

```bash
python scripts/database/test_connection.py
```

Should output:
SUCCESS! Connected to MySQL
Connected to database: canteen

### 7. Run Application

```bash
streamlit run src/app.py
```

Opens at: `http://localhost:8501`

### 8. Create Admin User (Optional)

```bash
python scripts/database/setup_users_table.py
```

**Login with:**
- Username: `admin`
- Password: `admin123`

## Troubleshooting

### "ModuleNotFoundError"

```bash
pip install -r requirements.txt --force-reinstall
```

### MySQL Connection Error

```bash
# Verify MySQL running:
mysql -u root -p

# Check credentials in .streamlit/secrets.toml
cat .streamlit/secrets.toml  # Mac/Linux
type .streamlit/secrets.toml  # Windows
```

### Port 8501 Already in Use

```bash
# Run on different port:
streamlit run src/app.py --server.port 8502

# Or kill existing process:
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Mac/Linux:
lsof -i :8501
kill -9 <PID>
```

## Next Steps

1. Load sample data from `data/sample/` folder
2. Explore dashboards
3. Create sales entries
4. View reports

---

**Version**: 1.0