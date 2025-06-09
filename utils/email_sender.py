import sqlite3
import smtplib
import ssl
from email.message import EmailMessage

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
    senha = "dyfi ubea lquz sqqu"
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
