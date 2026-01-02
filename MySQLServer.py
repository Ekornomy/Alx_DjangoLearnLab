 #!/usr/bin/python3
"""
MySQLServer.py - Creates alx_book_store database
"""

import mysql.connector
from mysql.connector import Error

def create_database():
    """
    Create alx_book_store database
    """
    connection = None
    try:
        # Establish connection to MySQL server
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        
        if connection.is_connected():
            # Create cursor
            cursor = connection.cursor()
            
            # Create database if not exists
            cursor.execute("CREATE DATABASE IF NOT EXISTS alx_book_store")
            
            print("Database 'alx_book_store' created successfully!")
            
            # Close cursor
            cursor.close()
            
    except Error as e:
        print(f"Error: {e}")
        
    finally:
        # Close connection
        if connection and connection.is_connected():
            connection.close()

def main():
    """Main function"""
    create_database()

if __name__ == "__main__":
    main()