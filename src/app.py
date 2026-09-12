import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date
import mysql.connector
from mysql.connector import Error
import io
import hashlib

# Page Configuration
st.set_page_config(
    page_title="Canteen Management System",
    page_icon="🍽️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem !important;
        font-weight: bold !important;
        color: #1f77b4 !important;
        text-align: center !important;
        padding: 20px !important;
        margin-bottom: 10px !important;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #145a8a;
    }
    .success-box {
        padding: 15px;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        padding: 15px;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ===========================
# DATABASE CONNECTION
# ===========================

@st.cache_resource
def init_connection():
    """Initialize MySQL database connection"""
    try:
        connection = mysql.connector.connect(
            host=st.secrets.get("DB_HOST", "localhost"),
            user=st.secrets.get("DB_USER", "root"),
            password=st.secrets.get("DB_PASSWORD", ""),
            database=st.secrets.get("DB_NAME", "canteen")
        )
        return connection
    except Error as e:
        st.error(f"❌ Database Connection Error: {e}")
        return None

def create_tables(connection):
    """Create necessary tables if they don't exist"""
    try:
        cursor = connection.cursor()
        
        # Sales Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
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
        """)
        
        # Inventory Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
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
        """)
        
        # Users Table (for authentication)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        connection.commit()
        cursor.close()
        return True
    except Error as e:
        st.error(f"❌ Error creating tables: {e}")
        return False

# ===========================
# AUTHENTICATION FUNCTIONS
# ===========================

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(connection, username, password):
    """Verify user credentials"""
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password_hash = %s",
            (username, hash_password(password))
        )
        user = cursor.fetchone()
        cursor.close()
        return user
    except Error as e:
        st.error(f"❌ Authentication error: {e}")
        return None

