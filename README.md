# 🚦 Monitoramento de Serviços de Rede com Python

## 📋 Sobre o Projeto

Este projeto foi desenvolvido como parte do meu portfólio para demonstrar habilidades práticas em monitoramento de infraestrutura e automação utilizando Python. Ele realiza a verificação periódica da disponibilidade de serviços de rede, registrando os resultados em um arquivo CSV para análise posterior.

---

## 🛠️ Tecnologias e Conceitos Aplicados

- 🐍 Python 3 (bibliotecas padrão: `socket`, `csv`, `datetime`, `time`)  
- 🌐 Monitoramento de serviços TCP/IP (ex: DNS, HTTP, SSH)  
- 🤖 Automação de tarefas e agendamento de processos com loops e delays  
- 📊 Registro e persistência de dados para análise histórica  
- 🔌 Conceitos de redes: IP, portas, protocolos TCP/UDP  

---

## ⚙️ Funcionalidades

- 🔄 Monitoramento contínuo da disponibilidade de hosts e portas configuradas  
- 📝 Registro dos status (`UP`/`DOWN`) com timestamp em arquivo CSV  
- ⚙️ Estrutura simples e facilmente configurável para adicionar novos serviços  
- 🚀 Código enxuto, ideal para profissionais iniciantes e intermediários em TI  

---

## ▶️ Como Executar

1. ✅ Tenha o Python 3 instalado em seu ambiente.  
2. 📥 Clone este repositório ou faça o download dos arquivos.  
3. ✍️ Abra o arquivo `monitoramento.py` e ajuste a lista `servicos` para os serviços que deseja monitorar.  
4. 💻 No terminal, execute o comando:

```bash
python monitoramento.py
