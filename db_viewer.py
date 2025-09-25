import sqlite3
import os

def view_database():
    # Database file path
    db_path = 'medicine_recommendation.db'
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"Database file '{db_path}' not found!")
        return
    
    print(f"\nDatabase location: {os.path.abspath(db_path)}")
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print('\nTables in the database:')
    for i, table in enumerate(tables):
        print(f"{i+1}. {table[0]}")
    
    while True:
        try:
            choice = input("\nEnter table number to view (or 'q' to quit): ")
            
            if choice.lower() == 'q':
                break
            
            table_index = int(choice) - 1
            if table_index < 0 or table_index >= len(tables):
                print("Invalid table number!")
                continue
            
            table_name = tables[table_index][0]
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
            
            # Show data with pagination
            page_size = 10
            page = 1
            
            while True:
                offset = (page - 1) * page_size
                cursor.execute(f"SELECT * FROM {table_name} LIMIT {page_size} OFFSET {offset}")
                rows = cursor.fetchall()
                
                if not rows:
                    print("No more data!")
                    break
                
                print(f"\nShowing page {page} (rows {offset+1}-{offset+len(rows)} of {row_count}):")
                print("-" * 50)
                
                # Print column headers
                header = "  ".join(column_names)
                print(header)
                print("-" * len(header))
                
                # Print rows
                for row in rows:
                    print("  ".join(str(item) for item in row))
                
                if offset + len(rows) >= row_count:
                    print("\nEnd of data reached.")
                    break
                
                nav = input("\nPress Enter for next page, 'b' for previous page, or 'q' to return to table selection: ")
                if nav.lower() == 'q':
                    break
                elif nav.lower() == 'b' and page > 1:
                    page -= 1
                else:
                    page += 1
                    
        except ValueError:
            print("Please enter a valid number!")
        except Exception as e:
            print(f"Error: {e}")
    
    # Close the connection
    conn.close()
    print("\nDatabase connection closed.")

if __name__ == "__main__":
    print("SQLite Database Viewer")
    print("=" * 20)
    view_database()