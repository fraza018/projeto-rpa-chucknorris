from utils.coleta import coletar_dados
from utils.banco import criar_banco, salvar_dado
from utils.processamento import processar_dados
from utils.email_sender import enviar_email

if __name__ == "__main__":
    criar_banco()
    for _ in range(5):
        id, texto = coletar_dados()
        salvar_dado(id, texto)
    processar_dados()
    enviar_email()
