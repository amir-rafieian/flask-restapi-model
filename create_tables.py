# =============================================================================
# Import Libraries
# =============================================================================
import sqlite3

# =============================================================================
# Initialize connection
# =============================================================================
connection = sqlite3.connect('data.db') #it will create a sqlite database

cursor = connection.cursor() #cursor is responsible for executing queries

# =============================================================================
# Queries
# =============================================================================
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)


connection.commit()


connection.close()