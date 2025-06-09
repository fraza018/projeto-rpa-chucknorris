import requests

def coletar_dados():
    url = "https://api.chucknorris.io/jokes/random"
    resposta = requests.get(url)
    dados = resposta.json()
    return dados['id'], dados['value']
