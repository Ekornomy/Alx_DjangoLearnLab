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
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )

        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS alxbookstore")
        print("Database 'alxbookstore' created successfully!")

        cursor.close()

    except Error as e:
        print("Error:", e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    main()
