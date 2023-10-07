import pandas as pd


# Read the SQL file into a DataFrame
sql_file = 'C:/Users/Shewanek/Desktop/Michuu_ChatBot/michudatabase_chatdata.sql'  # Replace with the path to your SQL file
# with open(sql_file, 'r', encoding='utf-8') as file:
#     query = file.read()

# data = pd.read_sql(query, con=None)
data = pd.read_csv(sql_file, delimiter=';')

# Close the database connection
# conn.close()

# Save the data to an Excel file
output_file = 'C:/Users/Shewanek/Desktop/Michuu_ChatBotfile.xlsx'  # Replace with the desired output file path
data.to_excel(output_file, index=False)
