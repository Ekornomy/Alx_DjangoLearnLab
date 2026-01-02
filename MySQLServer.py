 #!/usr/bin/python3
"""
MySQLServer.py - Creates alxbookstore database
"""

import mysql.connector
from mysql.connector import Error

def main():
    """Main function"""
    conn = None
    try:
        # Establish connection
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        
        if conn.is_connected():
            cursor = conn.cursor()
            
            # IMPORTANT: Use "alxbookstore" not "alx_book_store"
            cursor.execute("CREATE DATABASE IF NOT EXISTS alxbookstore")
            
            print("Database 'alxbookstore' created successfully!")
            
            cursor.close()
            
    except Error as e:
        print(f"Error: {e}")
        
    finally:
        if conn and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    main()