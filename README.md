# Project- Inventory & Warehouse-Management Using Python and MySQL
SQL Internship Project-2

# Abstract:
This project implements a warehouse inventory tracking system with a **MySQL** backend and a **Python** frontend. It supports monitoring stock levels across multiple warehouses, generating alerts for low stock, and visualizing inventory distribution. Designed to manage stock levels across multiple warehouses, suppliers, and products. This project simulates real-world prototype for inventory operations with data visualizations and alerts for stock shortages.

# Project Overview:
This system manages inventory for a retail enterprise spread across five warehouses in Odisha: Bhubaneswar, Cuttack, Sambalpur, Rourkela, and Puri. It supports:
  1. Realistic sample data generation for products, suppliers, warehouses, and stock levels.
  2. Monitoring of stock quantities per product and warehouse.
  3. Alert system for low stock levels (threshold = 100 units).
  4. Stock transfer options between warehouses.
  5. Visualizations for warehouse-wise stock distribution and product-wise stock counts.
  6. Interactive console menu to choose reports and operations.

 # Features:
  - **Relational Database Schema** (for Products, Warehouses, Suppliers, and Stock)
  - **Sample Data Insertion** (for realistic inventory simulation)
  - **Menu-driven Python Console** (to interact with inventory data)
  - **Stock Alerts** (for products below minimum quantity)
  - **Visualization**: Pie charts and bar graphs for warehouse and product stock levels
  - **Cross-warehouse Stock Lookup** (for efficient stock transfer decisions)

# Tools & Technologies:
  -> Python-	Frontend interactive console app
  -> MySQL-	Backend relational database
  -> SQLAlchemy-	Python-MySQL database connector
  -> Faker-	Dummy data generation
  -> Pandas-	Data handling
  -> Matplotlib-	Visualizations (Pie, Bar charts)
  -> Seaborn-	Enhanced data visual styling
  
# Database Schema
*Tables*:
  **products** — Product catalog
  **suppliers** — Supplier details
  **warehouses** — Warehouse locations
  **stock** — Inventory stock per product per warehouse

*Key Relationships*:
  -Stock table links products and warehouses via foreign keys.

# Setup Steps:
1. Ensure MySQL server is running.
2. Run the Python script Inventory_Warehouse_Management.py to:
3. Create database and tables
4. Insert sample data
5. Launch the interactive menu-driven dashboard

# Usage:
Upon running, the console menu offers:
  1. Show current stock alerts — Lists products below the threshold in any warehouse.
![SharedScreenshot 1](https://github.com/user-attachments/assets/f8460fa4-f962-48d3-8ce3-611dff873307)

  2. View stock distribution per warehouse — Pie chart of stock totals across warehouses.
<img width="700" height="700" alt="Figure_1" src="https://github.com/user-attachments/assets/328a34a7-37fa-463e-a06c-105a75ce0b3a" />

  3. View stock count per product in a warehouse — Bar chart for product quantities in selected warehouse.
<img width="1000" height="600" alt="Figure_2" src="https://github.com/user-attachments/assets/421d4311-651b-499d-9668-6eed1f8e6e4f" />
<img width="1000" height="600" alt="Figure_3" src="https://github.com/user-attachments/assets/9273d6a8-1fe8-4c53-965a-db5b71c88963" />
 
  4. Exit — Quit the program.  
  5. Users can also check alternate warehouses’ stock when a product alert is triggered and transfer stock between warehouses via the interface.
![SharedScreenshot 2](https://github.com/user-attachments/assets/e681df77-78c7-47a4-b812-a98f788f81e8)

# Key SQL Components:
  -Schema definitions for tables and foreign keys.
  -Data insertion with Faker-generated sample data.
  -Queries to aggregate stock and check alert conditions.
  -Stored procedure for stock transfer.
  -Triggers for low-stock notifications (simulated via queries).
<img width="1294" height="422" alt="Retail Sales Report" src="https://github.com/user-attachments/assets/dbb79f46-75a4-4afb-bd0f-fd32b32b5024" />

# Future Enhancements:
  -Real-time alert notifications via email or dashboard.
  -Web-based user interface using Flask or Django.
  -Integration with purchase order management.
  -Automated reorder processing.
  
