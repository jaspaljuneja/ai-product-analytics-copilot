import sqlite3
import random
import os
from datetime import datetime, timedelta

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

DB_PATH = "data/analytics.db"

NUM_USERS = 10000
NUM_PRODUCTS = 50
NUM_EVENTS = 220000
NUM_ORDERS = 12000

START_DATE = datetime(2026, 1, 1)
END_DATE = datetime(2026, 9, 1)

random.seed(42)

# --------------------------------------------------
# DATABASE SETUP
# --------------------------------------------------

os.makedirs("data", exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Start fresh every time we run the script
cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("DROP TABLE IF EXISTS events")
cursor.execute("DROP TABLE IF EXISTS products")
cursor.execute("DROP TABLE IF EXISTS users")

cursor.execute("""
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    signup_date DATE,
    country TEXT,
    device TEXT,
    age_group TEXT
)
""")

cursor.execute("""
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price REAL
)
""")

cursor.execute("""
CREATE TABLE events (
    event_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    event_name TEXT,
    event_date DATE,
    product_id INTEGER,
    session_id TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
""")

cursor.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    product_id INTEGER,
    order_date DATE,
    quantity INTEGER,
    revenue REAL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
""")

# --------------------------------------------------
# PRODUCTS
# --------------------------------------------------

product_names = [
    "Wireless Headphones",
    "Smart Watch",
    "Running Shoes",
    "Laptop Stand",
    "Bluetooth Speaker",
    "Mechanical Keyboard",
    "Wireless Mouse",
    "USB-C Hub",
    "Fitness Tracker",
    "Phone Case"
]

categories = [
    "Electronics",
    "Sports",
    "Accessories"
]

products = []

for product_id in range(1, NUM_PRODUCTS + 1):
    name = random.choice(product_names) + f" {product_id}"
    category = random.choice(categories)
    price = round(random.uniform(25, 300), 2)

    products.append(
        (product_id, name, category, price)
    )

cursor.executemany("""
INSERT INTO products
(product_id, product_name, category, price)
VALUES (?, ?, ?, ?)
""", products)

# --------------------------------------------------
# USERS
# --------------------------------------------------

countries = ["USA", "Canada", "UK", "India", "Germany"]

devices = ["iPhone", "Android", "Web"]

age_groups = ["18-24", "25-34", "35-44", "45-54", "55+"]

users = []

for user_id in range(1, NUM_USERS + 1):

    signup_date = START_DATE + timedelta(
        days=random.randint(0, 240)
    )

    country = random.choices(
        countries,
        weights=[50, 15, 15, 15, 5]
    )[0]

    device = random.choices(
        devices,
        weights=[40, 35, 25]
    )[0]

    age_group = random.choice(age_groups)

    users.append(
        (
            user_id,
            signup_date.strftime("%Y-%m-%d"),
            country,
            device,
            age_group
        )
    )

cursor.executemany("""
INSERT INTO users
(user_id, signup_date, country, device, age_group)
VALUES (?, ?, ?, ?, ?)
""", users)

# --------------------------------------------------
# EVENTS
# --------------------------------------------------

event_names = [
    "app_open",
    "product_view",
    "add_to_cart",
    "checkout_started",
    "purchase"
]

events = []

for event_id in range(1, NUM_EVENTS + 1):

    user_id = random.randint(1, NUM_USERS)
    product_id = random.randint(1, NUM_PRODUCTS)

    event_date = START_DATE + timedelta(
        days=random.randint(0, 243)
    )

    user = users[user_id - 1]
    device = user[3]

    # Normal event distribution
    event = random.choices(
        event_names,
        weights=[35, 30, 18, 10, 7]
    )[0]

    # --------------------------------------------------
    # AUGUST CONVERSION PROBLEM
    # --------------------------------------------------

    # August = days 212 onward approximately
    if event_date.month == 8:

        # Reduce purchases significantly
        if event == "purchase":
            if random.random() < 0.45:
                event = "checkout_started"

        # Web users have an even bigger conversion problem
        if device == "Web" and event == "purchase":
            if random.random() < 0.50:
                event = "checkout_started"

    session_id = f"session_{random.randint(1, 50000)}"

    events.append(
        (
            event_id,
            user_id,
            event,
            event_date.strftime("%Y-%m-%d"),
            product_id,
            session_id
        )
    )

cursor.executemany("""
INSERT INTO events
(event_id, user_id, event_name, event_date, product_id, session_id)
VALUES (?, ?, ?, ?, ?, ?)
""", events)

# --------------------------------------------------
# ORDERS
# --------------------------------------------------

orders = []

for order_id in range(1, NUM_ORDERS + 1):

    user_id = random.randint(1, NUM_USERS)
    product_id = random.randint(1, NUM_PRODUCTS)

    product = products[product_id - 1]
    price = product[3]

    order_date = START_DATE + timedelta(
        days=random.randint(0, 243)
    )

    quantity = random.randint(1, 3)

    revenue = round(price * quantity, 2)

    # Fewer orders in August
    if order_date.month == 8:
        if random.random() < 0.30:
            continue

    orders.append(
        (
            order_id,
            user_id,
            product_id,
            order_date.strftime("%Y-%m-%d"),
            quantity,
            revenue
        )
    )

cursor.executemany("""
INSERT INTO orders
(order_id, user_id, product_id, order_date, quantity, revenue)
VALUES (?, ?, ?, ?, ?, ?)
""", orders)

# --------------------------------------------------
# SAVE
# --------------------------------------------------

conn.commit()

# --------------------------------------------------
# VERIFY
# --------------------------------------------------

print("Database populated successfully!")

cursor.execute("SELECT COUNT(*) FROM users")
print("Users:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM products")
print("Products:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM events")
print("Events:", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM orders")
print("Orders:", cursor.fetchone()[0])

conn.close()
