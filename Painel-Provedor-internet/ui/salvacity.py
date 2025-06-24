import os
import json
import random
import webbrowser
import requests
from datetime import datetime
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock


# --- Tela Principal --- #
class TelaPrincipal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root_layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        root_layout.add_widget(Label(text="SalvaCity - Painel do Provedor", font_size=32, size_hint_y=None, height=50))

        grid = GridLayout(cols=2, spacing=15, size_hint=(None, None))
        grid.bind(minimum_height=grid.setter('height'), minimum_width=grid.setter('width'))
        grid.size = (300, 200)

        btn_cadastro = Button(text="Cadastrar Cliente", size_hint=(None, None), size=(140, 50), font_size=16,
                              background_color=(0.1, 0.6, 0.9, 1), background_normal='')
        btn_cadastro.bind(on_press=lambda x: setattr(self.manager, 'current', 'cadastro'))
        grid.add_widget(btn_cadastro)

        btn_clientes = Button(text="Clientes Conectados", size_hint=(None, None), size=(140, 50), font_size=16,
                             background_color=(0.1, 0.7, 0.4, 1), background_normal='')
        btn_clientes.bind(on_press=lambda x: self.manager.get_screen('conectados').atualizar_lista() or setattr(self.manager, 'current', 'conectados'))
        grid.add_widget(btn_clientes)

        btn_relatorios = Button(text="Relatórios", size_hint=(None, None), size=(140, 50), font_size=16,
                                background_color=(0.5, 0.5, 0.5, 1), background_normal='')
        btn_relatorios.bind(on_press=lambda x: self.manager.get_screen('relatorios').atualizar_dashboard() or setattr(self.manager, 'current', 'relatorios'))
        grid.add_widget(btn_relatorios)

        btn_configuracoes = Button(text="Configurações", size_hint=(None, None), size=(140, 50), font_size=16,
                                   background_color=(0.7, 0.4, 0.1, 1), background_normal='')
        btn_configuracoes.bind(on_press=lambda x: setattr(self.manager, 'current', 'configuracoes'))
        grid.add_widget(btn_configuracoes)

        btn_update = Button(text="Verificar Atualização", size_hint=(None, None), size=(300, 50), font_size=16,
                            background_color=(0.8, 0.5, 0.1, 1), background_normal='')
        btn_update.bind(on_press=lambda x: setattr(self.manager, 'current', 'atualizacao'))
        root_layout.add_widget(grid)
        root_layout.add_widget(btn_update)

        btn_sair = Button(text="Sair", size_hint=(None, None), size=(300, 50), font_size=16,
                          background_color=(0.9, 0.2, 0.2, 1), background_normal='')
        btn_sair.bind(on_press=lambda x: App.get_running_app().stop())
        root_layout.add_widget(btn_sair)

        self.add_widget(root_layout)


