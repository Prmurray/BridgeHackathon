import sqlite3

def clear_database(db_path='consultants.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # List of tables to clear
    tables = ['consultants']
    
    for table in tables:
        try:
            cursor.execute(f"DELETE FROM {table}")
            print(f"Cleared table: {table}")
        except sqlite3.OperationalError as e:
            print(f"Error clearing table {table}: {e}")
    
    conn.commit()
    conn.close()


clear_database()