# Troubleshooting Guide

Complete troubleshooting guide for common issues in the Canteen Management System.

---

## Quick Troubleshooting Checklist

| Problem | Solution |
|---------|----------|
| App won't load | Restart Streamlit, check port 8501 |
| Can't login | Verify credentials, check database connection |
| Data won't save | Check database connection, verify form validation |
| Slow performance | Check server resources, clear cache |
| Charts not displaying | Check data exists, refresh page |
| File upload fails | Check file format, check file size |

---

## Application Issues

### Issue 1: Application Won't Start

**Error Message**: 
```
StreamlitAPIException: streamlit.errors.StreamlitAPIException
```

**Cause**: Streamlit process crashed or port already in use

**Solution**:

```bash
# Step 1: Kill any existing Streamlit processes
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Mac/Linux:
lsof -i :8501
kill -9 <PID>

# Step 2: Restart application
streamlit run src/app.py

# Step 3: Access at http://localhost:8501
```

---

### Issue 2: Blank White Page

**Symptoms**: Page loads but shows nothing

**Causes**: 
- JavaScript disabled
- Browser cache issues
- Missing dependencies

**Solutions**:

```bash
# Step 1: Enable JavaScript in browser settings

# Step 2: Clear cache and cookies
# Browser menu → Settings → Privacy → Clear browsing data

# Step 3: Try different browser
# Chrome, Firefox, Safari, Edge

# Step 4: Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Step 5: Restart application
streamlit run src/app.py
```

---

### Issue 3: Page Layout Broken

**Symptoms**: Text overlapping, elements misaligned

**Cause**: Browser window too small, viewport issue

**Solutions**:

```bash
# Option 1: Maximize browser window
# Press F11 for fullscreen

# Option 2: Zoom out
# Press Ctrl/Cmd + Minus (-)

# Option 3: Try wider screen resolution
# Minimum: 1024x768 recommended

# Option 4: Refresh page
# Press Ctrl/Cmd + Shift + R (hard refresh)
```

---

### Issue 4: Slow Page Load

**Symptoms**: Takes 30+ seconds to load page

**Causes**:
- Network issues
- Database slow
- Large data loading

**Solutions**:

```bash
# Step 1: Check network connection
ping google.com

# Step 2: Check server resources
# Windows Task Manager: Performance tab
# Mac Activity Monitor
# Linux: top or htop

# Step 3: Restart application
streamlit run src/app.py

# Step 4: Check database performance
# See Database Issues section
```

---

## Login & Authentication Issues

### Issue 5: "Invalid Username or Password"

**Symptoms**: Cannot login even with correct credentials

**Causes**:
- Wrong username/password
- Database connection failed
- User account disabled

**Solutions**:

```bash
# Step 1: Verify credentials
# Check if typed correctly (case-sensitive)
# Ensure CAPS LOCK is off
# Default: admin / admin123

# Step 2: Check database connection
python scripts/database/test_connection.py

# Step 3: Verify user exists in database
# From MySQL prompt:
USE canteen;
SELECT * FROM users WHERE username = 'admin';

# Step 4: Reset password (if admin)
# Contact database administrator
```

---

### Issue 6: Session Expired or Invalid

**Symptoms**: Get redirected to login page unexpectedly

**Cause**: Session timeout, user logged out elsewhere

**Solutions**:

```bash
# Step 1: Login again
# This is normal behavior for security

# Step 2: Keep session active
# Don't leave browser idle for long
# Interact with app regularly

# Step 3: Clear browser cookies
# Settings → Privacy → Clear browsing data
# Select "Cookies and site data"
# Click Clear
# Try login again
```

---

### Issue 7: Account Locked

**Symptoms**: Cannot login after multiple attempts

**Cause**: Too many failed login attempts (security feature)

**Solutions**:

```bash
# Contact administrator to unlock account
# Admin can reset account status
# Try again after account is unlocked
```

---

## Database Connection Issues

### Issue 8: "MySQL Connection Failed"

**Error Message**:
```
mysql.connector.errors.DatabaseError: 1045 (28000): Access denied 
for user 'root'@'localhost' (using password: YES)
```

**Cause**: Database credentials incorrect or MySQL not running