def create_default_user(connection):
    """Create default admin user if no users exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                ("admin", hash_password("admin123"), "admin")
            )
            connection.commit()
            st.info("ℹ️ Default user created - Username: admin, Password: admin123")
        cursor.close()
    except Error as e:
        st.error(f"❌ Error creating default user: {e}")

# ===========================
# DATABASE OPERATIONS
# ===========================

def insert_sale(connection, data):
    """Insert new sale record"""
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO sales (date_of_sale, item_name, category, quantity_sold, 
                             unit_price, total_amount, payment_mode, customer_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
        return True
    except Error as e:
        st.error(f"❌ Error inserting sale: {e}")
        return False

def insert_inventory(connection, data):
    """Insert new inventory record"""
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO inventory (date_of_entry, item_name, stock_in, stock_used, 
                                 remaining_stock, unit_cost, supplier_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
        return True
    except Error as e:
        st.error(f"❌ Error inserting inventory: {e}")
        return False

def get_sales_data(connection, start_date=None, end_date=None):
    """Fetch sales data from database"""
    try:
        query = "SELECT * FROM sales"
        params = []
        
        if start_date and end_date:
            query += " WHERE date_of_sale BETWEEN %s AND %s"
            params = [start_date, end_date]
        
        query += " ORDER BY date_of_sale DESC"
        
        df = pd.read_sql(query, connection, params=params if params else None)
        
        if not df.empty:
            df['date_of_sale'] = pd.to_datetime(df['date_of_sale'])
            df['month_name'] = df['date_of_sale'].dt.strftime('%B')
            df['weekday'] = df['date_of_sale'].dt.strftime('%A')
        
        return df
    except Error as e:
        st.error(f"❌ Error fetching sales data: {e}")
        return pd.DataFrame()

def get_inventory_data(connection):
    """Fetch inventory data from database"""
    try:
        query = "SELECT * FROM inventory ORDER BY date_of_entry DESC"
        df = pd.read_sql(query, connection)
        
        if not df.empty:
            df['date_of_entry'] = pd.to_datetime(df['date_of_entry'])
            df['month_name'] = df['date_of_entry'].dt.strftime('%B')
        
        return df
    except Error as e:
        st.error(f"❌ Error fetching inventory data: {e}")
        return pd.DataFrame()

def bulk_insert_sales(connection, df):
    """Bulk insert sales data from uploaded file"""
    try:
        cursor = connection.cursor()
        
        for _, row in df.iterrows():
            query = """
                INSERT INTO sales (date_of_sale, item_name, category, quantity_sold, 
                                 unit_price, total_amount, payment_mode, customer_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = (
                row.get('date_of_sale', datetime.now().date()),
                row['item_name'],
                row.get('category', 'Other'),
                row.get('quantity_sold', 1),
                row.get('unit_price', 0),
                row.get('total_amount', 0),
                row.get('payment_mode', 'Cash'),
                row.get('customer_type', 'General')
            )
            cursor.execute(query, data)
        
        connection.commit()
        cursor.close()
        return True
    except Error as e:
        st.error(f"❌ Error in bulk insert: {e}")
        return False

def bulk_insert_inventory(connection, df):
    """Bulk insert inventory data from uploaded file"""
    try:
        cursor = connection.cursor()
        
        for _, row in df.iterrows():
            query = """
                INSERT INTO inventory (date_of_entry, item_name, stock_in, stock_used, 
                                     remaining_stock, unit_cost, supplier_name)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            data = (
                row.get('date_of_entry', datetime.now().date()),
                row['item_name'],
                row.get('stock_in', 0),
                row.get('stock_used', 0),
                row.get('remaining_stock', 0),
                row.get('unit_cost', 0),
                row.get('supplier_name', 'Unknown')
            )
            cursor.execute(query, data)
        
        connection.commit()
        cursor.close()
        return True
    except Error as e:
        st.error(f"❌ Error in bulk insert: {e}")
        return False

def delete_sale(connection, sale_id):
    """Delete a sale record"""
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM sales WHERE sale_id = %s", (sale_id,))
        connection.commit()
        cursor.close()
        return True
    except Error as e:
        st.error(f"❌ Error deleting sale: {e}")
        return False

def delete_inventory(connection, inventory_id):
    """Delete an inventory record"""
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM inventory WHERE inventory_id = %s", (inventory_id,))
        connection.commit()
        cursor.close()
        return True
    except Error as e:
        st.error(f"❌ Error deleting inventory: {e}")
        return False

# ===========================
# UTILITY FUNCTIONS
# ===========================

def load_file(uploaded_file):
    """Load CSV or Excel file"""
    try:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)
        else:
            st.error(f"❌ Unsupported file format: {file_extension}")
            return None
        
        return df
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
        return None

# ===========================
# AUTHENTICATION UI
# ===========================

def login_page():
    """Display login page"""
    st.markdown('<p class="main-header">🍽️ Canteen Management System</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if username and password:
                    conn = st.session_state.get('connection')
                    if conn and conn.is_connected():
                        user = verify_user(conn, username, password)
                        if user:
                            st.session_state['logged_in'] = True
                            st.session_state['user'] = user
                            st.success("✅ Login successful!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid username or password")
                else:
                    st.warning("⚠️ Please enter both username and password")
        

# ===========================
# MAIN APPLICATION
# ===========================

def main_app():
    """Main application after login"""
    
    st.markdown('<p class="main-header">🍽️ Canteen Management System</p>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title(f"👤 {st.session_state['user']['username']}")
    st.sidebar.markdown(f"**Role:** {st.session_state['user']['role']}")
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Main navigation
    page = st.sidebar.radio(
        "📌 Navigation",
        ["Dashboard", "Add New Entry", "Upload Data", "Sales Analysis", "Inventory Analysis", "Reports", "Data Management"]
    )
    
    conn = st.session_state.get('connection')
    
    if page == "Dashboard":
        show_dashboard(conn)
    elif page == "Add New Entry":
        show_entry_forms(conn)
    elif page == "Upload Data":
        show_upload_page(conn)
    elif page == "Sales Analysis":
        show_sales_analysis(conn)
    elif page == "Inventory Analysis":
        show_inventory_analysis(conn)
    elif page == "Reports":
        show_reports(conn)
    elif page == "Data Management":
        show_data_management(conn)

# ===========================
# PAGE FUNCTIONS
# ===========================

def show_dashboard(conn):
    """Display main dashboard"""
    st.header("📊 Dashboard Overview")
    
    sales_df = get_sales_data(conn)
    inventory_df = get_inventory_data(conn)
    
    if sales_df.empty and inventory_df.empty:
        st.info("ℹ️ No data available. Please add entries or upload data to get started.")
        return
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not sales_df.empty:
            total_sales = sales_df['total_amount'].sum()
            st.metric("💵 Total Sales", f"₹{total_sales:,.2f}")
        else:
            st.metric("💵 Total Sales", "₹0.00")
    
    with col2:
        if not sales_df.empty:
            total_items_sold = sales_df['quantity_sold'].sum()
            st.metric("🛒 Items Sold", f"{total_items_sold:,}")
        else:
            st.metric("🛒 Items Sold", "0")
    
    with col3:
        if not sales_df.empty:
            avg_order = sales_df['total_amount'].mean()
            st.metric("📊 Avg Order Value", f"₹{avg_order:.2f}")
        else:
            st.metric("📊 Avg Order Value", "₹0.00")
    
    with col4:
        if not inventory_df.empty:
            total_stock = inventory_df['remaining_stock'].sum()
            st.metric("📦 Total Stock", f"{total_stock:,} units")
        else:
            st.metric("📦 Total Stock", "0 units")
    
    st.markdown("---")
    
    # Charts
    if not sales_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏆 Top 10 Selling Items by Quantity")

            top_items = (
                sales_df
                .groupby('item_name')['quantity_sold']
                .sum()
                .sort_values(ascending=False)
                .head(10)
            )

            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.barh(top_items.index, top_items.values, color='#2ecc71')

            ax.set_xlabel('Quantity Sold (Units)', fontsize=14)
            ax.set_ylabel('Item Name', fontsize=14)

            # Highest value at top
            ax.invert_yaxis()

            # 👉 ADD VALUES ON BARS (IMPORTANT PART)
            for bar in bars:
                width = bar.get_width()
                ax.text(
                    width,                          # x position
                    bar.get_y() + bar.get_height()/2,  # y position (center of bar)
                    f'{int(width)}',                # value text
                    va='center',
                    ha='left',
                    fontsize=10
                )

            # Add a little extra space on x-axis so text is visible
            ax.set_xlim(0, max(top_items.values) * 1.15)

            plt.tight_layout()
            st.pyplot(fig)

        with col2:
            if 'payment_mode' in sales_df.columns:
                st.subheader("💳 Sales Distribution by Payment Mode")
                payment_counts = sales_df['payment_mode'].value_counts()
                
                fig, ax = plt.subplots(figsize=(10, 6))
                colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
                ax.pie(payment_counts.values, labels=payment_counts.index, 
                       autopct='%1.1f%%', colors=colors[:len(payment_counts)], startangle=90)
                ax.axis('equal')
                st.pyplot(fig)
    
    if not inventory_df.empty:
        st.markdown("---")
        st.subheader("⚠️ Low Stock Alert (< 20 units)")
        low_stock = inventory_df[inventory_df['remaining_stock'] < 20].sort_values('remaining_stock')
        
        if not low_stock.empty:
            st.warning(f"⚠️ {len(low_stock)} items need reordering!")
            st.dataframe(
                low_stock[['item_name', 'remaining_stock', 'supplier_name']],
                use_container_width=True
            )
        else:
            st.success("✅ All items are sufficiently stocked!")

def show_entry_forms(conn):
    """Display forms for adding new entries"""
    st.header("➕ Add New Entry")
    
    tab1, tab2 = st.tabs(["💰 New Sale", "📦 New Inventory"])
    
    with tab1:
        st.subheader("Add Sales Transaction")
        
        with st.form("sales_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                sale_date = st.date_input("Date of Sale", value=date.today())
                item_name = st.text_input("Item Name *", placeholder="e.g., Coffee")
                category = st.selectbox("Category", ["Beverage", "Snacks", "Meals", "Desserts", "Other"])
                quantity = st.number_input("Quantity Sold *", min_value=1, value=1)
            
            with col2:
                unit_price = st.number_input("Unit Price (₹) *", min_value=0.0, value=0.0, step=0.5)
                total_amount = quantity * unit_price
                st.text_input("Total Amount (₹)", value=f"{total_amount:.2f}", disabled=True)
                payment_mode = st.selectbox("Payment Mode", ["Cash", "UPI", "Card", "Other"])
                customer_type = st.selectbox("Customer Type", ["Student", "Staff", "Guest", "Other"])
            
            submitted = st.form_submit_button("💾 Save Sale")
            
            if submitted:
                if item_name and unit_price > 0:
                    data = (
                        sale_date,
                        item_name,
                        category,
                        quantity,
                        unit_price,
                        total_amount,
                        payment_mode,
                        customer_type
                    )
                    
                    if insert_sale(conn, data):
                        st.success("✅ Sale recorded successfully!")
                        st.balloons()
                    else:
                        st.error("❌ Failed to record sale")
                else:
                    st.warning("⚠️ Please fill all required fields (*)")
    
    with tab2:
        st.subheader("Add Inventory Entry")
        
        with st.form("inventory_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                entry_date = st.date_input("Date of Entry", value=date.today())
                item_name_inv = st.text_input("Item Name *", placeholder="e.g., Coffee Beans")
                stock_in = st.number_input("Stock In *", min_value=0, value=0)
                stock_used = st.number_input("Stock Used", min_value=0, value=0)
            
            with col2:
                remaining_stock = stock_in - stock_used
                st.text_input("Remaining Stock", value=f"{remaining_stock}", disabled=True)
                unit_cost = st.number_input("Unit Cost (₹)", min_value=0.0, value=0.0, step=0.5)
                supplier_name = st.text_input("Supplier Name", placeholder="e.g., FreshFoods")
            
            submitted_inv = st.form_submit_button("💾 Save Inventory")
            
            if submitted_inv:
                if item_name_inv and stock_in >= 0:
                    data = (
                        entry_date,
                        item_name_inv,
                        stock_in,
                        stock_used,
                        remaining_stock,
                        unit_cost,
                        supplier_name
                    )
                    
                    if insert_inventory(conn, data):
                        st.success("✅ Inventory entry added successfully!")
                        st.balloons()
                    else:
                        st.error("❌ Failed to add inventory entry")
                else:
                    st.warning("⚠️ Please fill all required fields (*)")

def show_upload_page(conn):
    """Display bulk upload page"""
    st.header("📤 Bulk Upload Data")
    
    st.info("💡 Upload CSV or Excel files to add multiple records at once")
    
    tab1, tab2 = st.tabs(["💰 Upload Sales", "📦 Upload Inventory"])
    
    with tab1:
        st.subheader("Upload Sales Data")
        
        sales_file = st.file_uploader(
            "Choose sales file (CSV or Excel)",
            type=['csv', 'xlsx', 'xls'],
            key='sales_upload'
        )
        
        if sales_file:
            df = load_file(sales_file)
            
            if df is not None:
                st.success(f"✅ File loaded: {len(df)} records")
                st.dataframe(df.head(10), use_container_width=True)
                
                if st.button("📥 Import Sales Data", key='import_sales'):
                    with st.spinner("Importing data..."):
                        # Clean date column
                        if 'date_of_sale' in df.columns:
                            df['date_of_sale'] = pd.to_datetime(df['date_of_sale'], errors='coerce')
                        
                        if bulk_insert_sales(conn, df):
                            st.success(f"✅ Successfully imported {len(df)} sales records!")
                            st.balloons()
                        else:
                            st.error("❌ Failed to import data")
    
    with tab2:
        st.subheader("Upload Inventory Data")
        
        inventory_file = st.file_uploader(
            "Choose inventory file (CSV or Excel)",
            type=['csv', 'xlsx', 'xls'],
            key='inventory_upload'
        )
        
        if inventory_file:
            df = load_file(inventory_file)
            
            if df is not None:
                st.success(f"✅ File loaded: {len(df)} records")
                st.dataframe(df.head(10), use_container_width=True)
                
                if st.button("📥 Import Inventory Data", key='import_inventory'):
                    with st.spinner("Importing data..."):
                        # Clean date column
                        if 'date_of_entry' in df.columns:
                            df['date_of_entry'] = pd.to_datetime(df['date_of_entry'], errors='coerce')
                        
                        if bulk_insert_inventory(conn, df):
                            st.success(f"✅ Successfully imported {len(df)} inventory records!")
                            st.balloons()
                        else:
                            st.error("❌ Failed to import data")

def show_sales_analysis(conn):
    """Display detailed sales analysis"""
    st.header("💰 Sales Analysis")
    
    # Date filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=date.today().replace(day=1))
    with col2:
        end_date = st.date_input("End Date", value=date.today())
    
    sales_df = get_sales_data(conn, start_date, end_date)
    
    if sales_df.empty:
        st.info("ℹ️ No sales data available for the selected period")
        return
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💵 Total Sales", f"₹{sales_df['total_amount'].sum():,.2f}")
    with col2:
        st.metric("📋 Total Transactions", len(sales_df))
    with col3:
        st.metric("📊 Average Transaction", f"₹{sales_df['total_amount'].mean():.2f}")
    
    st.markdown("---")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    filtered_df = sales_df.copy()
    
    with col1:
        if 'category' in sales_df.columns:
            categories = ['All'] + list(sales_df['category'].unique())
            selected_category = st.selectbox("Filter by Category", categories)
            if selected_category != 'All':
                filtered_df = filtered_df[filtered_df['category'] == selected_category]
    
    with col2:
        if 'payment_mode' in sales_df.columns:
            payments = ['All'] + list(sales_df['payment_mode'].unique())
            selected_payment = st.selectbox("Filter by Payment Mode", payments)
            if selected_payment != 'All':
                filtered_df = filtered_df[filtered_df['payment_mode'] == selected_payment]
    
    with col3:
        if 'customer_type' in sales_df.columns:
            customers = ['All'] + list(sales_df['customer_type'].unique())
            selected_customer = st.selectbox("Filter by Customer Type", customers)
            if selected_customer != 'All':
                filtered_df = filtered_df[filtered_df['customer_type'] == selected_customer]
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        if 'category' in filtered_df.columns:
            st.subheader("📊 Sales by Category")
            category_sales = filtered_df.groupby('category')['total_amount'].sum().sort_values(ascending=False)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(category_sales.index, category_sales.values, color='#9b59b6')
            ax.set_xlabel('Category', fontsize=11)
            ax.set_ylabel('Total Sales (₹)', fontsize=11)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
    
    with col2:
        st.subheader("🏆 Top 10 Items by Revenue")
        top_revenue = filtered_df.groupby('item_name')['total_amount'].sum().sort_values(ascending=False).head(10)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(top_revenue.index, top_revenue.values, color='#e74c3c')
        ax.set_xlabel('Total Revenue (₹)', fontsize=11)
        ax.set_ylabel('Item Name', fontsize=11)
        ax.invert_yaxis()
        plt.tight_layout()
        st.pyplot(fig)
    
    st.markdown("---")
    
    # Data table
    st.subheader("📋 Transaction Details")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

def show_inventory_analysis(conn):
    """Display inventory analysis"""
    st.header("📦 Inventory Analysis")
    
    inventory_df = get_inventory_data(conn)
    
    if inventory_df.empty:
        st.info("ℹ️ No inventory data available")
        return
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📥 Total Stock In", f"{inventory_df['stock_in'].sum():,} units")
    with col2:
        st.metric("📤 Total Stock Used", f"{inventory_df['stock_used'].sum():,} units")
    with col3:
        st.metric("📊 Avg Remaining Stock", f"{inventory_df['remaining_stock'].mean():.0f} units")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Stock Status by Item")
        stock_by_item = inventory_df.groupby('item_name')['remaining_stock'].sum().sort_values(ascending=True).head(15)
        
        # fig, ax = plt.subplots(figsize=(10, 6))
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = ['red' if x < 20 else 'orange' if x < 50 else 'green' for x in stock_by_item.values]

        #extra
        for i, v in enumerate(stock_by_item.values):
            ax.text(v + 50, i, f'{v:,}', va='center')

        #extra
        ax.grid(axis='x', linestyle='--', alpha=0.3)

        ax.barh(stock_by_item.index, stock_by_item.values, color=colors)
        ax.set_xlabel('Remaining Stock (units)', fontsize=11)
        ax.set_ylabel('Item Name', fontsize=11)
        ax.axvline(x=20, color='red', linestyle='--', linewidth=2, label='Low Stock (< 20)')
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)
    
    # with col2:
    #     if 'supplier_name' in inventory_df.columns:
    #         st.subheader("🏭 Supplier Distribution")
    #         supplier_stock = inventory_df.groupby('supplier_name')['stock_in'].sum().sort_values(ascending=False)
            
    #         fig, ax = plt.subplots(figsize=(10, 6))
    #         colors = plt.cm.Set3(range(len(supplier_stock)))
    #         ax.pie(supplier_stock.values, labels=supplier_stock.index, 
    #                autopct='%1.1f%%', colors=colors, startangle=90)
    #         ax.axis('equal')
    #         st.pyplot(fig)
    
    # updated above code here
    # with col2:
    #     if 'supplier_name' in inventory_df.columns:
    #         st.subheader("🏭 Supplier Distribution")

    #         supplier_stock = (
    #             inventory_df.groupby('supplier_name')['stock_in']
    #             .sum()
    #             .sort_values(ascending=False)
    #         )

    #         # ✅ Show only top 5 suppliers
    #         top_n = 5
    #         if len(supplier_stock) > top_n:
    #             top_suppliers = supplier_stock[:top_n]
    #             others_sum = supplier_stock[top_n:].sum()
    #             supplier_stock = top_suppliers.copy()
    #             supplier_stock["Others"] = others_sum

    #         fig, ax = plt.subplots(figsize=(8, 6))

    #         colors = plt.cm.Set3(range(len(supplier_stock)))

    #         # ✅ Donut chart (pie with hole)
    #         wedges, texts, autotexts = ax.pie(
    #             supplier_stock.values,
    #             autopct='%1.1f%%',
    #             startangle=90,
    #             colors=colors,
    #             wedgeprops=dict(width=0.4)   # 🔥 makes donut
    #         )

    #         # ✅ Legend outside (clean look)
    #         ax.legend(
    #             wedges,
    #             supplier_stock.index,
    #             title="Suppliers",
    #             loc="center left",
    #             bbox_to_anchor=(1, 0.5)
    #         )

    #         ax.axis('equal')
    #         plt.tight_layout()

    #         st.pyplot(fig)

    #again upated:
    with col2:
        if 'supplier_name' in inventory_df.columns:
            st.subheader("🏭 Supplier Distribution")

            supplier_stock = (
                inventory_df.groupby('supplier_name')['stock_in']
                .sum()
                .sort_values(ascending=False)
            )

            # ✅ Top 5 + Others
            top_n = 5
            if len(supplier_stock) > top_n:
                top_suppliers = supplier_stock[:top_n]
                others_sum = supplier_stock[top_n:].sum()
                supplier_stock = top_suppliers.copy()
                supplier_stock["Others"] = others_sum

            values = supplier_stock.values
            labels = supplier_stock.index

            fig, ax = plt.subplots(figsize=(8, 6))
            # fig, ax = plt.subplots(figsize=(6, 5))
            colors = plt.cm.Set3(range(len(values)))

            # ✅ Show % ONLY if > 5%
            def autopct_format(pct):
                return f'{pct:.1f}%' if pct > 5 else ''

            wedges, texts, autotexts = ax.pie(
                values,
                startangle=90,
                colors=colors,
                autopct=autopct_format,      # 🔥 hides small labels
                wedgeprops=dict(width=0.45)  # donut thickness
                # wedgeprops=dict(width=0.35),  # donut thickness

                #extra
                # radius=0.9
            )

            # ✅ Put total in center (professional look)
            total = values.sum()
            ax.text(0, 0, f'Total\n{total:,}',
                    ha='center', va='center',
                    fontsize=12, fontweight='bold')
                    # fontsize=11, fontweight='bold')

            # ✅ Legend outside only (clean)
            ax.legend(
                wedges,
                labels,
                title="Suppliers",
                loc="center left",
                bbox_to_anchor=(1, 0.5)
            )

            ax.axis('equal')
            plt.tight_layout()

            st.pyplot(fig)


    st.markdown("---")
    
    # Low Stock Alert
    st.subheader("⚠️ Low Stock Alert (< 20 units)")
    low_stock = inventory_df[inventory_df['remaining_stock'] < 20].sort_values('remaining_stock')
    
    if not low_stock.empty:
        st.warning(f"⚠️ {len(low_stock)} items need reordering!")
        st.dataframe(
            low_stock[['item_name', 'remaining_stock', 'supplier_name']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("✅ All items are sufficiently stocked!")
    
    st.markdown("---")
    
    # Full inventory table
    st.subheader("📋 Complete Inventory")
    st.dataframe(inventory_df, use_container_width=True, hide_index=True)

def show_reports(conn):
    """Display reports and insights"""
    st.header("📈 Business Intelligence Reports")
    
    sales_df = get_sales_data(conn)
    inventory_df = get_inventory_data(conn)
    
    if sales_df.empty and inventory_df.empty:
        st.info("ℹ️ No data available for reports")
        return
    
    # Key Insights
    st.subheader("🎯 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if not sales_df.empty:
            best_item = sales_df.groupby('item_name')['quantity_sold'].sum().idxmax()
            best_qty = sales_df.groupby('item_name')['quantity_sold'].sum().max()
            
            revenue_item = sales_df.groupby('item_name')['total_amount'].sum().idxmax()
            revenue_amt = sales_df.groupby('item_name')['total_amount'].sum().max()
            
            st.info(f"""
            **📊 Sales Insights:**
            - **Best Selling Item:** {best_item} ({best_qty:,} units)
            - **Highest Revenue Item:** {revenue_item} (₹{revenue_amt:,.2f})
            - **Total Revenue:** ₹{sales_df['total_amount'].sum():,.2f}
            - **Total Transactions:** {len(sales_df):,}
            """)
    
    with col2:
        if not inventory_df.empty:
            low_count = len(inventory_df[inventory_df['remaining_stock'] < 20])
            
            st.warning(f"""
            **📦 Inventory Insights:**
            - **Low Stock Items:** {low_count} items need reordering
            - **Total Items:** {len(inventory_df.groupby('item_name'))}
            - **Average Stock Usage:** {inventory_df['stock_used'].mean():.1f} units
            - **Action Required:** Reorder items below 20 units
            """)
    
    st.markdown("---")
    
    # Trend Analysis
    if not sales_df.empty and 'month_name' in sales_df.columns:
        # st.subheader("📈 Monthly Sales Trend")
        # monthly_sales = sales_df.groupby('month_name')['total_amount'].sum()
        
        # fig, ax = plt.subplots(figsize=(14, 5))
        # ax.plot(monthly_sales.index, monthly_sales.values, marker='o', 
        #         linewidth=3, markersize=10, color='#1f77b4')
        # ax.set_xlabel('Month', fontsize=12)
        # ax.set_ylabel('Total Sales (₹)', fontsize=12)
        # ax.grid(True, alpha=0.3)
        # plt.xticks(rotation=45)
        # plt.tight_layout()
        # st.pyplot(fig)

        #updated above code here
        st.subheader("📈 Monthly Sales Trend")
        month_order = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

        # sales_df['month_name'] = pd.Categorical(
        #     sales_df['month_name'],
        #     categories=month_order,
        #     ordered=True
        # )

        # monthly_sales = (
        #     sales_df
        #     .groupby('month_name')['total_amount']
        #     .sum()
        #     .sort_index()
        # )

        monthly_sales = (
            sales_df
            .groupby('month_name')['total_amount']
            .sum()
            .reindex(month_order)
            .dropna()   # ✅ removes fake zero months
        )

        fig, ax = plt.subplots(figsize=(14, 5))

        ax.plot(
            monthly_sales.index,
            monthly_sales.values,
            marker='o',
            linewidth=3,
            markersize=8,
            color='#1f77b4'
        )

        # ✅ 5. Add value labels (professional look)
        for i, v in enumerate(monthly_sales.values):
            ax.text(i, v, f'₹{v:,.0f}', ha='center', va='bottom', fontsize=9)

        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Total Sales (₹)', fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.3)

        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(fig)


    st.markdown("---")
    
    # Download Reports
    st.subheader("📥 Download Reports")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if not sales_df.empty:
            csv_sales = sales_df.to_csv(index=False)
            st.download_button(
                label="📊 Download Sales Report",
                data=csv_sales,
                file_name=f"sales_report_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if not inventory_df.empty:
            csv_inventory = inventory_df.to_csv(index=False)
            st.download_button(
                label="📦 Download Inventory Report",
                data=csv_inventory,
                file_name=f"inventory_report_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

def show_data_management(conn):
    """Improved professional data management page"""

    st.header("🗄️ Data Management")

    tab1, tab2 = st.tabs(["💰 Manage Sales", "📦 Manage Inventory"])

    # =========================================================
    # 💰 SALES MANAGEMENT
    # =========================================================
    with tab1:
        st.subheader("Sales Data Management")

        sales_df = get_sales_data(conn)

        if sales_df.empty:
            st.info("No sales data available")
            return

        # ---------- Summary ----------
        st.info(f"Total Records: {len(sales_df)}")

        # ---------- Search ----------
        search = st.text_input("🔍 Search Item Name", key="sales_search")

        if search:
            sales_df = sales_df[
                sales_df["item_name"].str.contains(search, case=False)
            ]

        # ---------- Pagination ----------
        page_size = st.selectbox("Rows per page", [10, 25, 50, 100], index=2)

        total_pages = (len(sales_df) // page_size) + 1
        page = st.number_input("Page", 1, total_pages, 1)

        start = (page - 1) * page_size
        end = start + page_size

        display_df = sales_df.iloc[start:end].copy()

        # =====================================================
        # ⭐⭐⭐ ADD FORMATTING HERE (SALES) ⭐⭐⭐
        # =====================================================

        # Format date
        display_df["date_of_sale"] = (
            pd.to_datetime(display_df["date_of_sale"])
            .dt.strftime("%d %b %Y")
        )

        # Format currency
        display_df["total_amount"] = (
            display_df["total_amount"]
            .apply(lambda x: f"₹{x:,.2f}")
        )

        # ---------- Professional Table ----------
        st.dataframe(
            display_df[
                ["sale_id", "date_of_sale", "item_name", "total_amount"]
            ].rename(columns={
                "sale_id": "ID",
                "date_of_sale": "Date",
                "item_name": "Item",
                "total_amount": "Amount (₹)"
            }),
            use_container_width=True,
            hide_index=True,
            height=400   # ⭐ nicer height
        )

        # ---------- Delete Section ----------
        st.markdown("### ⚠️ Delete Record")

        sale_to_delete = st.selectbox(
            "Select Sale ID",
            display_df["sale_id"]
        )

        if st.button("Delete Selected Sale"):
            if delete_sale(conn, sale_to_delete):
                st.success("Sale deleted successfully!")
                st.rerun()

        st.caption(f"Showing {len(display_df)} of {len(sales_df)} records")

    # =========================================================
    # 📦 INVENTORY MANAGEMENT
    # =========================================================
    with tab2:
        st.subheader("Inventory Data Management")

        inventory_df = get_inventory_data(conn)

        if inventory_df.empty:
            st.info("No inventory data available")
            return

        # ---------- Summary ----------
        st.info(f"Total Records: {len(inventory_df)}")

        # ---------- Search ----------
        search_inv = st.text_input("🔍 Search Item Name", key="inv_search")

        if search_inv:
            inventory_df = inventory_df[
                inventory_df["item_name"].str.contains(search_inv, case=False)
            ]

        # ---------- Pagination ----------
        page_size = st.selectbox("Rows per page", [10, 25, 50, 100], index=2, key="inv_page")

        total_pages = (len(inventory_df) // page_size) + 1
        page = st.number_input("Page", 1, total_pages, 1, key="inv_page_no")

        start = (page - 1) * page_size
        end = start + page_size

        display_df = inventory_df.iloc[start:end].copy()

        # =====================================================
        # ⭐⭐⭐ ADD FORMATTING HERE (INVENTORY) ⭐⭐⭐
        # =====================================================

        display_df["date_of_entry"] = (
            pd.to_datetime(display_df["date_of_entry"])
            .dt.strftime("%d %b %Y")
        )

        # ---------- Professional Table ----------
        st.dataframe(
            display_df[
                ["inventory_id", "date_of_entry", "item_name", "remaining_stock"]
            ].rename(columns={
                "inventory_id": "ID",
                "date_of_entry": "Date",
                "item_name": "Item",
                "remaining_stock": "Stock"
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )

        # ---------- Delete Section ----------
        st.markdown("### ⚠️ Delete Record")

        inv_to_delete = st.selectbox(
            "Select Inventory ID",
            display_df["inventory_id"]
        )

        if st.button("Delete Selected Inventory"):
            if delete_inventory(conn, inv_to_delete):
                st.success("Inventory deleted successfully!")
                st.rerun()

        st.caption(f"Showing {len(display_df)} of {len(inventory_df)} records")

# ===========================
# MAIN EXECUTION
# ===========================

def main():
    """Main application entry point"""
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    # Initialize database connection
    if 'connection' not in st.session_state:
        conn = init_connection()
        if conn:
            st.session_state['connection'] = conn
            create_tables(conn)
            create_default_user(conn)
    
    # Route to appropriate page
    if not st.session_state['logged_in']:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
    