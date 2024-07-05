import mysql.connector
import uuid
try:
    # Establish a connection to MySQL
    mydb = mysql.connector.connect(
        host="63.34.199.220",
        port="3306",
        user="sane",
        password="sanemysql!2244",
        database="michuBot_db"
    )
    mycursor = mydb.cursor()

    # If no errors occur, print a success message
    # print("Connected to MySQL database successfully.")
    

    # Close the database connection
    # mydb.close()

except mysql.connector.Error as err:
    # If there's an error, print the error message
    print("Error connecting to MySQL database:", err)


def command(user_id, language, command):
    try:
        # Generate a UUID for the id column
        # id_val = str(uuid.uuid4())
        
    
        # Define the SQL query
        sql = "INSERT INTO command (user_id, lang_id, command) VALUES (%s, %s, %s)"
        # Define the values to insert into the query
        val = (user_id, language, command)
        # Execute the SQL query
        mycursor.execute(sql, val)
        
        # Commit the changes to the database
        mydb.commit()
        # print("Data stored successfully.")
    except mysql.connector.Error as err:
        print(f"Error storing data: {err}")


def dev(user_id, lang_id, email, suggestion):
    try:
        # id_val = str(uuid.uuid4())
        sql = "INSERT INTO dev (user_id, lang_id, email, suggestion) VALUES (%s, %s, %s, %s)"
        val = (user_id, lang_id, email, suggestion)
        mycursor.execute(sql, val)
        mydb.commit()
        # print("Data stored successfully.")
    except mysql.connector.Error as err:
        print(f"Error storing data: {err}")

def michuChannel(user_id, lang_id):
    try:
        
        # id_val = str(uuid.uuid4())
        sql = "INSERT INTO michuChannel (user_id, lang_id) VALUES (%s, %s)"
        val = (user_id, lang_id)
        mycursor.execute(sql, val)
        mydb.commit()
        # print("Data stored successfully.")
    except mysql.connector.Error as err:
        print(f"Error storing data: {err}")

def userComment(user_id, lang_id, comment):
    try:
        # id_val = str(uuid.uuid4())
        sql = "INSERT INTO userComment (user_id, lang_id, comment) VALUES (%s, %s, %s)"
        val = (user_id, lang_id, comment)
        mycursor.execute(sql, val)
        mydb.commit()
        # print("Data stored successfully.")
    except mysql.connector.Error as err:
        print(f"Error storing data: {err}")
        
def userRank(user_id, lang_id, rating):
    try:
        
        # id_val = str(uuid.uuid4())
        sql = "INSERT INTO userRank (user_id, lang_id, rating) VALUES (%s, %s, %s)"
        val = (user_id, lang_id, rating)
        mycursor.execute(sql, val)
        mydb.commit()
        # print("Data stored successfully.")
    except mysql.connector.Error as err:
        print(f"Error storing data: {err}")
        
def faq(user_id, lang_id):
    try:
        
        # id_val = str(uuid.uuid4())
        sql = "INSERT INTO faq (user_id, lang_id) VALUES (%s, %s)"
        val = (user_id, lang_id)
        mycursor.execute(sql, val)
        mydb.commit()
        # print("Data stored successfully.")
    except mysql.connector.Error as err:
        print(f"Error storing data: {err}")

def userInfo(user_id, user_name, first_name, lang_id):
    try:
        # Check if the user_id already exists in the database
        mycursor.execute("SELECT * FROM userInfo WHERE user_id = %s", (user_id,))
        existing_data = mycursor.fetchone()

        if existing_data:
            # print("Conversation data for user_id", user_id, "already exists. Skipping insertion.")
            return
        
        sql = "INSERT INTO userInfo (user_id, user_name, first_name, lang_id) VALUES (%s, %s, %s, %s)"
        val = (user_id, user_name, first_name, lang_id)
        mycursor.execute(sql, val)
        mydb.commit()
        # print("Data stored successfully.")
    except mysql.connector.Error as err:
        print(f"Error storing data: {err}")

