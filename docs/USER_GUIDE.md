# User Guide - Canteen Management System

Complete guide for using the Canteen Management System application.

---

## Getting Started

### Accessing the Application

1. Open your web browser
2. Navigate to: `http://localhost:8501`
3. You should see the login page

### System Requirements

- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (or local network access)
- Stable display with 1024x768+ resolution

---

## Login

### First-Time Login

**Default Credentials** (change immediately after first login):
- **Username**: admin
- **Password**: admin123

### Login Steps

1. Enter username in the username field
2. Enter password in the password field
3. Click **"Login"** button
4. If credentials are correct, you'll see the dashboard

### Changing Your Password

⚠️ **Important**: Change default password immediately!

1. Look for **"Settings"** or **"Account"** option
2. Select **"Change Password"**
3. Enter current password
4. Enter new password (strong password recommended)
5. Confirm new password
6. Click **"Save"**

### Forgot Password?

Contact your administrator for password reset.

---

## Dashboard

The dashboard is your main view after login. It shows key metrics and quick actions.

### Dashboard Components

```
┌──────────────────────────────────────────┐
│     CANTEEN MANAGEMENT SYSTEM            │
├──────────────────────────────────────────┤
│                                          │
│  ┌────────────┐ ┌────────────┐          │
│  │ Today's    │ │ Low Stock  │          │
│  │ Sales: Rs. │ │ Items: 5   │          │
│  │ 2,450      │ │            │          │
│  └────────────┘ └────────────┘          │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │      Sales Trend (Last 7 Days)     │ │
│  │      [Graph visualization]         │ │
│  │                                    │ │
│  └────────────────────────────────────┘ │
│                                          │
│  ┌─────────────────────────────────────┤│
│  │ Quick Actions                       ││
│  │ □ Add Sales Entry                  ││
│  │ □ Add Inventory Entry              ││
│  │ □ View Reports                     ││
│  └─────────────────────────────────────┤│
└──────────────────────────────────────────┘

Sidebar Navigation:
📊 Dashboard
💰 Sales
📦 Inventory
📈 Reports
⚙️ Settings
```

### Dashboard Metrics

**Today's Sales**
- Total amount collected today
- Number of transactions
- Best selling item

**Low Stock Items**
- Items with stock < 20 units
- Shows item name and quantity
- Click to reorder

**Inventory Value**
- Total value of items in stock
- Calculated from: Quantity × Unit Cost

---

## Sales Management

### Adding Sales Entry

#### Access Sales
1. Click **"Sales"** in sidebar
2. Click **"Add New Entry"** button

#### Sales Form Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Date | Date Picker | ✅ | Date of sale |
| Item Name | Text | ✅ | What was sold? |
| Category | Dropdown | ⚠️ | Category (Snacks, Beverages, etc.) |
| Quantity | Number | ✅ | How many units sold |
| Unit Price | Decimal | ✅ | Price per unit |
| Total Amount | Auto | Auto | System calculates: Qty × Price |
| Payment Mode | Dropdown | ⚠️ | Cash, Card, UPI, etc. |
| Customer Type | Dropdown | ⚠️ | Student, Staff, Guest, etc. |

#### Step-by-Step: Adding Sales

**Example: Selling 10 Samosas at Rs. 5 each**

1. **Date**: Select today's date
   - Click date field → Select date
   - Default is today

2. **Item Name**: Enter "Samosa"
   - Be consistent with name
   - Affects reporting

3. **Category**: Select "Snacks"
   - Use dropdown menu
   - Helps organize sales

4. **Quantity**: Enter "10"
   - Number of items sold
   - Must be > 0

5. **Unit Price**: Enter "5.00"
   - Price per item
   - Must be > 0

6. **Total Amount**: System auto-calculates
   - Shows: 10 × 5.00 = 50.00
   - You cannot edit this

7. **Payment Mode**: Select "Cash"
   - Options: Cash, Card, UPI, Cheque
   - Helps track payment methods

8. **Customer Type**: Select "Student"
   - Options: Student, Staff, Guest, Visitor
   - For customer analysis

9. **Review**: Check all information
   - Verify date is correct
   - Verify quantities and prices

10. **Submit**: Click **"Add Entry"**
    - System saves to database
    - Shows confirmation message

### Viewing Sales History

1. Go to **"Sales"** → **"View All Sales"**
2. Shows all sales with:
   - Date
   - Item name
   - Quantity
   - Price
   - Total
   - Payment mode
   - Customer type

3. **Sort** by clicking column headers (Date, Item, Total, etc.)
4. **Filter** by:
   - Date range (Select from → Select to)
   - Item name
   - Category
   - Payment mode

5. **Search** for specific items
6. **Download** data as CSV/Excel

### Editing Sales Entry

1. Click **"Edit"** button on sale record
2. Modify fields as needed
3. Click **"Update"** to save changes

### Deleting Sales Entry

⚠️ **Warning**: Deletion is permanent!

1. Click **"Delete"** button on sale record
2. Confirm deletion in popup
3. Record is permanently removed

---

## Inventory Management

### Adding Inventory Entry

#### Access Inventory
1. Click **"Inventory"** in sidebar
2. Click **"Add New Entry"** button

#### Inventory Form Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| Date | Date Picker | ✅ | Date of transaction |
| Item Name | Text | ✅ | Name of item |
| Stock In | Number | ⚠️ | Units received |
| Stock Used | Number | ⚠️ | Units used/consumed |
| Unit Cost | Decimal | ✅ | Cost per unit |
| Supplier Name | Text | ⚠️ | Who supplied it? |

#### Step-by-Step: Adding Inventory

**Example: Receiving 100 Samosas**

1. **Date**: Select today's date

2. **Item Name**: Enter "Samosa"

3. **Stock In**: Enter "100"
   - This means you received 100 units

4. **Stock Used**: Enter "0"
   - Or if you used some: enter "10"
   - Remaining = 100 - 10 = 90

5. **Unit Cost**: Enter "3.50"
   - Cost per unit from supplier

6. **Supplier Name**: Enter "Local Baker"

7. **Review**: Check information
   - System calculates: Remaining = Stock In - Stock Used

8. **Submit**: Click **"Add Entry"**

### Current Stock View

1. Go to **"Inventory"** → **"Current Stock"**
2. Shows all items with:
   - Item name
   - Current quantity
   - Unit cost
   - Total value
   - Supplier name

3. **Sort** by clicking column headers
4. **Filter** by item name or supplier

### Low Stock Alerts

The system automatically alerts when stock falls below 20 units.

**Alert indicates**:
- Item name
- Current quantity
- Supplier contact
- Action: Order more stock

---

## Reports & Analytics

### Dashboard Reports

Access via **"Reports"** menu

#### Sales Reports

**Daily Sales Report**
- Select date range
- Shows: Total sales, number of transactions, average transaction

**Top Selling Items**
- Shows 10 best-selling items
- Quantity sold and revenue
- Includes pie chart visualization

**Sales by Category**
- Revenue breakdown by category
- Bar chart comparison
- Percentage of total sales

**Monthly Sales Report**
- Sales for each month
- Trend analysis
- Year-over-year comparison

#### Inventory Reports

**Current Stock Level**
- All items and quantities
- Unit cost and total value
- Supplier information

**Stock Movement**
- Items added and used
- Date-wise tracking
- Supplier analysis

**Low Stock Items**
- Items below 20 units
- Urgent reorder list
- Supplier details

### Analytics & Charts

**Sales Trend Graph**
- Line chart showing sales over time
- Last 7 days, 30 days, or custom range
- Identify peak sales periods

**Category Performance**
- Pie chart of sales by category
- Percentage breakdown
- Top performing categories

**Item Performance**
- Bar chart of top items
- Sales volume and revenue
- Helps with inventory planning

---

## Data Upload

### Bulk Import Sales Data

#### Access Upload
1. Click **"Upload Data"** in menu
2. Select **"Sales Data Upload"**

#### File Format

**File Type**: CSV or Excel (.xlsx, .xls)

**Required Columns**:
| Column | Format | Example |
|--------|--------|---------|
| date_of_sale | YYYY-MM-DD | 2024-01-15 |
| item_name | Text | Samosa |
| category | Text | Snacks |
| quantity_sold | Number | 10 |
| unit_price | Decimal | 5.00 |
| payment_mode | Text | Cash |
| customer_type | Text | Student |

**Example CSV**:
```
date_of_sale,item_name,category,quantity_sold,unit_price,payment_mode,customer_type
2024-01-15,Samosa,Snacks,10,5.00,Cash,Student
2024-01-15,Tea,Beverages,25,10.00,Card,Staff
2024-01-16,Coffee,Beverages,15,15.00,UPI,Guest
```

#### Upload Steps

1. Click **"Choose File"**
2. Select your CSV/Excel file
3. Click **"Preview"** to verify data
4. Check column mapping is correct
5. Click **"Upload"**
6. System shows success/error message

### Bulk Import Inventory Data

#### File Format

**Required Columns**:
| Column | Format | Example |
|--------|--------|---------|
| date_of_entry | YYYY-MM-DD | 2024-01-15 |
| item_name | Text | Samosa |
| stock_in | Number | 50 |
| stock_used | Number | 10 |
| unit_cost | Decimal | 3.50 |
| supplier_name | Text | Local Baker |

#### Upload Steps

Same as sales upload process.

---

## Search & Filter

### Search Functionality

1. Use **Search** box on any list page
2. Type item name or partial text
3. Results filter in real-time
4. Shows matching records

### Filter Options

**By Date Range**:
- Select "From Date"
- Select "To Date"
- Results show only that range

**By Category**:
- Select from dropdown
- Shows only that category

**By Supplier**:
- Select from dropdown
- Shows items from that supplier

**By Payment Mode**:
- Select: Cash, Card, UPI, Cheque
- Shows matching transactions

### Sort & Arrange

1. Click column headers to sort
2. Click again to reverse order
3. Arrow (↑↓) shows sort direction

---

## Data Management

### Export Data

1. Go to **"Data Management"** → **"Export"**
2. Select table: Sales, Inventory, or Users
3. Select date range (optional)
4. Click **"Download"** 
5. File downloads as CSV/Excel

### Delete Records

⚠️ **Warning**: Deletion is permanent! No undo!

1. Click **"Delete"** button on record
2. Confirm in popup
3. Record is removed permanently

### Backup Data

Contact administrator to backup database.

---

## Settings & Administration

### Profile Settings

1. Click **"Settings"** in sidebar
2. View your profile information
3. Update email (if available)
4. Update phone number (if available)

### Change Password

1. Go to **Settings**
2. Click **"Change Password"**
3. Enter current password
4. Enter new password (min 8 characters)
5. Confirm new password
6. Click **"Save"**

**Password Requirements**:
- Minimum 8 characters
- Mix of letters and numbers recommended
- Avoid common words
- Don't reuse old passwords

### System Settings (Admin Only)

**Low Stock Threshold**:
- Default: 20 units
- Adjust when alert triggers

**Report Preferences**:
- Date format
- Currency format
- Number of decimal places

---

## Tips & Tricks

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Tab | Move to next field |
| Enter | Submit form |
| Esc | Close popup |
| Ctrl+P | Print current page |

### Quick Entry Tips

1. **Copy Previous Entry**:
   - Speeds up data entry
   - Avoids re-typing

2. **Use Tab Key**:
   - Move between fields
   - Faster than clicking

3. **Set Today as Default**:
   - Date field defaults to today
   - No need to change if adding today's data

4. **Use Dropdowns**:
   - Click dropdown arrow
   - Start typing to filter
   - Select from suggestions

5. **Review Before Submit**:
   - Double-check all data
   - Verify calculations
   - Check dates carefully

### Performance Tips

1. **Close old tabs** - Frees up memory
2. **Clear browser cache** - If page slow
3. **Use recent data** - Archive old records
4. **Sort by date** - Newest first usually faster
5. **Limit date ranges** - Fewer records = faster

---

## Troubleshooting

### Common Issues

**Page won't load**:
- Refresh browser (Ctrl+Shift+R)
- Check internet connection
- Try different browser

**Data won't save**:
- Check all required fields filled
- Verify database connection
- Try again
- Contact administrator

**Slow performance**:
- Clear browser cache
- Close other tabs
- Restart application
- Check internet connection

**Can't download file**:
- Check browser pop-up settings
- Disable ad blockers
- Try different browser
- Contact administrator

### Getting Help

1. **For Technical Issues**:
   - Contact IT administrator
   - Provide error message details
   - Describe what you were doing

2. **For Password Reset**:
   - Contact administrator
   - Provide username
   - Verify identity

3. **For New Features**:
   - Submit feature request to administrator
   - Explain the need
   - Suggest implementation

4. **For Bugs**:
   - Document the issue
   - Provide steps to reproduce
   - Contact administrator

---

## Best Practices

✅ **DO**:
- ✅ Update data regularly (daily)
- ✅ Review reports weekly
- ✅ Check low stock alerts
- ✅ Keep inventory accurate
- ✅ Use strong passwords
- ✅ Log out when done
- ✅ Verify data before submitting
- ✅ Use consistent item names

❌ **DON'T**:
- ❌ Share login credentials
- ❌ Leave system logged in unattended
- ❌ Enter future dates
- ❌ Use negative quantities
- ❌ Skip required fields
- ❌ Force browser close (log out properly)
- ❌ Enter same data twice
- ❌ Change data after submitting

---

## Keyboard & Mouse Tips

### Mouse Tips

1. **Hover over fields** - See help text
2. **Click column headers** - Sort data
3. **Drag to resize** - Adjust column width
4. **Right-click** - Context menu options

### Keyboard Tips

1. **Tab** - Move between fields (faster)
2. **Shift+Tab** - Move backward
3. **Enter** - Submit form
4. **Esc** - Cancel/close
5. **Ctrl+A** - Select all text
6. **Ctrl+C** - Copy
7. **Ctrl+V** - Paste

---

## Accessing Help

- **On-screen Help**: Hover over (?) icons for tooltips
- **This User Guide**: Available in Help menu
- **Contact Admin**: For questions not covered here
- **FAQ**: Check TROUBLESHOOTING.md guide

---

## Quick Links

- [README.md](../README.md) - Project overview
- [QUICK_START.md](../QUICK_START.md) - Setup guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
- [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) - Database structure
- [SCRIPTS.md](SCRIPTS.md) - Utility scripts

---

**Version**: 1.0  
**Last Updated**: July 2026  
**Application**: Canteen Management System  
**Status**: ✅ Production Ready

For technical details, see [ARCHITECTURE.md](ARCHITECTURE.md)
