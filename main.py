import requests
import sqlite3
import re
import smtplib
import ssl
import os
from email.message import EmailMessage

# 1. Coleta de dados da API
def coletar_dados():
    url = "https://api.chucknorris.io/jokes/random"
    resposta = requests.get(url)
    dados = resposta.json()
    return dados['id'], dados['value']

# 2. Armazenamento no banco SQLite
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

# 3. Processamento dos dados com regex
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

# 4. Envio do relatório por email
def enviar_email():
    conn = sqlite3.connect("database/projeto_rpa.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dados_processados")
    dados = cursor.fetchall()
    conn.close()

    corpo = "Relatório Chuck Norris - Dados Processados:\n\n"
    for id, palavras in dados:
        corpo += f"ID: {id}\nPalavras longas: {palavras}\n\n"

    # Configuração do seu e-mail
    email_origem = "frazaoarthur710@gmail.com"
    senha = "dyfi ubea lquz sqqu"  # senha de app
    email_destino = "arthurgrazao@gmail.com"

    mensagem = EmailMessage()
    mensagem.set_content(corpo)
    mensagem["Subject"] = "Relatório Automatizado - Chuck Norris"
    mensagem["From"] = email_origem
    mensagem["To"] = email_destino

    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as servidor:
        servidor.login(email_origem, senha)
        servidor.send_message(mensagem)

def main():
    criar_banco()
    for _ in range(5):  # coleta e armazena 5 piadas
        id, texto = coletar_dados()
        salvar_dado(id, texto)
    processar_dados()
    enviar_email()
    print("Processo finalizado com sucesso.")

if __name__ == "__main__":
    main()
