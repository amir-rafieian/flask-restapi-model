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
#### Create
create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

#### Insert
user = (1, 'user1', 'abcxyz')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)
connection.commit()


#### Insert many users
users = [(2, 'user2', 'abcxyz'),
         (3, 'rolf', 'asdf')]
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.executemany(insert_query, users)
connection.commit()


#### Select
select_query = "SELECT * FROM users"
res = cursor.execute(select_query)
for row in res:
    print(row)
    
#query = "SELECT * FROM users WHERE username=?"
#result = cursor.execute(query, (username,)) #parameters have to be in the form of a tuple
        
        
# =============================================================================
# Close the connection
# =============================================================================
connection.close()