**Solutions**:

**Step 1: Verify MySQL is Running**

```bash
# Windows: Check Services
# Open Services app → Look for MySQL
# Status should be "Running"

# Mac: Check System Preferences
# System Preferences → MySQL → Status: Running

# Linux: Check service status
sudo systemctl status mysql
# Should show: active (running)

# If not running, start MySQL:
sudo systemctl start mysql
```

**Step 2: Test MySQL Connection Directly**

```bash
# From command line
mysql -u root -p -h localhost

# When prompted, enter password
# If successful, you see: mysql>
# If failed, check credentials

# Exit:
EXIT;
```

**Step 3: Verify Credentials in secrets.toml**

```bash
# Check .streamlit/secrets.toml
cat .streamlit/secrets.toml

# Should show:
# DB_HOST = "localhost"
# DB_USER = "root"
# DB_PASSWORD = "your_password"
# DB_NAME = "canteen"
```

**Step 4: Verify Database Exists**

```bash
# Login to MySQL
mysql -u root -p

# List databases
SHOW DATABASES;

# Should see: canteen

# If not exists, create:
CREATE DATABASE canteen;
```

**Step 5: Verify Tables Exist**

```bash
# Check tables
USE canteen;
SHOW TABLES;

# Should see: users, sales, inventory

# If empty, run app once (auto-creates tables)
# Or run: python scripts/maintenance/quick_fix.py
```

**Step 6: Restart Application**

```bash
# If all above checks pass:
streamlit run src/app.py
```

---

### Issue 9: "Lost Connection to MySQL Server"

**Error Message**:
```
mysql.connector.errors.OperationalError: 2013 (HY000): 
Lost connection to MySQL server during query
```

**Causes**:
- MySQL server stopped
- Network disconnection
- Query took too long

**Solutions**:

```bash
# Step 1: Verify MySQL is still running
# Windows: Check Services
# Linux: sudo systemctl status mysql

# Step 2: Restart MySQL
# Windows: Services → MySQL → Restart
# Linux: sudo systemctl restart mysql

# Step 3: Test connection again
python scripts/database/test_connection.py

# Step 4: Restart application
streamlit run src/app.py
```

---

### Issue 10: "Table Not Found" or "No Tables in Database"

**Error Message**:
```
mysql.connector.errors.ProgrammingError: 1146 (42S02): 
Table 'canteen.users' doesn't exist
```

**Cause**: Database tables not created

**Solutions**:

```bash
# Step 1: Check if tables exist
mysql -u root -p canteen
SHOW TABLES;

# If empty, create tables

# Step 2: Run application (auto-creates)
streamlit run src/app.py

# Step 3: Or create admin user and tables
python scripts/maintenance/quick_fix.py

# Step 4: Verify tables created
USE canteen;
SHOW TABLES;
# Should show: users, sales, inventory
```

---

## Data Issues

### Issue 11: Data Not Saving

**Symptoms**: 
- Form submits but data doesn't appear
- No error message shown

**Causes**:
- Database connection dropped
- Form validation failed silently
- Transaction rolled back

**Solutions**:

```bash
# Step 1: Check form fields
# All required fields must be filled
# Check for red error indicators

# Step 2: Verify database connection
python scripts/database/test_connection.py

# Step 3: Check browser console for errors
# Press F12 → Console tab
# Look for red error messages

# Step 4: Refresh page and try again
# Ctrl/Cmd + Shift + R (hard refresh)

# Step 5: Try simpler data
# Use minimal fields first
# Gradually add more

# Step 6: Verify database has space
# Check disk space not full
# Run: df -h (Linux/Mac) or disk manager (Windows)
```

---

### Issue 12: Duplicate Data in Database

**Symptoms**: Same record appears multiple times

**Cause**: Network issue caused double submission

**Solutions**:

```bash
# Step 1: Identify duplicates
USE canteen;
SELECT date_of_sale, item_name, COUNT(*) 
FROM sales 
GROUP BY date_of_sale, item_name 
HAVING COUNT(*) > 1;

# Step 2: Delete duplicates (keep first)
DELETE s1 FROM sales s1
INNER JOIN sales s2 
WHERE s1.sale_id > s2.sale_id 
AND s1.date_of_sale = s2.date_of_sale 
AND s1.item_name = s2.item_name;

# Step 3: Verify deletion
SELECT COUNT(*) FROM sales;
```

