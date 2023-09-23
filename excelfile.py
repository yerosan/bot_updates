# import pandas as pd
# import sqlite3

# # Connect to an in-memory SQLite database
# conn = sqlite3.connect(':memory:')

# # Read the SQL file
# with open('C:/Users/Shewanek/Documents/dumps/Dump20230916/michudatabase_chatdata.sql', 'r', encoding='utf-8') as file:
#     sql_script = file.read()

# # Remove the "AUTO_INCREMENT" syntax
# sql_script = sql_script.replace("AUTO_INCREMENT", "AUTOINCREMENT")
# # Execute the SQL script
# conn.executescript(sql_script)
# # 0938252530 madin shiferaw
# # Execute a specific SQL query
# query = 'SELECT * FROM chatdata'
# data = pd.read_sql_query(query, conn)

# # Close the database connection
# conn.close()

# # Save the data to an Excel file
# data.to_excel('output.xlsx', index=False)


import pandas as pd
import sqlite3

# Connect to an in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Read the SQL file
with open('C:/Users/Shewanek/Documents/dumps/Dump20230916/michudatabase_chatdata.sql', 'r', encoding='utf-8') as file:
    sql_script = file.read()

# Modify the SQL script to use "INTEGER PRIMARY KEY AUTOINCREMENT"
sql_script = sql_script.replace("AUTO_INCREMENT", "INTEGER PRIMARY KEY AUTOINCREMENT")

# Execute each statement individually
cursor.executescript(sql_script)

# Execute a specific SQL query
query = 'SELECT * FROM chatdata'
cursor.execute(query)
data = cursor.fetchall()

# Get column names from the cursor description
columns = [column[0] for column in cursor.description]

# Create a DataFrame from the query results
df = pd.DataFrame(data, columns=columns)

# Close the database connection
cursor.close()
conn.close()

# Save the data to an Excel file
df.to_excel('output.xlsx', index=False)