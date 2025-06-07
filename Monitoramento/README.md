# 📡 Monitoramento de Serviços

Este projeto é um script Python simples para **monitorar a disponibilidade de serviços de rede**, como DNS, servidores web e SSH. O resultado de cada verificação é salvo em um arquivo CSV com um log detalhado.

## 🚀 Funcionalidades

- Verifica conexão com serviços via IP/host e porta.
- Registra logs com:
  - Data e hora
  - Nome do serviço
  - Host
  - Porta
  - Status (UP/DOWN)
- Salva tudo em um arquivo `logs.csv`.
- Roda automaticamente a cada 60 segundos.

## 🧠 Como Funciona

O script faz uso da biblioteca `socket` para tentar abrir uma conexão com cada serviço definido. Se a conexão for bem-sucedida, o serviço é considerado "UP"; caso contrário, "DOWN".

### Exemplo da Lista de Serviços Monitorados:

```python
servicos = [
    {"nome": "Google DNS", "host": "8.8.8.8", "porta": 53},
    {"nome": "GitHub", "host": "github.com", "porta": 443},
    {"nome": "Servidor Local", "host": "192.168.0.1", "porta": 22}
]
```

## 📋 Exemplo de Log

```
DataHora,Nome,Host,Porta,Status
2025-06-07 12:00:00,Google DNS,8.8.8.8,53,UP
2025-06-07 12:00:00,GitHub,github.com,443,UP
2025-06-07 12:00:00,Servidor Local,192.168.0.1,22,DOWN
```

## 💻 Como Usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. Execute o script:
   ```bash
   python monitoramento.py
   ```

> O script rodará continuamente, fazendo verificações a cada 60 segundos.

## 🛠 Requisitos

- Python 3.x
- Permissão de escrita no diretório para gerar o `logs.csv`

## ✏️ Personalização

Você pode modificar a lista de serviços no topo do script `monitoramento.py` para monitorar o que for necessário.

---

🧠 Projeto simples e eficaz para quem precisa de uma solução leve de monitoramento local.