# --- Tela Cadastro --- #
class TelaCadastro(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=15)

        self.layout.add_widget(Label(text="Cadastro de Cliente", font_size=28, size_hint_y=None, height=40))

        grid_form = GridLayout(cols=2, spacing=10, size_hint_y=None)
        grid_form.bind(minimum_height=grid_form.setter('height'))

        grid_form.add_widget(Label(text="Nome:", size_hint_y=None, height=30))
        self.nome_input = TextInput(multiline=False, size_hint_y=None, height=30)
        grid_form.add_widget(self.nome_input)

        grid_form.add_widget(Label(text="Usuário PPPoE:", size_hint_y=None, height=30))
        self.usuario_input = TextInput(multiline=False, size_hint_y=None, height=30)
        grid_form.add_widget(self.usuario_input)

        grid_form.add_widget(Label(text="Senha PPPoE:", size_hint_y=None, height=30))
        self.senha_input = TextInput(password=True, multiline=False, size_hint_y=None, height=30)
        grid_form.add_widget(self.senha_input)

        grid_form.add_widget(Label(text="Plano:", size_hint_y=None, height=30))
        self.plano_spinner = Spinner(
            text='Selecione o plano',
            values=('5M/5M', '10M/10M', '20M/20M', '50M/50M', '100M/100M'),
            size_hint_y=None,
            height=30
        )
        grid_form.add_widget(self.plano_spinner)

        grid_form.add_widget(Label(text="Data de Vencimento (YYYY-MM-DD):", size_hint_y=None, height=30))
        self.data_vencimento_input = TextInput(multiline=False, size_hint_y=None, height=30, hint_text="2025-12-31")
        grid_form.add_widget(self.data_vencimento_input)

        self.layout.add_widget(grid_form)

        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=20)
        btn_salvar = Button(text="Salvar Cliente", background_color=(0.1, 0.6, 0.9, 1))
        btn_salvar.bind(on_press=self.salvar_cliente)
        btn_layout.add_widget(btn_salvar)

        btn_voltar = Button(text="Voltar", background_color=(0.5, 0.5, 0.5, 1))
        btn_voltar.bind(on_press=lambda x: setattr(self.manager, 'current', 'principal'))
        btn_layout.add_widget(btn_voltar)

        self.layout.add_widget(btn_layout)

        self.add_widget(self.layout)

    def salvar_cliente(self, instance):
        nome = self.nome_input.text.strip()
        usuario = self.usuario_input.text.strip()
        senha = self.senha_input.text.strip()
        plano = self.plano_spinner.text
        data_venc = self.data_vencimento_input.text.strip()

        if not nome or not usuario or not senha or plano == 'Selecione o plano' or not data_venc:
            self._mostrar_popup("Erro", "Preencha todos os campos corretamente!")
            return

        try:
            datetime.strptime(data_venc, "%Y-%m-%d")
        except ValueError:
            self._mostrar_popup("Erro", "Formato de data inválido! Use YYYY-MM-DD")
            return

        cliente = {
            'nome': nome,
            'usuario': usuario,
            'senha': senha,
            'plano': plano,
            'data_vencimento': data_venc,
            'bloqueado': False,
            'consumo_mb': random.randint(100, 10000)
        }

        app = App.get_running_app()
        app.clientes.append(cliente)
        app.salvar_backup()  # Salva backup após cadastro

        self._mostrar_popup("Sucesso", f"Cliente {nome} salvo!")

        self.nome_input.text = ""
        self.usuario_input.text = ""
        self.senha_input.text = ""
        self.plano_spinner.text = 'Selecione o plano'
        self.data_vencimento_input.text = ""

    def _mostrar_popup(self, titulo, mensagem):
        box = BoxLayout(orientation='vertical', padding=10)
        box.add_widget(Label(text=mensagem))
        btn = Button(text="OK", size_hint_y=None, height=40)
        box.add_widget(btn)
        popup = Popup(title=titulo, content=box, size_hint=(0.6, 0.3))
        btn.bind(on_press=popup.dismiss)
        popup.open()


# --- Tela Editar Cliente --- #
class TelaEditarCliente(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cliente_index = None
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=15)

        self.layout.add_widget(Label(text="Editar Cliente", font_size=24))
        self.layout.add_widget(Label(text="Nome:"))
        self.nome_label = Label(text="")
        self.layout.add_widget(self.nome_label)

        self.layout.add_widget(Label(text="Plano:"))
        self.plano_spinner = Spinner(values=('5M/5M', '10M/10M', '20M/20M', '50M/50M', '100M/100M'))
        self.layout.add_widget(self.plano_spinner)

        self.layout.add_widget(Label(text="Data de Vencimento (YYYY-MM-DD):"))
        self.data_vencimento_input = TextInput(multiline=False)
        self.layout.add_widget(self.data_vencimento_input)

        self.layout.add_widget(Label(text="Senha PPPoE:"))
        self.senha_input = TextInput(multiline=False, password=True)
        self.layout.add_widget(self.senha_input)

        btn_salvar = Button(text="Salvar Alterações")
        btn_salvar.bind(on_press=self.salvar)
        self.layout.add_widget(btn_salvar)

        btn_voltar = Button(text="Voltar")
        btn_voltar.bind(on_press=lambda x: setattr(self.manager, 'current', 'conectados'))
        self.layout.add_widget(btn_voltar)

        self.add_widget(self.layout)

    def carregar_dados(self, index):
        self.cliente_index = index
        app = App.get_running_app()
        cliente = app.clientes[index]
        self.nome_label.text = cliente['nome']
        self.plano_spinner.text = cliente['plano']
        self.data_vencimento_input.text = cliente['data_vencimento']
        self.senha_input.text = cliente['senha']

    def salvar(self, instance):
        app = App.get_running_app()
        cliente = app.clientes[self.cliente_index]
        cliente['plano'] = self.plano_spinner.text
        cliente['data_vencimento'] = self.data_vencimento_input.text.strip()
        cliente['senha'] = self.senha_input.text.strip()
        app.salvar_backup()  # Salva backup após editar
        self.manager.get_screen('conectados').atualizar_lista()
        self.manager.current = 'conectados'


