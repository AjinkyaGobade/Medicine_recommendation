import sqlite3

def view_database():
    # Connect to the database
    conn = sqlite3.connect('medicine_recommendation.db')
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print('\nTables in the database:')
    for table in tables:
        table_name = table[0]
        print(f"\n{'-'*50}\nTable: {table_name}\n{'-'*50}")
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        print(f"Columns: {', '.join(column_names)}")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        print(f"Number of rows: {row_count}")
        
        # Show sample data (up to 5 rows)
        if row_count > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
            rows = cursor.fetchall()
            print("\nSample data:")
            for row in rows:
                print(row)
    
    # Close the connection
    conn.close()

if __name__ == "__main__":
    view_database()