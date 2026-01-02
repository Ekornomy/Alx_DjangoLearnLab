#!/usr/bin/python3
"""
MySQLServer.py - Creates alx_book_store database
"""

import mysql.connector
from mysql.connector import Error

def main():
    """Main function"""
    connection = None
    
    # TRY BLOCK for exception handling
    try:
        # Code to establish connection
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        
        # Create cursor
        cursor = connection.cursor()
        
        # CREATE DATABASE statement (NO SELECT or SHOW)
        cursor.execute("CREATE DATABASE IF NOT EXISTS alx_book_store")
        
        # Required success message
        print("Database 'alx_book_store' created successfully!")
        
        # Close cursor
        cursor.close()
        
    # EXCEPTION HANDLING for MySQL errors
    except Error as e:
        print(f"Error: {e}")
        
    # EXCEPTION HANDLING for other errors
    except Exception as e:
        print(f"Error: {e}")
        
    # FINALLY block to close connection
    finally:
        if connection and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    main()