#!/usr/bin/python3
"""
MySQLServer.py - Creates alx_book_store database
"""

import mysql.connector
from mysql.connector import Error

def main():
    """Main function to create database"""
    connection = None
    
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS alx_book_store")
            print("Database 'alx_book_store' created successfully!")
            cursor.close()
    
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        if connection and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    main()