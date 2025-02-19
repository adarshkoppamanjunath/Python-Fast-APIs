import sqlite3


def setup_db():
    create_user_db()
    store_user()
    create_inventory_db()
    
def get_db():
    con = sqlite3.connect("user_credentials.db")
    con.row_factory = sqlite3.Row
    return con

def get_inventory_db():
    icon = sqlite3.connect("inventory.db")
    icon.row_factory = sqlite3.Row
    return icon    

def create_user_db():
    con = get_db()
    cursor = con.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
            )
            ''')
    con.commit()
    con.close()

def create_inventory_db():
    icon = get_db()
    cursor = icon.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            product_description TEXT NOT NULL  )
            ''')
    icon.commit()
    icon.close()

def store_user():
    con = get_db()
    cursor = con.cursor()
    cursor.execute("REPLACE INTO users (username, password, role) VALUES (?, ?, ?)", ("testuser", "$2b$12$YAP/SVePrbiS7RMCXVCKTeGfIDAop8qGUXR17kMBM/tVCoWae0oFq", "admin"))
    cursor.execute("REPLACE INTO users (username, password, role) VALUES (?, ?, ?)", ("testuser2", "$2b$12$YAP/SVePrbiS7RMCXVCKTeGfIDAop8qGUXR17kMBM/tVCoWae0oFq", "view"))
    con.commit()
    con.close()
    


