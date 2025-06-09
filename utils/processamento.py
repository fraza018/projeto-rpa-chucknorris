import sqlite3
import re

def processar_dados():
    conn = sqlite3.connect("database/projeto_rpa.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM piadas")
    dados = cursor.fetchall()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dados_processados (
            id TEXT PRIMARY KEY,
            palavras_longas TEXT
        )
    ''')

    for id, texto in dados:
        palavras = re.findall(r'\b\w{7,}\b', texto)
        palavras_longas = ', '.join(palavras)
        cursor.execute("INSERT OR REPLACE INTO dados_processados (id, palavras_longas) VALUES (?, ?)", (id, palavras_longas))

    conn.commit()
    conn.close()
