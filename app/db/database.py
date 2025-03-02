import sqlite3

#set up database - create userdb and store required users for basic and jwt auth
def setup_db():
    create_user_db()
    store_user()
    create_inventory_db()

#get db connection object
def get_db():
    con = sqlite3.connect("app/db_files/user_credentials.db")
    con.row_factory = sqlite3.Row
    return con

#not being used atm
def get_inventory_db():
    icon = sqlite3.connect("app/db_files/inventory.db")
    icon.row_factory = sqlite3.Row
    return icon    

#create user db
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
    
#not being used at the moment
def create_inventory_db():
    icon = get_inventory_db()
    cursor = icon.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
            item_id INTEGER PRIMARY KEY,
            item_name TEXT NOT NULL,
            item_description TEXT NOT NULL,
            item_price FLOAT NOT NULL
            )
            ''')
    icon.commit()
    icon.close()
    
#store two users with different roles - can be used for basic and jwt auth
def store_user():
    con = get_db()
    cursor = con.cursor()
    cursor.execute("REPLACE INTO users (username, password, role) VALUES (?, ?, ?)", ("testuser", "$2b$12$YAP/SVePrbiS7RMCXVCKTeGfIDAop8qGUXR17kMBM/tVCoWae0oFq", "admin"))
    cursor.execute("REPLACE INTO users (username, password, role) VALUES (?, ?, ?)", ("testuser2", "$2b$12$YAP/SVePrbiS7RMCXVCKTeGfIDAop8qGUXR17kMBM/tVCoWae0oFq", "view"))
    con.commit()
    con.close()
    