---

### Issue 13: Wrong Data Displayed

**Symptoms**: Numbers don't match reality

**Causes**:
- Data entry errors
- Filter applied
- Cached data shown

**Solutions**:

```bash
# Step 1: Refresh page
# Ctrl/Cmd + Shift + R (hard refresh)

# Step 2: Check filters
# Reset any active filters
# Click "Clear All Filters"

# Step 3: Clear cache
# Settings → Privacy → Clear browsing data
# Select "Cached images and files"

# Step 4: Verify in database directly
USE canteen;
SELECT * FROM sales WHERE date_of_sale = '2024-01-15';

# Step 5: Correct incorrect data
UPDATE sales SET quantity_sold = 10 WHERE sale_id = 1;
```

---

## File Upload Issues

### Issue 14: "File Format Not Supported"

**Error Message**: 
```
Upload failed: File format not supported
```

**Cause**: Wrong file format or encoding

**Solutions**:

```bash
# Step 1: Ensure file is CSV or Excel
# Accepted formats: .csv, .xlsx, .xls

# Step 2: Save CSV with correct encoding
# Use UTF-8 encoding (not ANSI)
# Excel: Save As → CSV UTF-8 (.csv)

# Step 3: Check column headers
# Must match expected format
# See USER_GUIDE.md for correct format

# Step 4: Validate file
# Open in text editor
# Check for special characters
# Remove if present

# Step 5: Try smaller file
# Test with 5 rows first
# If works, try larger file
```

---

### Issue 15: "File Too Large"

**Error Message**:
```
File size exceeds limit
```

**Cause**: File larger than maximum allowed

**Solutions**:

```bash
# Step 1: Check file size
# Windows: Right-click → Properties
# Mac: Right-click → Get Info
# Linux: ls -lh filename

# Step 2: Split large file
# Break into smaller parts
# Upload separately

# Step 3: Remove unnecessary columns
# Keep only required data
# Delete extra columns in Excel

# Step 4: Reduce rows
# Upload in batches
# E.g., 1000 rows per upload
```

---

### Issue 16: "Data Not Imported Correctly"

**Symptoms**: 
- Some rows imported, others skipped
- Incorrect column mapping
- Data validation errors

**Solutions**:

```bash
# Step 1: Check preview before import
# Review data shown in preview
# Verify column mapping is correct

# Step 2: Validate data format
# Dates must be YYYY-MM-DD format
# Numbers must have no currency symbols
# Text fields shouldn't have quotes

# Step 3: Check for missing required fields
# Sales: date, item, quantity, price required
# Inventory: date, item, unit_cost required

# Step 4: Fix file and retry
# Correct formatting issues
# Save and upload again

# Step 5: Import manually
# If automated import fails
# Use form entry for critical records
```

---

## Performance Issues

### Issue 17: Application is Slow

**Symptoms**:
- Takes 5+ seconds to respond
- Buttons take long to click
- Charts take long to load

**Causes**:
- Large dataset
- Slow database query
- Low system resources

**Solutions**:

```bash
# Step 1: Restart application
streamlit run src/app.py

# Step 2: Clear cache
# Browser cache
# Application cache via button

# Step 3: Check system resources
# Windows: Task Manager
# Mac: Activity Monitor
# Linux: top
# Look for: CPU, Memory, Disk usage

# Step 4: Close other applications
# Free up RAM
# Close browser tabs
# Stop unnecessary services

# Step 5: Optimize database
# Run maintenance
mysql -u root -p
USE canteen;
OPTIMIZE TABLE users;
OPTIMIZE TABLE sales;
OPTIMIZE TABLE inventory;

# Step 6: Archive old data
# Move old records to backup
# Keeps main tables smaller
# Improves query speed
```

---

### Issue 18: Reports/Charts Not Loading

**Symptoms**:
- Report page shows loading spinner
- Chart appears blank
- "Error generating report" message

**Causes**:
- No data in database
- Query timeout
- Visualization error

**Solutions**:

