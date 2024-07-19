import csv
import sqlite3

def populate_database_from_csv(csv_file):
    conn = sqlite3.connect('participants.db')
    cursor = conn.cursor()

    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute('''
            INSERT OR REPLACE INTO participante (EMAIL, NOME, ACADEMIA, CIDADE, PCD, DATA_NASCIMENTO, CPF, SEXO, TELEFONE, PROVA_14_09, PROVA_15_09, IDADE)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['EMAIL'],
                row['NOME'],
                row['ACADEMIA'],
                row['CIDADE'],
                row['PCD'],
                row['DATA NASCIMENTO'],
                row['CPF'],
                row['SEXO'],
                row['TELEFONE'],
                row['PROVA 14/09'],
                row['PROVA 15/09'],
                row['IDADE']
            ))

    conn.commit()
    conn.close()

# Run this function to populate the database from the CSV file

populate_database_from_csv('Data/planilhaComIdade.csv')
