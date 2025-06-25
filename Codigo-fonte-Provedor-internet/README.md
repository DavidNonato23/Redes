# Painel de Gerenciamento de Provedor de Internet 🚀

---

## Visão Geral do Projeto 💡

Este projeto é um **Painel de Gerenciamento de Provedor de Internet** desenvolvido em Python com a biblioteca Kivy para a interface gráfica. Ele foi criado para simplificar e automatizar diversas tarefas de um provedor, desde a gestão de clientes até a interação direta com equipamentos MikroTik.

## Tecnologias Utilizadas 🛠️

* **Python**: Linguagem de programação principal. 🐍
* **Kivy**: Framework para construção de interfaces gráficas multiplataforma. ✨
* **Git & GitHub**: Para controle de versão e hospedagem do código-fonte. 🐙
* **cx_Freeze**: Ferramenta utilizada para empacotar o aplicativo em um executável `.exe` para Windows. 📦
* **API MikroTik**: Integração para comunicação e automação com dispositivos MikroTik RouterOS. 🔌
* **JSON**: Utilizado para armazenamento de dados como backups e informações de versão. 💾
* **Requests**: Biblioteca para requisições HTTP, usada na funcionalidade de verificação de atualizações. 🌐

---

## Funcionalidades Principais ⭐

* **Interface de Usuário Intuitiva**: Desenvolvida com Kivy, oferece uma navegação fácil e responsiva. 🖥️
* **Integração com MikroTik**: Automatiza configurações e gerenciamento de rede diretamente com seus dispositivos MikroTik. ⚙️
* **Gerenciamento de Clientes Conectados**: Visão e controle em tempo real dos clientes conectados ao provedor. 🧑‍🤝‍🧑
* **Sistema de Backup Integrado**: Funcionalidade para criar e gerenciar backups importantes do sistema. 💾
* **Controle de Versão e Atualizações**: O aplicativo pode verificar e gerenciar suas próprias atualizações, garantindo que você tenha sempre a versão mais recente. ⬆️

---

## Como Rodar o Projeto (Desenvolvimento) ▶️

Se este projeto está dentro de uma pasta maior ou não possui um repositório Git próprio, você pode baixá-lo diretamente do GitHub e configurá-lo:

1.  **Baixe o Projeto:**
    * Vá para a página do repositório no GitHub onde este projeto está localizado.
    * Clique no botão verde **`<> Code`** e depois em **`Download ZIP`**.
    * Descompacte o arquivo ZIP em um local de sua preferência no computador.
    * Navegue até a pasta `Painel-Provedor-internet` (ou o nome da pasta raiz do seu projeto) dentro do conteúdo descompactado.

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    # No Windows
    venv\Scripts\activate
    # No Linux/macOS
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install kivy requests cx_Freeze
    ```

4.  **Execute o aplicativo:**
    ```bash
    python main.py
    ```

---

## Como Gerar o Executável (.exe para Windows) 📦

Para empacotar o aplicativo em um executável para Windows, utilizaremos o `cx_Freeze`.

1.  **Certifique-se de ter o `setup.py` configurado corretamente.** O `setup.py` no repositório já deve estar otimizado para o empacotamento com todas as dependências e recursos.

2.  **Limpe as pastas de build anteriores (altamente recomendado):**
    Exclua as pastas `build/`, `dist/` e todas as pastas `__pycache__/` do seu projeto.

3.  **Execute o script de build no terminal (na raiz do projeto):**
    ```bash
    python setup.py build
    ```

4.  **Localize o executável:**
    Após a conclusão do processo, seu aplicativo compilado estará na pasta `dist/SalvaCity_Painel/` (ou o nome que você definiu no `setup.py`). O executável principal será `SalvaCity_Painel.exe`.

---

## Distribuição do Executável (Via GitHub Releases) 🚀

Como o executável pode ser grande, não o versionamos diretamente no Git. Em vez disso, você pode distribuí-lo usando as **Releases do GitHub**:

1.  **Compacte a pasta do executável:** Crie um arquivo `.zip` da pasta `dist/SalvaCity_Painel`.
2.  **Crie uma nova Release no GitHub:**
    * No seu repositório GitHub, vá em **"Releases"**.
    * Clique em **"Draft a new release"**.
    * Preencha os detalhes da versão (tag, título, descrição).
    * Em "Assets", faça o upload do seu arquivo `.zip` compactado.
    * Publique a Release.

---

## Estrutura do Projeto (Códigos-Source) 📂

Abaixo está a estrutura principal dos arquivos e pastas que compõem o código-fonte deste projeto:
