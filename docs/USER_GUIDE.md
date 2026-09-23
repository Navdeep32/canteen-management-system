# User Guide

Guide to using the Canteen Sales & Inventory Management System.

---

## Getting Started

Start the application with:

```bash
streamlit run src/app.py
```

Once the application starts, open:

```text
http://localhost:8501
```

The application uses MySQL for storing sales, inventory, and user data.

---

## Login

Enter your username and password on the login page.

### Default Development Account

```text
Username: admin
Password: admin123
```

> These credentials are provided for the academic/development version of the project.

After successful login, the application opens the main dashboard.

---

## Dashboard

The dashboard provides an overview of the canteen's current data.

Depending on the available data, it provides information such as:

* Sales-related KPIs
* Inventory information
* Low-stock items
* Quick access to application modules

Use the sidebar to navigate between the different sections.

---

## Sales Management

The Sales section is used to record and manage sales transactions.

### Add a Sale

1. Open **Sales** from the sidebar.
2. Enter the required sales information.
3. Provide the item name, quantity, and price.
4. Enter any other available transaction details.
5. Submit the form.
6. The record is stored in the MySQL database.

The total transaction amount is calculated from the quantity and unit price where applicable.

### View Sales

The sales section can be used to view previously recorded transactions.

Typical information includes:

* Sale ID
* Date
* Item
* Category
* Quantity
* Unit price
* Total amount
* Payment mode
* Customer type

---

## Inventory Management

The Inventory section is used to record and monitor stock information.

### Add Inventory

1. Open **Inventory** from the sidebar.
2. Enter the item details.
3. Enter stock received or used.
4. Enter the unit cost.
5. Provide supplier information where applicable.
6. Submit the form.

The application stores the inventory information in the MySQL database.

### Monitor Stock

The inventory section provides information about available stock and helps identify items that may require replenishment.

---

## Reports & Analytics

The Reports section provides an analytical view of the data stored in the system.

Depending on the available data, reports can be used to examine:

* Sales performance
* Sales trends
* Item-level performance
* Category-level performance
* Inventory information

Charts and summary metrics help provide a quick view of business performance.

---

## Data Upload

The application supports uploading structured sales or inventory data where the corresponding upload functionality is available.

### General Process

1. Open the relevant upload section.
2. Select the data file.
3. Review the uploaded data.
4. Verify that the columns and values are correct.
5. Submit the upload.
6. Verify the imported records.

Before uploading, ensure that the file follows the format expected by the application.

---

## Common Data Operations

### Searching and Filtering

Where available, use the search and filter controls to narrow down records.

Common filtering criteria may include:

* Date
* Item
* Category
* Supplier
* Payment mode

### Editing Records

If editing is available for a particular record:

1. Select the record.
2. Choose the edit option.
3. Update the required information.
4. Save the changes.

### Deleting Records

If deletion is available:

1. Select the record.
2. Choose the delete option.
3. Confirm the action.

> Deleted records may not be recoverable, so verify the record before deleting it.

---

## Data Entry Guidelines

For more reliable reports and analysis:

* Use consistent item names.
* Enter accurate quantities and prices.
* Check dates before submitting.
* Complete all required fields.
* Review the entered information before saving.
* Avoid entering the same transaction more than once.

---

## Troubleshooting

For common setup and application issues, see:

**[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

For database and utility-script information, see:

**[SCRIPTS.md](SCRIPTS.md)**

---

## Related Documentation

* [README.md](../README.md) — Project overview
* [QUICK_START.md](../QUICK_START.md) — Setup instructions
* [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Common issues
* [SCRIPTS.md](SCRIPTS.md) — Utility scripts

---

**Project:** Canteen Sales & Inventory Management System
**Technology:** Python, MySQL, Streamlit, Pandas, Matplotlib
**Type:** Academic Project
