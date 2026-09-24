# User Guide

Guide to using the Canteen Sales and Inventory Management System.

---

## Getting Started

Start the application with:

```bash
streamlit run src/app.py
```

Open the application at:

```text
http://localhost:8501
```

The application uses MySQL to store sales, inventory, and user data.

---

## Login

Use the login page to access the application.

### Default Development Account

```text
Username: admin
Password: admin123
```

> These credentials are provided for the academic/development version of the project and should not be used for a real deployment.

---

## Dashboard

The dashboard provides an overview of the canteen data.

It includes:

* Sales and revenue KPIs
* Inventory information
* Low-stock alerts
* Access to the main application sections

Use the sidebar to navigate through the application.

---

## Sales

The Sales section is used to record and manage sales transactions.

### Add a Sale

1. Open **Sales** from the sidebar.
2. Enter the required transaction details.
3. Enter the item, quantity, and price.
4. Enter the remaining required information.
5. Submit the form.

The transaction is stored in the MySQL database.

### View Sales

The sales section displays recorded transactions and related information such as:

* Date
* Item
* Category
* Quantity
* Unit price
* Total amount
* Payment mode
* Customer type

---

## Inventory

The Inventory section is used to manage and monitor stock information.

### Add Inventory

1. Open **Inventory** from the sidebar.
2. Enter the item details.
3. Enter stock information.
4. Enter the unit cost and supplier details where required.
5. Submit the form.

### Monitor Stock

The inventory section displays current stock information and highlights items that require attention based on stock levels.

---

## Reports & Analytics

The analytics sections provide an overview of sales and inventory performance.

They can be used to examine:

* Sales and revenue performance
* Sales trends
* Product-level performance
* Category-level performance
* Inventory levels
* Low-stock items

Charts and KPI cards provide a visual summary of the available data.

---

## Data Upload

The application supports uploading sales and inventory data from supported file formats.

### Upload Process

1. Open the relevant upload section.
2. Select the data file.
3. Preview the uploaded data.
4. Check the columns and values.
5. Submit the upload.
6. Verify the imported records.

Make sure the uploaded file follows the format expected by the application.

---

## Searching, Filtering and Deleting Records

The application provides controls for working with stored records.

Use the available search and filter options to locate specific records.

Records can also be deleted from the relevant management sections when required.

> Verify a record before deleting it because deleted records may not be recoverable.

---

## Troubleshooting

For common application and database issues, see:

**[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

For database utility scripts, see:

**[SCRIPTS.md](SCRIPTS.md)**

---

**Project:** Canteen Sales & Inventory Management System
**Technology:** Python, MySQL, Streamlit, Pandas, Matplotlib
**Type:** Academic Project