# --- Tela Clientes Conectados --- #
class TelaConectados(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)

        layout.add_widget(Label(text="Clientes Conectados", font_size=28, size_hint_y=None, height=40))

        self.scroll = ScrollView()
        self.grid_clientes = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid_clientes.bind(minimum_height=self.grid_clientes.setter('height'))
        self.scroll.add_widget(self.grid_clientes)
        layout.add_widget(self.scroll)

        btn_voltar = Button(text="Voltar", size_hint_y=None, height=50, background_color=(0.5, 0.5, 0.5, 1))
        btn_voltar.bind(on_press=lambda x: setattr(self.manager, 'current', 'principal'))
        layout.add_widget(btn_voltar)

        self.add_widget(layout)

    def atualizar_lista(self):
        app = App.get_running_app()
        clientes = app.clientes

        hoje = datetime.today()
        self.grid_clientes.clear_widgets()

        if not clientes:
            self.grid_clientes.add_widget(Label(text="Nenhum cliente conectado.", font_size=16))
        else:
            for i, c in enumerate(clientes):
                try:
                    data_venc = datetime.strptime(c['data_vencimento'], "%Y-%m-%d")
                    c['bloqueado'] = data_venc < hoje
                except Exception:
                    c['bloqueado'] = False

                status = "[color=ff0000]Bloqueado[/color]" if c['bloqueado'] else "[color=00ff00]Ativo[/color]"
                consumo = f"Consumo: {c['consumo_mb']} MB"
                texto = f"{i + 1}. {c['nome']} - Usuário: {c['usuario']} - Plano: {c['plano']} - {status} - {consumo}"

                linha = BoxLayout(size_hint_y=None, height=30)
                lbl = Label(text=texto, markup=True)
                btn_editar = Button(text="Editar", size_hint=(None, None), size=(80, 30))
                btn_editar.bind(on_press=self.criar_callback_editar(i))
                linha.add_widget(lbl)
                linha.add_widget(btn_editar)
                self.grid_clientes.add_widget(linha)

    def criar_callback_editar(self, index):
        def callback(instance):
            tela = self.manager.get_screen('editar')
            tela.carregar_dados(index)
            self.manager.current = 'editar'
        return callback