def userlanguage(lang_id, language):
    try:
        # Check if the user_id already exists in the database
        mycursor.execute("SELECT * FROM userlanguage WHERE lang_id = %s", (lang_id,))
        existing_data = mycursor.fetchone()

        if existing_data:
            # print("Conversation data for lang_id", lang_id, "already exists. Skipping insertion.")
            return
        # id_val = str(uuid.uuid4())
        sql = "INSERT INTO userlanguage (lang_id,language) VALUES (%s, %s)"
        val = (lang_id, language)
        mycursor.execute(sql, val)
        mydb.commit()
        # print("Data stored successfully.")
    except mysql.connector.Error as err:
        print(f"Error storing data: {err}")
        
def buttonQuestion(user_id, lang_id, asked_button, intent, confidence, answer):
    try:
        answer_id = fetchAnswerIdByIntent(answer)
        # id_val = str(uuid.uuid4())
        sql = "INSERT INTO buttonQuestion (user_id, lang_id, asked_button, intent, answer_id, confidence) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (user_id, lang_id, asked_button, intent, answer_id, confidence)
        mycursor.execute(sql, val)
        mydb.commit()
        # print("Data stored successfully.")
    except mysql.connector.Error as err:
        print(f"Error storing data: {err}")

def fetchAnswerIdByIntent(answer):
    try:
        sql = "SELECT ans_id FROM botAnswer WHERE answer = %s"
        val = (answer,)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()
        if result:
            return result[0]  # Return the fetched answer_id
        else:
            return None  # Return None if no match found
    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
        return None
def textQuestion(user_id, lang_id, question, intent, confidence, answer):
    try:
        answer_id = fetchAnswerIdByIntent(answer)
        # id_val = str(uuid.uuid4())
        sql = "INSERT INTO textQuestion (user_id, lang_id, question, intent, answer_id, confidence) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (user_id, lang_id, question, intent, answer_id, confidence)
        mycursor.execute(sql, val)
        mydb.commit()
        # print("Data stored successfully.")
    except mysql.connector.Error as err:
        print(f"Error storing data: {err}")
        
def botAnswer(user_id, lang_id,  sel_intent, b_answer):
    try:
        # Check if the user_id already exists in the database
        mycursor.execute("SELECT * FROM botAnswer WHERE answer = %s", (b_answer,))
        existing_data = mycursor.fetchone()

        if existing_data:
            # print("Conversation data for lang_id", lang_id, "already exists. Skipping insertion.")
            return
   
        # id_val = str(uuid.uuid4())
        sql = "INSERT INTO botAnswer (user_id, lang_id, intent, answer) VALUES (%s, %s, %s, %s)"
        val = (user_id, lang_id, sel_intent, b_answer)
        mycursor.execute(sql, val)
        mydb.commit()
        # print("Data stored successfully.")
    except mysql.connector.Error as err:
        print(f"Error storing data: {err}")
 
def update_lang_id(user_id, new_lang_id):
    try:
        sql = "UPDATE userInfo SET lang_id = %s WHERE user_id = %s"
        val = (new_lang_id, user_id)
        mycursor.execute(sql, val)
        mydb.commit()  # Commit the transaction
        # print(f"Lang_id updated successfully for user_id {user_id}")
    except mysql.connector.Error as err:
        print(f"Error updating lang_id: {err}")

def fetch_user_lang():
    try:
        sql = "SELECT user_id, lang_id FROM userInfo WHERE lang_id IS NOT NULL AND lang_id <> ''"
        mycursor.execute(sql)
        results = mycursor.fetchall()
        if results:
            return {int(user_id): int(lang_id) for user_id, lang_id in results}  # Return as dictionary with user_id as key and lang_id as value
        else:
            return {}  # Return an empty dictionary if no match found
    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
        return None


    
     
# mydb.close()   
# userlanguage('English')
# command('4098409', 2, '/start', 'very good')
