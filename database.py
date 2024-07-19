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

setup_database()