# --- Tela Relatórios --- #
class TelaRelatorios(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        self.label_titulo = Label(text="Relatórios", font_size=28, size_hint_y=None, height=40)
        self.label_info = Label(text="(Relatórios e gráficos simples)", font_size=16)
        self.graph_box = BoxLayout(size_hint=(1, 1))

        self.btn_voltar = Button(text="Voltar", size_hint_y=None, height=50, background_color=(0.5, 0.5, 0.5, 1))
        self.btn_voltar.bind(on_press=lambda x: setattr(self.manager, 'current', 'principal'))

        self.layout.add_widget(self.label_titulo)
        self.layout.add_widget(self.label_info)
        self.layout.add_widget(self.graph_box)
        self.layout.add_widget(self.btn_voltar)
        self.add_widget(self.layout)

    def atualizar_dashboard(self):
        self.graph_box.clear_widgets()
        app = App.get_running_app()
        clientes = app.clientes

        ativos = len([c for c in clientes if not c['bloqueado']])
        bloqueados = len([c for c in clientes if c['bloqueado']])
        consumo_total = sum(c['consumo_mb'] for c in clientes)

        from kivy.uix.widget import Widget
        from kivy.graphics import Color, Rectangle

        class BarraGrafico(Widget):
            def __init__(self, categorias, valores, **kwargs):
                super().__init__(**kwargs)
                self.categorias = categorias
                self.valores = valores
                self.max_valor = max(valores) if valores else 1
                self.bind(pos=self.desenhar, size=self.desenhar)

            def desenhar(self, *args):
                self.canvas.clear()
                if self.width <= 0 or self.height <= 0:
                    return
                with self.canvas:
                    largura_barra = self.width / (len(self.categorias) * 2)
                    espacamento = largura_barra
                    x = self.x + espacamento
                    y = self.y
                    altura_max = self.height * 0.8

                    cores = [(0, 1, 0), (1, 0, 0), (0, 0, 1)]

                    for i, valor in enumerate(self.valores):
                        altura_barra = (valor / self.max_valor) * altura_max
                        Color(*cores[i % len(cores)], 1)
                        Rectangle(pos=(x, y), size=(largura_barra, altura_barra))
                        x += largura_barra + espacamento

        categorias = ['Ativos', 'Bloqueados', 'Consumo (MB)']
        valores = [ativos, bloqueados, consumo_total]

        grafico = BarraGrafico(categorias, valores)
        self.graph_box.add_widget(grafico)


# --- Tela Configurações --- #
class TelaConfiguracoes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=15)

        self.layout.add_widget(Label(text="Configurações", font_size=28, size_hint_y=None, height=50))

        # Nome do provedor
        self.layout.add_widget(Label(text="Nome do Provedor:", size_hint_y=None, height=30))
        self.nome_provedor_input = TextInput(text="", multiline=False, size_hint_y=None, height=30)
        self.layout.add_widget(self.nome_provedor_input)

        # Contato do provedor
        self.layout.add_widget(Label(text="Contato (email ou telefone):", size_hint_y=None, height=30))
        self.contato_input = TextInput(text="", multiline=False, size_hint_y=None, height=30)
        self.layout.add_widget(self.contato_input)

        # Limite de consumo mensal em MB
        self.layout.add_widget(Label(text="Limite de Consumo Mensal (MB):", size_hint_y=None, height=30))
        self.limite_input = TextInput(text="", multiline=False, input_filter='int', size_hint_y=None, height=30)
        self.layout.add_widget(self.limite_input)

        # Tema claro/escuro
        self.layout.add_widget(Label(text="Tema:", size_hint_y=None, height=30))
        self.tema_spinner = Spinner(
            text="Claro",
            values=["Claro", "Escuro"],
            size_hint_y=None,
            height=30
        )
        self.layout.add_widget(self.tema_spinner)

        # Caminho para salvar backup
        self.layout.add_widget(Label(text="Pasta para Backup:", size_hint_y=None, height=30))
        self.backup_path_input = TextInput(text="", multiline=False, size_hint_y=None, height=30)
        self.layout.add_widget(self.backup_path_input)

        btn_browse = Button(text="Escolher Pasta", size_hint_y=None, height=40)
        btn_browse.bind(on_press=self.abrir_dialogo_pasta)
        self.layout.add_widget(btn_browse)

        # Botão Restaurar Backup
        btn_restaurar = Button(text="Restaurar Backup", size_hint_y=None, height=50, background_color=(0.9, 0.4, 0.1, 1))
        btn_restaurar.bind(on_press=self.restaurar_backup)
        self.layout.add_widget(btn_restaurar)

        # Botão limpar clientes
        btn_limpar = Button(text="Limpar Clientes", size_hint_y=None, height=50, background_color=(0.9, 0.1, 0.1, 1))
        btn_limpar.bind(on_press=self.confirmar_limpar)
        self.layout.add_widget(btn_limpar)

        # Botões Salvar / Voltar
        btn_salvar = Button(text="Salvar Configurações", size_hint_y=None, height=50, background_color=(0.1, 0.6, 0.9, 1))
        btn_salvar.bind(on_press=self.salvar_configuracoes)
        self.layout.add_widget(btn_salvar)

        btn_voltar = Button(text="Voltar", size_hint_y=None, height=50, background_color=(0.5, 0.5, 0.5, 1))
        btn_voltar.bind(on_press=lambda x: setattr(self.manager, 'current', 'principal'))
        self.layout.add_widget(btn_voltar)

        self.add_widget(self.layout)

        # Carregar configurações iniciais
        Clock.schedule_once(self.carregar_configuracoes, 0.5)

    def abrir_dialogo_pasta(self, instance):
        msg = "Digite o caminho da pasta onde deseja salvar o backup, ex: C:/BackupSalvaCity"
        self._mostrar_popup("Escolher Pasta", msg)

    def confirmar_limpar(self, instance):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text="Tem certeza que deseja limpar todos os clientes?"))
        btn_sim = Button(text="Sim", background_color=(0.8, 0.1, 0.1, 1))
        btn_nao = Button(text="Não", background_color=(0.5, 0.5, 0.5, 1))
        box.add_widget(btn_sim)
        box.add_widget(btn_nao)
        popup = Popup(title="Confirmação", content=box, size_hint=(0.6, 0.4))
        btn_sim.bind(on_press=lambda x: self.limpar_clientes(popup))
        btn_nao.bind(on_press=popup.dismiss)
        popup.open()

    def limpar_clientes(self, popup):
        app = App.get_running_app()
        app.clientes.clear()
        app.salvar_backup()
        popup.dismiss()
        self._mostrar_popup("Sucesso", "Base de clientes limpa!")

    def salvar_configuracoes(self, instance):
        app = App.get_running_app()
        app.nome_provedor = self.nome_provedor_input.text.strip()
        app.contato = self.contato_input.text.strip()
        try:
            app.limite_consumo = int(self.limite_input.text)
        except ValueError:
            app.limite_consumo = 0
        app.tema = self.tema_spinner.text
        path = self.backup_path_input.text.strip()
        if path:
            app.backup_path = path
        else:
            app.backup_path = os.path.join(os.path.expanduser("~"), "SalvaCityBackup")
        self._mostrar_popup("Sucesso", "Configurações salvas!")

    def carregar_configuracoes(self, dt):
        app = App.get_running_app()
        self.nome_provedor_input.text = app.nome_provedor
        self.contato_input.text = app.contato
        self.limite_input.text = str(app.limite_consumo)
        self.tema_spinner.text = app.tema
        self.backup_path_input.text = app.backup_path

    def restaurar_backup(self, instance):
        # Abrir popup para digitar o caminho do arquivo de backup a restaurar
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text="Digite o caminho completo do arquivo de backup (.json):"))
        caminho_input = TextInput(multiline=False, size_hint_y=None, height=30)
        box.add_widget(caminho_input)
        btn_restaurar = Button(text="Restaurar", size_hint_y=None, height=40, background_color=(0.2, 0.7, 0.2, 1))
        btn_cancelar = Button(text="Cancelar", size_hint_y=None, height=40, background_color=(0.7, 0.2, 0.2, 1))
        btn_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_box.add_widget(btn_restaurar)
        btn_box.add_widget(btn_cancelar)
        box.add_widget(btn_box)

        popup = Popup(title="Restaurar Backup", content=box, size_hint=(0.7, 0.4))

        def ao_restaurar(instance):
            caminho = caminho_input.text.strip()
            if not os.path.exists(caminho):
                self._mostrar_popup("Erro", "Arquivo não encontrado!")
                return
            try:
                with open(caminho, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                if not isinstance(dados, list):
                    self._mostrar_popup("Erro", "Arquivo inválido!")
                    return
                app = App.get_running_app()
                app.clientes = dados
                app.salvar_backup()
                self._mostrar_popup("Sucesso", "Backup restaurado com sucesso!")
                popup.dismiss()
            except Exception as e:
                self._mostrar_popup("Erro", f"Erro ao restaurar backup:\n{e}")

        btn_restaurar.bind(on_press=ao_restaurar)
        btn_cancelar.bind(on_press=popup.dismiss)
        popup.open()

    def _mostrar_popup(self, titulo, mensagem):
        box = BoxLayout(orientation='vertical', padding=10)
        box.add_widget(Label(text=mensagem))
        btn = Button(text="OK", size_hint_y=None, height=40)
        box.add_widget(btn)
        popup = Popup(title=titulo, content=box, size_hint=(0.6, 0.3))
        btn.bind(on_press=popup.dismiss)
        popup.open()


# --- Tela Atualização --- #
class TelaAtualizacao(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        self.layout.add_widget(Label(text="Verificar Atualizações", font_size=32, size_hint_y=None, height=50))

        self.status_label = Label(text="Clique em 'Checar Atualização' para verificar.", font_size=18)
        self.layout.add_widget(self.status_label)

        btn_checar = Button(text="Checar Atualização", size_hint_y=None, height=50, background_color=(0.1, 0.6, 0.9, 1))
        btn_checar.bind(on_press=self.checar_atualizacao)
        self.layout.add_widget(btn_checar)

        btn_voltar = Button(text="Voltar", size_hint_y=None, height=50, background_color=(0.5, 0.5, 0.5, 1))
        btn_voltar.bind(on_press=lambda x: setattr(self.manager, 'current', 'principal'))
        self.layout.add_widget(btn_voltar)

        self.add_widget(self.layout)

    def checar_atualizacao(self, instance):
        url = "https://raw.githubusercontent.com/seuusuario/repositorio/main/salvacity_version.json"  # Altere para seu link real

        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                self._mostrar_popup("Erro", f"Erro ao acessar servidor de atualizações: {response.status_code}")
                return
            dados = response.json()
            versao_remota = dados.get("versao")
            novidades = dados.get("novidades", "")
            link_download = dados.get("link_download", "")

            app = App.get_running_app()
            versao_local = getattr(app, 'versao_app', "0.0")

            if versao_remota is None:
                self._mostrar_popup("Erro", "Arquivo de versão inválido.")
                return

            if versao_remota > versao_local:
                msg = f"Nova versão disponível: {versao_remota}\n\nNovidades:\n{novidades}"
                if link_download:
                    msg += f"\n\nClique OK para abrir a página de download."
                popup = Popup(title="Atualização Disponível",
                              content=Label(text=msg),
                              size_hint=(0.8, 0.5))
                popup.open()
                popup.bind(on_dismiss=lambda *args: webbrowser.open(link_download) if link_download else None)
                self.status_label.text = "Atualização encontrada! Veja o popup."
            else:
                self.status_label.text = "Você já está na versão mais recente."
                self._mostrar_popup("Atualização", "Seu sistema está atualizado.")

        except Exception as e:
            self._mostrar_popup("Erro", f"Erro ao verificar atualização:\n{e}")

    def _mostrar_popup(self, titulo, mensagem):
        box = BoxLayout(orientation='vertical', padding=10)
        box.add_widget(Label(text=mensagem))
        btn = Button(text="OK", size_hint_y=None, height=40)
        box.add_widget(btn)
        popup = Popup(title=titulo, content=box, size_hint=(0.6, 0.3))
        btn.bind(on_press=popup.dismiss)
        popup.open()


# --- App principal --- #
class SalvaCityApp(App):
    versao_app = "1.0"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clientes = []
        self.nome_provedor = ""
        self.contato = ""
        self.limite_consumo = 0
        self.tema = "Claro"
        self.backup_path = os.path.join(os.path.expanduser("~"), "SalvaCityBackup")

    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(TelaPrincipal(name='principal'))
        self.sm.add_widget(TelaCadastro(name='cadastro'))
        self.sm.add_widget(TelaEditarCliente(name='editar'))
        self.sm.add_widget(TelaConectados(name='conectados'))
        self.sm.add_widget(TelaRelatorios(name='relatorios'))
        self.sm.add_widget(TelaConfiguracoes(name='configuracoes'))
        self.sm.add_widget(TelaAtualizacao(name='atualizacao'))

        # Cria pasta backup se não existir
        if not os.path.exists(self.backup_path):
            os.makedirs(self.backup_path)

        # Inicia backup automático a cada 5 minutos (300 segundos)
        Clock.schedule_interval(lambda dt: self.salvar_backup(), 300)

        # Tenta carregar backup ao iniciar
        self.carregar_backup()

        return self.sm

    def salvar_backup(self):
        try:
            if not os.path.exists(self.backup_path):
                os.makedirs(self.backup_path)
            backup_file = os.path.join(self.backup_path, "backup_clientes.json")
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(self.clientes, f, indent=4, ensure_ascii=False)
            print(f"Backup salvo em: {backup_file} às {datetime.now()}")
        except Exception as e:
            print(f"Erro ao salvar backup: {e}")

    def carregar_backup(self, caminho=None):
        try:
            if caminho is None:
                caminho = os.path.join(self.backup_path, "backup_clientes.json")
            if os.path.exists(caminho):
                with open(caminho, 'r', encoding='utf-8') as f:
                    self.clientes = json.load(f)
                print(f"Backup carregado de: {caminho}")
            else:
                print("Arquivo de backup não encontrado.")
        except Exception as e:
            print(f"Erro ao carregar backup: {e}")


if __name__ == "__main__":
    SalvaCityApp().run()