```bash
# Step 1: Verify data exists
USE canteen;
SELECT COUNT(*) FROM sales;

# Should show > 0 if data exists

# Step 2: Refresh page
# Ctrl/Cmd + Shift + R

# Step 3: Try different date range
# Maybe no data in selected range

# Step 4: Clear chart cache
# Streamlit menu → Clear cache

# Step 5: Check browser console
# F12 → Console
# Look for JavaScript errors

# Step 6: Try downloading data
# If report doesn't load
# Try downloading first
# Then visualize in Excel
```

---

## Common Error Messages

### "Streamlit API Exception"

**Cause**: Application error in Python code

**Solutions**:
```bash
# Check application logs
# Restart application
# Report to developer if persistent
```

---

### "Connection Refused"

**Cause**: Cannot connect to server

**Solutions**:
```bash
# Verify server is running
# Check IP address and port
# Check firewall settings
# Restart application
```

---

### "Permission Denied"

**Cause**: Insufficient user permissions

**Solutions**:
```bash
# Contact administrator
# Request elevated permissions
# Or use admin account
```

---

### "Timeout"

**Cause**: Request took too long

**Solutions**:
```bash
# Check internet connection
# Restart application
# Try again with smaller dataset
```

---

## Backup & Recovery

### Issue 19: Lost Database Data

**Recovery Steps**:

```bash
# Step 1: Check if backup exists
ls -la backup_*.sql

# Step 2: Restore from backup
mysql -u root -p canteen < backup_20240115.sql

# Step 3: Verify data restored
mysql -u root -p
USE canteen;
SELECT COUNT(*) FROM sales;

# Step 4: Check integrity
# Run validation queries
# Compare with paper records
```

---

### Issue 20: Database Corruption

**Symptoms**:
- Random errors
- Missing data
- Incorrect calculations

**Solutions**:

```bash
# Step 1: Check table integrity
mysql -u root -p
USE canteen;
CHECK TABLE users;
CHECK TABLE sales;
CHECK TABLE inventory;

# If errors found:

# Step 2: Repair table
REPAIR TABLE sales;
REPAIR TABLE inventory;

# Step 3: Optimize table
OPTIMIZE TABLE sales;
OPTIMIZE TABLE inventory;

# Step 4: If still issues
# Restore from backup
# See Issue 19 above
```

---

## Getting Help

### Before Asking for Help

1. **Document the issue**:
   - Error message (exact text)
   - When does it happen?
   - Steps to reproduce
   - What were you trying to do?

2. **Try basic troubleshooting**:
   - Restart application
   - Clear cache
   - Refresh page
   - Restart computer

3. **Check relevant logs**:
   - Application logs
   - Browser console (F12)
   - MySQL logs

### Asking for Help

**Provide**:
- Error message
- Steps to reproduce
- Browser used
- Operating system
- When it started happening

**Contact**:
- Administrator
- Developer
- Support team

---

## Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| Won't load | Restart app, check port 8501 |
| Can't login | Check credentials, test DB connection |
| Data won't save | Verify DB connection, check form |
| Slow | Restart app, clear cache, check resources |
| Charts blank | Check data exists, refresh page |
| File upload fails | Check file format, check size |
| Wrong data | Clear cache, check filters, verify DB |

---

## Database Credentials Quick Reference

**Database**: `canteen`  
**Username**: `root`  
**Default Admin User**: `admin` / `admin123`

**Secrets File** (`.streamlit/secrets.toml`):
```toml
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password"
DB_NAME = "canteen"
```

---

## Useful Scripts

**Test Connection**:
```bash
python scripts/database/test_connection.py
```

**Check Database Schema**:
```bash
python scripts/database/check_database_schema.py
```

**Create Admin User**:
```bash
python scripts/maintenance/quick_fix.py
```

---

## For More Help

- [README.md](../README.md) - Project overview
- [QUICK_START.md](../QUICK_START.md) - Setup guide
- [USER_GUIDE.md](USER_GUIDE.md) - How to use app
- [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) - Database info
- [SCRIPTS.md](SCRIPTS.md) - Available utilities

---

**Version**: 1.0  
**Last Updated**: July 2026  
**Database**: MySQL - canteen  
**Status**: ✅ Production Ready
