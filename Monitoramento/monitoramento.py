import socket
import time
from datetime import datetime
import csv

# Lista de sites ou serviços para monitorar
servicos = [
    {"nome": "Google DNS", "host": "8.8.8.8", "porta": 53},
    {"nome": "GitHub", "host": "github.com", "porta": 443},
    {"nome": "Servidor Local", "host": "192.168.0.1", "porta": 22}
]

def testar_conexao(servico):
    try:
        socket.create_connection((servico["host"], servico["porta"]), timeout=2)
        return "UP"
    except:
        return "DOWN"

def salvar_log(dados):
    with open("logs.csv", mode="a", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(dados)

# Cabeçalho do arquivo (uma vez só)
with open("logs.csv", mode="a", newline="") as arquivo:
    escritor = csv.writer(arquivo)
    if arquivo.tell() == 0:
        escritor.writerow(["DataHora", "Nome", "Host", "Porta", "Status"])

# Laço principal (roda a cada 60 segundos)
while True:
    for servico in servicos:
        status = testar_conexao(servico)
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linha = [agora, servico["nome"], servico["host"], servico["porta"], status]
        print(linha)
        salvar_log(linha)
    time.sleep(60)
