import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random

# --- CONFIGURATION SETUP---
HOST = "localhost"
USER = "root"
PASSWORD = "Password"  
DATABASE = "warehouse_inventory"

REORDER_LEVEL = 100

# --- Connecting to MySQL  ---
conn = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD
)
cursor = conn.cursor()

# --- 1. Creating Database ---
cursor.execute(f"DROP DATABASE IF EXISTS {DATABASE}")
cursor.execute(f"CREATE DATABASE {DATABASE}")
cursor.execute(f"USE {DATABASE}")

# --- 2. Creating Tables ---
cursor.execute("""
CREATE TABLE Warehouses (
    warehouse_id INT PRIMARY KEY AUTO_INCREMENT,
    warehouse_name VARCHAR(100) UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE Products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE Stock (
    stock_id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    warehouse_id INT,
    quantity INT,
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (warehouse_id) REFERENCES Warehouses(warehouse_id)
)
""")

conn.commit()

# --- 3. Inserting sample Warehouses ---
warehouses = ["Bhubaneswar", "Cuttack", "Sambalpur", "Rourkela", "Puri"]
cursor.executemany("INSERT INTO Warehouses (warehouse_name) VALUES (%s)", [(w,) for w in warehouses])
conn.commit()

# --- 4. Insert sample Products ---
products = [
    "Laptop", "Smartphone", "Headphones", "Keyboard", "Monitor",
    "Mouse", "Tablet", "Printer", "Camera", "Router"
]
cursor.executemany("INSERT INTO Products (product_name) VALUES (%s)", [(p,) for p in products])
conn.commit()

# --- 5. Inserting Stock data ---
# (Through warehouse IDs)
cursor.execute("SELECT warehouse_id, warehouse_name FROM Warehouses")
warehouse_data = cursor.fetchall()  

cursor.execute("SELECT product_id, product_name FROM Products")
product_data = cursor.fetchall() 

stock_records = []
for w_id, w_name in warehouse_data:
    for p_id, p_name in product_data:
        # Random quantity, mostly above reorder, some below to test alert
        if random.random() < 0.15:
            qty = random.randint(10, REORDER_LEVEL-1)  # Below reorder threshold ~15% products
        else:
            qty = random.randint(REORDER_LEVEL, 300)  # Above reorder threshold
        stock_records.append((p_id, w_id, qty))

cursor.executemany("INSERT INTO Stock (product_id, warehouse_id, quantity) VALUES (%s, %s, %s)", stock_records)
conn.commit()

# --- Creating an SQLAlchemy engine for pandas ---
engine = create_engine(f"mysql+pymysql://root:Nkm%405120800@{HOST}/{DATABASE}")
conn.close()

# Reconnecting using mysql.connector with dict cursor for easy access in menu
conn = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)
cursor = conn.cursor(dictionary=True)

# --- MENU FUNCTIONS ---
def show_stock_alerts():
    print("\n-- STOCK ALERTS: Products below reorder level --")
    query = f"""
        SELECT w.warehouse_name, p.product_name, s.quantity
        FROM Stock s
        JOIN Warehouses w ON s.warehouse_id = w.warehouse_id
        JOIN Products p ON s.product_id = p.product_id
        WHERE s.quantity < {REORDER_LEVEL}
        ORDER BY p.product_name, w.warehouse_name;
    """
    cursor.execute(query)
    alerts = cursor.fetchall()
    if not alerts:
        print("No stock alerts. All products above reorder level.")
        return
    for idx, row in enumerate(alerts, 1):
        print(f"{idx}. Product: {row['product_name']} | Warehouse: {row['warehouse_name']} | Qty: {row['quantity']}")

    prod_set = sorted({row['product_name'] for row in alerts})
    print("\nEnter product number from alert list to see stock across all warehouses, or 0 to return:")
    while True:
        try:
            choice = int(input(f"Enter choice (0-{len(prod_set)}): "))
            if choice == 0:
                return
            if 1 <= choice <= len(prod_set):
                product_name = prod_set[choice - 1]
                show_stock_across_warehouses(product_name)
                return
            else:
                print("Invalid input, try again.")
        except ValueError:
            print("Please enter a valid number.")

def show_stock_across_warehouses(product_name):
    print(f"\nStock of '{product_name}' across all warehouses:")
    query = """
        SELECT w.warehouse_name, s.quantity
        FROM Stock s
        JOIN Warehouses w ON s.warehouse_id = w.warehouse_id
        JOIN Products p ON s.product_id = p.product_id
        WHERE p.product_name = %s
        ORDER BY w.warehouse_name;
    """
    cursor.execute(query, (product_name,))
    rows = cursor.fetchall()
    if not rows:
        print("No data found for this product.")
        return
    for row in rows:
        print(f"Warehouse: {row['warehouse_name']} | Quantity: {row['quantity']}")
    print()

def stock_distribution_per_warehouse():
    print("\n-- Stock Distribution Per Warehouse --")
    query = """
        SELECT w.warehouse_name, SUM(s.quantity) as total_quantity
        FROM Stock s
        JOIN Warehouses w ON s.warehouse_id = w.warehouse_id
        GROUP BY w.warehouse_name;
    """
    df = pd.read_sql(query, engine)
    if df.empty:
        print("No stock data found.")
        return
    plt.figure(figsize=(7,7))
    plt.pie(df['total_quantity'], labels=df['warehouse_name'], autopct='%1.1f%%', startangle=140)
    plt.title("Total Stock Distribution by Warehouse")
    plt.axis('equal')
    plt.show()

def stock_count_per_product_in_warehouse():
    print("\n-- Stock Count per Product in a Warehouse --")
    cursor.execute("SELECT warehouse_id, warehouse_name FROM Warehouses ORDER BY warehouse_name")
    warehouses = cursor.fetchall()
    if not warehouses:
        print("No warehouses found.")
        return

    print("Select warehouse:")
    for w in warehouses:
        print(f"{w['warehouse_id']}. {w['warehouse_name']}")
    while True:
        try:
            w_choice = int(input("Enter warehouse ID: "))
            if any(w['warehouse_id'] == w_choice for w in warehouses):
                break
            else:
                print("Invalid warehouse ID, try again.")
        except ValueError:
            print("Please enter a valid number.")

    query = """
        SELECT p.product_name, s.quantity
        FROM Stock s
        JOIN Products p ON s.product_id = p.product_id
        WHERE s.warehouse_id = %s
        ORDER BY p.product_name;
    """
    df = pd.read_sql(query, engine, params=(w_choice,))
    if df.empty:
        print("No stock data for this warehouse.")
        return
    plt.figure(figsize=(10,6))
    sns.barplot(data=df, x='product_name', y='quantity', color='maroon')
    plt.title(f"Stock Count per Product in Warehouse ID {w_choice}")
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Quantity")
    plt.xlabel("Product")
    plt.tight_layout()
    plt.show()

# --- MAIN MENU ---
def main():
    while True:
        print("\n=== Warehouse Inventory Management Dashboard ===")
        print("1. Show current stock alerts")
        print("2. View stock distribution per warehouse")
        print("3. View stock count per product in a warehouse")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            show_stock_alerts()
        elif choice == '2':
            stock_distribution_per_warehouse()
        elif choice == '3':
            stock_count_per_product_in_warehouse()
        elif choice == '4':
            print("Exiting. Thank you!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()
    cursor.close()
    conn.close()
