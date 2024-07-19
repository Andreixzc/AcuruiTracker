import sqlite3
import csv

def check_records(csv_file, db_file):
    # Read data from the CSV file
    with open(csv_file, newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        csv_data = [row for row in csv_reader]
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Fetch data from the database
    cursor.execute("SELECT * FROM participante")
    db_data = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    # Check the number of records
    if len(csv_data) != len(db_data):
        print(f"Record count mismatch: CSV has {len(csv_data)} records, DB has {len(db_data)} records.")
        return False
    
    # Convert database rows to dictionary format for easier comparison
    db_columns = [column[0] for column in cursor.description]
    db_data_dicts = [dict(zip(db_columns, row)) for row in db_data]
    
    # Check individual records
    for csv_record in csv_data:
        if not any(db_record['CPF'] == csv_record['CPF'] for db_record in db_data_dicts):
            print(f"Record missing in DB: {csv_record}")
            return False
    
    print("All records inserted correctly.")
    return True

# Check records after populating the database
if __name__ == "__main__":
    csv_file = 'Data/planilhaComIdade.csv'
    db_file = 'participants.db'
    check_records(csv_file, db_file)
