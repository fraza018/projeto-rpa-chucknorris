import sqlite3
import os

def criar_banco():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect("database/projeto_rpa.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS piadas (
            id TEXT PRIMARY KEY,
            texto TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_dado(id, texto):
    conn = sqlite3.connect("database/projeto_rpa.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO piadas (id, texto) VALUES (?, ?)", (id, texto))
    conn.commit()
    conn.close()
