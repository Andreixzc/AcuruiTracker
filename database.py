import sqlite3

def setup_database():
    conn = sqlite3.connect('participants.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS participante (
        EMAIL TEXT,
        NOME TEXT,
        ACADEMIA TEXT,
        CIDADE TEXT,
        PCD TEXT,
        DATA_NASCIMENTO TEXT,
        CPF TEXT PRIMARY KEY,
        SEXO TEXT,
        TELEFONE TEXT,
        PROVA_14_09 TEXT,
        PROVA_15_09 TEXT,
        IDADE INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS competicao (
        cpf_participante TEXT PRIMARY KEY,
        Kids100_14_09_24 TEXT,
        Fast200_14_09_24 TEXT,
        Absolut1000_14_09_24 TEXT,
        Long4000_14_09_24 TEXT,
        Open500_14_09_24 TEXT,
        Golden2000_14_09_24 TEXT,
        Clinica_17_08_24 TEXT,
        FOREIGN KEY(cpf_participante) REFERENCES participante(CPF)
    )
    ''')

    conn.commit()
    conn.close()

def update_competition(cpf, competition, final_time):
    print(f"Updating competition {competition} for participant {cpf} with time {final_time}")
    conn = sqlite3.connect('participants.db')
    cursor = conn.cursor()

    query_check = """
    SELECT COUNT(*) FROM competicao
    WHERE cpf_participante = ?
    """
    cursor.execute(query_check, (cpf,))
    exists = cursor.fetchone()[0] > 0

    if exists:
        query_update = f"""
        UPDATE competicao
        SET {competition} = ?
        WHERE cpf_participante = ?
        """
        cursor.execute(query_update, (final_time, cpf))
    else:
        query_insert = f"""
        INSERT INTO competicao (cpf_participante, {competition})
        VALUES (?, ?)
        """
        cursor.execute(query_insert, (cpf, final_time))

    conn.commit()
    conn.close()

def finalize_registration():
    conn = sqlite3.connect('participants.db')
    cursor = conn.cursor()

    categories = {
        "A - Sub 15": (0, 15),
        "B - 16-19": (16, 19),
        "C - 20-24": (20, 24),
        "D - 25-29": (25, 29),
        "E - 30-34": (30, 34),
        "F - 35-39": (35, 39),
        "G - 40-44": (40, 44),
        "H - 45-49": (45, 49),
        "I - 50-54": (50, 54),
        "J - 55-59": (55, 59),
        "K - 60-64": (60, 64),
        "L - 65-69": (65, 69),
        "M - 70-74": (70, 74),
        "N - 75-80": (75, 80),
        "O - 80-84": (80, 84),
        "P - 85-89": (85, 89),
        "Q - 90-94": (90, 94),
        "R - 95-99": (95, 99),
    }

    ranking = {}

    for category, age_range in categories.items():
        min_age, max_age = age_range
        query = f"""
        SELECT participante.NOME, competicao.Clinica_17_08_24
        FROM participante
        JOIN competicao ON participante.CPF = competicao.cpf_participante
        WHERE participante.IDADE BETWEEN {min_age} AND {max_age}
        ORDER BY CAST(competicao.Clinica_17_08_24 AS TEXT)
        """
        cursor.execute(query)
        ranking[category] = cursor.fetchall()

    query = """
    SELECT participante.NOME, competicao.Clinica_17_08_24
    FROM participante
    JOIN competicao ON participante.CPF = competicao.cpf_participante
    WHERE participante.PCD = 1
    ORDER BY CAST(competicao.Clinica_17_08_24 AS TEXT)
    """
    cursor.execute(query)
    ranking["PCD"] = cursor.fetchall()

    conn.close()

    with open('ranking.txt', 'w') as f:
        for category, participants in ranking.items():
            f.write(f"Category: {category}\n")
            for participant in participants:
                f.write(f"{participant[0]}: {participant[1]}\n")
            f.write("\n")

    print("Ranking list generated and saved to ranking.txt")

import sqlite3

def clean_database_for_competition(competition_name):
    """
    Deletes records related to a specific competition from the competicao table.
    
    Args:
        competition_name (str): The name of the competition to clean from the database.
    """
    conn = sqlite3.connect('participants.db')
    cursor = conn.cursor()

    # Prepare the SQL query to delete records related to the specific competition
    query = f"""
    DELETE FROM competicao
    WHERE {competition_name} IS NOT NULL
    """
    
    # Execute the query
    cursor.execute(query)
    
    # Commit the changes
    conn.commit()
    
    # Close the connection
    conn.close()

    print(f"Cleaned records for competition: {competition_name}")

