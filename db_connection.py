import mysql.connector
from mysql.connector import Error

# This script is used to connect to a MySQL database and execute queries. If you have another type of database, make sure to change the code accordingly if you have to.
def create_connection():
    
    """Create a MySQL database connection."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host='', # Your host here if you are not using localhost
            user='', # Your user here
            password='', # Your password here
            database='' # Your database here
        )
        if connection.is_connected():
            print('Connected to MySQL database.')
            return connection
    except Error as e:
        print('Error:', e)
        return None
    
def query_database(query):
    """Execute an SQL query and return the results."""
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Error as e:
            print('Error executing query:', e)
        finally:
            cursor.close()
            connection.close()
            print('Connection closed.')
    else:
        return None
    
def execute_query(query):
    """Execute an SQL query that does not return any result (e.g., UPDATE, INSERT, DELETE)."""
    connection = create_connection()

    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()  # Commit the changes to the database
            print('Query executed successfully.')
        except Error as e:
            print('Error executing query:', e)
        finally:
            cursor.close()
            connection.close()
            print('Connection closed.')
    else:
        print('Connection failed.')
