import os
import json
import random
import webbrowser
import requests 
from datetime import datetime, timedelta
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
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import AsyncImage

# --- Configuração da Imagem de Fundo (Global) ---
WEB_BACKGROUND_IMAGE_URL = 'https://a3aengenharia.com.br/wp-content/uploads/2024/08/tipos-de-redes-2.jpeg'

# --- Mixin para Adicionar Fundo ---
class BackgroundScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.15, 0.15, 0.15, 1) # Cinza escuro
            self.rect_fallback = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect_fallback, pos=self._update_rect_fallback)

        self.bg_image_widget = AsyncImage(
            source=WEB_BACKGROUND_IMAGE_URL,
            pos=self.pos,
            size=self.size,
            allow_stretch=True, 
            keep_ratio=False    
        )
        super().add_widget(self.bg_image_widget, index=0) 
        self.bind(size=self._update_bg_image_widget, pos=self._update_bg_image_widget)

        self.content_area = BoxLayout(orientation='vertical')
        super().add_widget(self.content_area) 
        self.bind(size=self._update_content_area, pos=self._update_content_area) 


    def _update_bg_image_widget(self, instance, value):
        if self.bg_image_widget:
            self.bg_image_widget.pos = instance.pos
            self.bg_image_widget.size = instance.size

    def _update_content_area(self, instance, value):
        if self.content_area:
            self.content_area.pos = instance.pos
            self.content_area.size = instance.size

    def _update_rect_fallback(self, instance, value):
        self.rect_fallback.pos = instance.pos
        self.rect_fallback.size = instance.size


# --- Tela Principal --- #
class TelaPrincipal(BackgroundScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        root_layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        root_layout.add_widget(Label(
            text="David Nonato\nPainel do Provedor",
            font_size=56,
            bold=True,
            color=(1,1,1,1),
            size_hint_y=None,
            height=120,
            halign='center',
            valign='middle'
        ))

        grid = GridLayout(cols=2, spacing=15, size_hint=(None, None))
        grid.bind(minimum_height=grid.setter('height'), minimum_width=grid.setter('width'))
        grid.size = (300, 200)

        btn_cadastro = Button(text="Cadastrar Cliente", size_hint=(None, None), size=(140, 50), font_size=16,
                              background_color=(0.1, 0.6, 0.9, 1), background_normal='')
        btn_cadastro.bind(on_press=lambda x: self.manager.get_screen('cadastro').pre_preencher_data() or setattr(self.manager, 'current', 'cadastro'))
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

        self.content_area.add_widget(root_layout)


# --- Tela Cadastro --- #
class TelaCadastro(BackgroundScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=15)

        self.layout.add_widget(Label(text="Cadastro de Cliente", font_size=28, size_hint_y=None, height=40, color=(1,1,1,1)))

        grid_form = GridLayout(cols=2, spacing=10, size_hint_y=None)
        grid_form.bind(minimum_height=grid_form.setter('height'))

        grid_form.add_widget(Label(text="Nome:", size_hint_y=None, height=30, color=(1,1,1,1)))
        self.nome_input = TextInput(multiline=False, size_hint_y=None, height=30)
        grid_form.add_widget(self.nome_input)

        grid_form.add_widget(Label(text="Usuário PPPoE:", size_hint_y=None, height=30, color=(1,1,1,1)))
        self.usuario_input = TextInput(multiline=False, size_hint_y=None, height=30)
        grid_form.add_widget(self.usuario_input)

        grid_form.add_widget(Label(text="Senha PPPoE:", size_hint_y=None, height=30, color=(1,1,1,1)))
        self.senha_input = TextInput(password=True, multiline=False, size_hint_y=None, height=30)
        grid_form.add_widget(self.senha_input)

        grid_form.add_widget(Label(text="Plano:", size_hint_y=None, height=30, color=(1,1,1,1)))
        self.plano_spinner = Spinner(
            text='Selecione o plano',
            values=('5M/5M', '10M/10M', '20M/20M', '50M/50M', '100M/100M'),
            size_hint_y=None,
            height=30
        )
        grid_form.add_widget(self.plano_spinner)

        grid_form.add_widget(Label(text="Data de Vencimento (YYYY-MM-DD):", size_hint_y=None, height=30, color=(1,1,1,1)))
        self.data_vencimento_input = TextInput(multiline=False, size_hint_y=None, height=30)
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

        self.content_area.add_widget(self.layout)

    def pre_preencher_data(self):
        hoje = datetime.today().strftime("%Y-%m-%d")
        self.data_vencimento_input.text = hoje

    def salvar_cliente(self, instance):
        nome = self.nome_input.text.strip()
        usuario = self.usuario_input.text.strip()
        senha = self.senha_input.text.strip()
        plano = self.plano_spinner.text
        data_venc_str = self.data_vencimento_input.text.strip()

        if not nome or not usuario or not senha or plano == 'Selecione o plano' or not data_venc_str:
            self._mostrar_popup("Erro", "Preencha todos os campos corretamente!")
            return

        try:
            datetime.strptime(data_venc_str, "%Y-%m-%d")
        except ValueError:
            self._mostrar_popup("Erro", "Formato de data inválido! UseYYYY-MM-DD")
            return

        cliente = {
            'nome': nome,
            'usuario': usuario,
            'senha': senha,
            'plano': plano,
            'data_vencimento': data_venc_str,
            'bloqueado': False,
            'consumo_mb': random.randint(100, 10000)
        }

        app = App.get_running_app()
        app.clientes.append(cliente)
        app.salvar_backup()

        self._mostrar_popup("Sucesso", f"Cliente {nome} salvo!")

        self.nome_input.text = ""
        self.usuario_input.text = ""
        self.senha_input.text = ""
        self.plano_spinner.text = 'Selecione o plano'
        self.data_vencimento_input.text = ""
        self.pre_preencher_data()


    def _mostrar_popup(self, titulo, mensagem):
        box = BoxLayout(orientation='vertical', padding=10)
        box.add_widget(Label(text=mensagem))
        btn = Button(text="OK", size_hint_y=None, height=40)
        box.add_widget(btn)
        popup = Popup(title=titulo, content=box, size_hint=(0.6, 0.3))
        btn.bind(on_press=popup.dismiss)
        popup.open()


# --- Tela Editar Cliente --- #
class TelaEditarCliente(BackgroundScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cliente_index = None
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=15)

        self.layout.add_widget(Label(text="Editar Cliente", font_size=24, color=(1,1,1,1)))
        self.layout.add_widget(Label(text="Nome:", color=(1,1,1,1)))
        self.nome_label = Label(text="", color=(1,1,1,1))
        self.layout.add_widget(self.nome_label)

        self.layout.add_widget(Label(text="Plano:", color=(1,1,1,1)))
        self.plano_spinner = Spinner(values=('5M/5M', '10M/10M', '20M/20M', '50M/50M', '100M/100M'))
        self.layout.add_widget(self.plano_spinner)

        self.layout.add_widget(Label(text="Data de Vencimento (YYYY-MM-DD):", color=(1,1,1,1)))
        self.data_vencimento_input = TextInput(multiline=False)
        self.layout.add_widget(self.data_vencimento_input)

        self.layout.add_widget(Label(text="Senha PPPoE:", color=(1,1,1,1)))
        self.senha_input = TextInput(multiline=False, password=True)
        self.layout.add_widget(self.senha_input)
        
        self.layout.add_widget(Label(text="Status de Bloqueio:", color=(1,1,1,1)))
        self.bloqueado_spinner = Spinner(
            text="Ativo",
            values=["Ativo", "Bloqueado"],
            size_hint_y=None,
            height=30
        )
        self.layout.add_widget(self.bloqueado_spinner)


        btn_salvar = Button(text="Salvar Alterações")
        btn_salvar.bind(on_press=self.salvar)
        self.layout.add_widget(btn_salvar)

        btn_voltar = Button(text="Voltar")
        btn_voltar.bind(on_press=lambda x: setattr(self.manager, 'current', 'conectados'))
        self.layout.add_widget(btn_voltar)

        self.content_area.add_widget(self.layout)

    def carregar_dados(self, index):
        self.cliente_index = index
        app = App.get_running_app()
        cliente = app.clientes[index]
        self.nome_label.text = cliente['nome']
        self.plano_spinner.text = cliente['plano']
        self.data_vencimento_input.text = cliente['data_vencimento']
        self.senha_input.text = cliente['senha']
        self.bloqueado_spinner.text = "Bloqueado" if bool(cliente.get('bloqueado', False)) else "Ativo"


    def salvar(self, instance):
        app = App.get_running_app()
        cliente = app.clientes[self.cliente_index]
        cliente['plano'] = self.plano_spinner.text
        cliente['data_vencimento'] = self.data_vencimento_input.text.strip()
        cliente['senha'] = self.senha_input.text.strip()
        cliente['bloqueado'] = True if self.bloqueado_spinner.text == "Bloqueado" else False
        app.salvar_backup()
        self.manager.get_screen('conectados').atualizar_lista()
        self.manager.current = 'conectados'


# --- Tela Clientes Conectados --- #
class TelaConectados(BackgroundScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)

        layout.add_widget(Label(text="Clientes Conectados", font_size=28, size_hint_y=None, height=40, color=(1,1,1,1)))

        self.scroll = ScrollView()
        self.grid_clientes = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid_clientes.bind(minimum_height=self.grid_clientes.setter('height'))
        self.scroll.add_widget(self.grid_clientes)
        layout.add_widget(self.scroll)

        btn_voltar = Button(text="Voltar", size_hint_y=None, height=50, background_color=(0.5, 0.5, 0.5, 1))
        btn_voltar.bind(on_press=lambda x: setattr(self.manager, 'current', 'principal'))
        layout.add_widget(btn_voltar)

        self.content_area.add_widget(layout)

    def atualizar_lista(self):
        app = App.get_running_app()
        clientes = app.clientes

        hoje = datetime.today()
        self.grid_clientes.clear_widgets()

        if not clientes:
            self.grid_clientes.add_widget(Label(text="Nenhum cliente conectado.", font_size=16, color=(1,1,1,1)))
        else:
            for i, c in enumerate(clientes):
                c['bloqueado'] = bool(c.get('bloqueado', False))

                bloqueio_manual = c['bloqueado']
                bloqueio_vencimento = False
                try:
                    data_venc = datetime.strptime(c['data_vencimento'], "%Y-%m-%d")
                    bloqueio_vencimento = data_venc < hoje
                except Exception:
                    pass

                cliente_bloqueado = bloqueio_manual or bloqueio_vencimento

                status_display = "[color=ff0000]Bloqueado[/color]" if cliente_bloqueado else "[color=00ff00]Ativo[/color]"
                consumo = f"Consumo: {c['consumo_mb']} MB"
                texto = f"{i + 1}. {c['nome']} - Usuário: {c['usuario']} - Plano: {c['plano']} - {status_display} - {consumo}"
                
                linha = BoxLayout(size_hint_y=None, height=50, spacing=5)
                lbl = Label(text=texto, markup=True, size_hint_x=0.7, color=(1,1,1,1))
                
                btn_editar = Button(text="Editar", size_hint=(None, None), size=(80, 40), font_size=12)
                btn_editar.bind(on_press=self.criar_callback_editar(i))
                
                btn_toggle_bloqueio = Button(
                    text="Desbloquear" if bloqueio_manual else "Bloquear",
                    size_hint=(None, None),
                    size=(100, 40),
                    font_size=12,
                    background_color=(0.2, 0.7, 0.2, 1) if bloqueio_manual else (0.9, 0.2, 0.2, 1)
                )
                btn_toggle_bloqueio.bind(on_press=self.criar_callback_toggle_bloqueio(i))

                linha.add_widget(lbl)
                linha.add_widget(btn_editar)
                linha.add_widget(btn_toggle_bloqueio)
                self.grid_clientes.add_widget(linha)

    def criar_callback_editar(self, index):
        def callback(instance):
            tela = self.manager.get_screen('editar')
            tela.carregar_dados(index)
            self.manager.current = 'editar'
        return callback

    def criar_callback_toggle_bloqueio(self, index):
        def callback(instance):
            app = App.get_running_app()
            
            if index < 0 or index >= len(app.clientes):
                self._mostrar_popup("Erro", "Cliente não encontrado para esta ação.")
                return

            cliente = app.clientes[index]
            cliente['bloqueado'] = not bool(cliente.get('bloqueado', False))
            
            try:
                app.salvar_backup()
            except Exception as e:
                self._mostrar_popup("Erro", f"Falha ao salvar o estado do cliente: {e}")

            Clock.schedule_once(lambda dt: self.atualizar_lista(), 0)
            
            status_acao = "Bloqueado" if cliente['bloqueado'] else "Desbloqueado"
            self._mostrar_popup("Ação Concluída", f"Cliente {cliente['nome']} foi {status_acao} manualmente.")

        return callback
        
    def _mostrar_popup(self, titulo, mensagem):
        box = BoxLayout(orientation='vertical', padding=10)
        box.add_widget(Label(text=mensagem))
        btn = Button(text="OK", size_hint_y=None, height=40)
        box.add_widget(btn)
        popup = Popup(title=titulo, content=box, size_hint=(0.6, 0.3))
        btn.bind(on_press=popup.dismiss)
        popup.open()


# --- Tela Relatórios --- #
class TelaRelatorios(BackgroundScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        self.label_titulo = Label(text="Relatórios do Provedor", font_size=32, size_hint_y=None, height=60, color=(1,1,1,1), bold=True)
        self.label_info = Label(text="Visão geral de clientes e consumo (Atualiza a cada 5s)", font_size=16, color=(0.8,0.8,0.8,1))
        self.graph_box = BoxLayout(size_hint=(1, 1)) 

        self.btn_voltar = Button(text="Voltar", size_hint_y=None, height=50, background_color=(0.5, 0.5, 0.5, 1))
        self.btn_voltar.bind(on_press=lambda x: setattr(self.manager, 'current', 'principal'))

        self.layout.add_widget(self.label_titulo)
        self.layout.add_widget(self.label_info)
        self.layout.add_widget(self.graph_box)
        self.layout.add_widget(self.btn_voltar)
        self.content_area.add_widget(self.layout)

        self.update_event = None 

    def on_enter(self, *args):
        self.atualizar_dashboard() 
        self.update_event = Clock.schedule_interval(self.atualizar_dashboard, 5) 

    def on_leave(self, *args):
        if self.update_event:
            self.update_event.cancel()
            self.update_event = None 

    def atualizar_dashboard(self, dt=0): 
        self.graph_box.clear_widgets() 
        app = App.get_running_app()
        clientes = app.clientes

        ativos = len([c for c in clientes if not c.get('bloqueado', False)])
        bloqueados = len([c for c in clientes if c.get('bloqueado', False)])
        total_consumo_mb = sum(c['consumo_mb'] for c in clientes)

        if total_consumo_mb >= 1024: 
            consumo_display = f"{total_consumo_mb / 1024:.2f} GB"
            consumo_valor_para_grafico = total_consumo_mb / 1024 
        else:
            consumo_display = f"{total_consumo_mb} MB"
            consumo_valor_para_grafico = total_consumo_mb 

        class BarraGrafico(Widget):
            def __init__(self, categorias, valores_grafico, valores_display, **kwargs):
                super().__init__(**kwargs)
                self.categorias = categorias
                self.valores_grafico = valores_grafico 
                self.valores_display = valores_display 
                self.max_valor = max(valores_grafico) if valores_grafico else 1 
                self.bind(pos=self.draw_chart, size=self.draw_chart)

            def draw_chart(self, *args):
                self.canvas.clear()
                for child in list(self.children):
                    if isinstance(child, Label):
                        self.remove_widget(child)

                if self.width <= 0 or self.height <= 0:
                    return

                bar_count = len(self.categorias)
                if bar_count == 0:
                    return

                padding_x = 40  
                padding_y = 60  
                
                chart_width = self.width - 2 * padding_x
                chart_height = self.height - 2 * padding_y

                bar_spacing_ratio = 0.4 
                bar_width_calc = chart_width / (bar_count + bar_count * bar_spacing_ratio - bar_spacing_ratio)
                bar_spacing = bar_width_calc * bar_spacing_ratio

                x_start_chart = self.x + padding_x
                y_start_chart = self.y + padding_y 

                colors = [
                    (0.2, 0.7, 0.2, 1), 
                    (0.9, 0.3, 0.3, 1), 
                    (0.1, 0.5, 0.9, 1)  
                ]

                with self.canvas:
                    Color(0.2, 0.2, 0.2, 0.5) 
                    Rectangle(pos=(x_start_chart - bar_spacing/2, y_start_chart - 30), 
                              size=(chart_width + bar_spacing, chart_height + 30 + 30)) 

                    current_x = x_start_chart + bar_spacing / 2 

                    for i in range(bar_count):
                        valor_grafico = self.valores_grafico[i]
                        valor_display = self.valores_display[i]

                        bar_height = (valor_grafico / self.max_valor) * chart_height

                        Color(*colors[i % len(colors)])
                        Rectangle(pos=(current_x, y_start_chart), size=(bar_width_calc, bar_height))

                        value_label = Label(
                            text=valor_display, 
                            pos=(current_x + bar_width_calc / 2, y_start_chart + bar_height + 5),
                            size_hint=(None, None),
                            size=(bar_width_calc, 20),
                            halign='center',
                            valign='bottom',
                            color=(1, 1, 1, 1), 
                            font_size='12sp'
                        )
                        if value_label.top > self.height - 20: 
                            value_label.pos = (current_x + bar_width_calc / 2, y_start_chart + bar_height - 25) 
                        self.add_widget(value_label)

                        category_label = Label(
                            text=self.categorias[i],
                            pos=(current_x + bar_width_calc / 2, y_start_chart - 30), 
                            size_hint=(None, None),
                            size=(bar_width_calc, 20),
                            halign='center',
                            valign='top',
                            color=(1, 1, 1, 1), 
                            font_size='12sp'
                        )
                        self.add_widget(category_label)

                        current_x += bar_width_calc + bar_spacing 

        categorias = ['Ativos', 'Bloqueados', 'Consumo'] 
        valores_grafico = [ativos, bloqueados, consumo_valor_para_grafico] 
        valores_display = [str(ativos), str(bloqueados), consumo_display] 

        grafico = BarraGrafico(categorias, valores_grafico, valores_display)
        self.graph_box.add_widget(grafico)


# --- Tela Configurações --- #
class TelaConfiguracoes(BackgroundScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=15)

        self.layout.add_widget(Label(text="Configurações", font_size=28, size_hint_y=None, height=50, color=(1,1,1,1)))

        self.layout.add_widget(Label(text="Nome do Provedor:", size_hint_y=None, height=30, color=(1,1,1,1)))
        self.nome_provedor_input = TextInput(text="", multiline=False, size_hint_y=None, height=30)
        self.layout.add_widget(self.nome_provedor_input)

        self.layout.add_widget(Label(text="Contato (email ou telefone):", size_hint_y=None, height=30, color=(1,1,1,1)))
        self.contato_input = TextInput(text="", multiline=False, size_hint_y=None, height=30)
        self.layout.add_widget(self.contato_input)

        self.layout.add_widget(Label(text="Limite de Consumo Mensal (MB):", size_hint_y=None, height=30, color=(1,1,1,1)))
        self.limite_input = TextInput(text="", multiline=False, input_filter='int', size_hint_y=None, height=30)
        self.layout.add_widget(self.limite_input)

        self.layout.add_widget(Label(text="Tema:", size_hint_y=None, height=30, color=(1,1,1,1)))
        self.tema_spinner = Spinner(
            text="Claro",
            values=["Claro", "Escuro"],
            size_hint_y=None,
            height=30
        )
        self.layout.add_widget(self.tema_spinner)

        self.layout.add_widget(Label(text="Pasta para Backup:", size_hint_y=None, height=30, color=(1,1,1,1)))
        self.backup_path_input = TextInput(text="", multiline=False, size_hint_y=None, height=30)
        self.layout.add_widget(self.backup_path_input)

        btn_browse = Button(text="Escolher Pasta", size_hint_y=None, height=40)
        btn_browse.bind(on_press=self.abrir_dialogo_pasta)
        self.layout.add_widget(btn_browse)

        btn_restaurar = Button(text="Restaurar Backup", size_hint_y=None, height=50, background_color=(0.9, 0.4, 0.1, 1))
        btn_restaurar.bind(on_press=self.restaurar_backup)
        self.layout.add_widget(btn_restaurar)

        btn_limpar = Button(text="Limpar Clientes", size_hint_y=None, height=50, background_color=(0.9, 0.1, 0.1, 1))
        btn_limpar.bind(on_press=self.confirmar_limpar)
        self.layout.add_widget(btn_limpar)

        btn_salvar = Button(text="Salvar Configurações", size_hint_y=None, height=50, background_color=(0.1, 0.6, 0.9, 1))
        btn_salvar.bind(on_press=self.salvar_configuracoes)
        self.layout.add_widget(btn_salvar)

        btn_voltar = Button(text="Voltar", size_hint_y=None, height=50, background_color=(0.5, 0.5, 0.5, 1))
        btn_voltar.bind(on_press=lambda x: setattr(self.manager, 'current', 'principal'))
        self.layout.add_widget(btn_voltar)

        self.content_area.add_widget(self.layout)

        Clock.schedule_once(self.carregar_configuracoes, 0.5)

    def abrir_dialogo_pasta(self, instance):
        msg = "Digite o caminho da pasta onde deseja salvar o backup, ex: C:/BackupSalvaCity"
        self._mostrar_popup("Escolher Pasta", msg)

    def confirmar_limpar(self, instance):
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text="Tem certeza que deseja limpar todos os clientes?", color=(1,1,1,1)))
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
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text="Digite o caminho completo do arquivo de backup (.json):", color=(1,1,1,1)))
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
class TelaAtualizacao(BackgroundScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        self.layout.add_widget(Label(text="Verificar Atualizações", font_size=32, size_hint_y=None, height=50, color=(1,1,1,1)))

        self.status_label = Label(text="Clique em 'Checar Atualização' para verificar.", font_size=18, color=(1,1,1,1))
        self.layout.add_widget(self.status_label)

        btn_checar = Button(text="Checar Atualização", size_hint_y=None, height=50, background_color=(0.1, 0.6, 0.9, 1))
        btn_checar.bind(on_press=self.checar_atualizacao)
        self.layout.add_widget(btn_checar)

        btn_voltar = Button(text="Voltar", size_hint_y=None, height=50, background_color=(0.5, 0.5, 0.5, 1))
        btn_voltar.bind(on_press=lambda x: setattr(self.manager, 'current', 'principal'))
        self.layout.add_widget(btn_voltar)

        self.content_area.add_widget(self.layout)

    def checar_atualizacao(self, instance):
        # URL do arquivo JSON no seu GitHub
        url = "https://raw.githubusercontent.com/DavidNonato23/Redes/DavidNonato23/Aulas/Painel-Provedor-internet/salvacity_version.json" 

        try:
            response = requests.get(url, timeout=5)
            
            if response.status_code != 200:
                self._mostrar_popup("Erro", f"Erro ao acessar servidor de atualizações: {response.status_code}. Verifique a URL do GitHub ou sua conexão.")
                return
            
            dados = response.json()
            # Espera a nova estrutura com a lista de versões disponíveis
            available_versions = dados.get("available_versions", []) 
            
            app = App.get_running_app()
            versao_local = getattr(app, 'versao_app', "0.0")

            newer_versions = []
            for v_info in available_versions:
                remote_version = v_info.get("versao")
                # Compara as versões como strings para garantir que "1.10" é maior que "1.9"
                if remote_version and self._compare_versions(remote_version, versao_local) > 0:
                    newer_versions.append(v_info)
            
            if not newer_versions:
                self.status_label.text = f"Seu sistema está atualizado (v{versao_local})."
                self._mostrar_popup("Atualização", f"Seu sistema já está na versão mais recente (v{versao_local}).")
            else:
                self.status_label.text = f"Atualizações encontradas! Veja o popup para escolher."
                self._mostrar_update_selection_popup(newer_versions)

        except requests.exceptions.RequestException as e:
            self._mostrar_popup("Erro de Conexão", f"Não foi possível conectar ao GitHub. Verifique sua internet ou a URL:\n{e}")
            self.status_label.text = "Erro: Sem conexão ou URL inválida."
        except json.JSONDecodeError:
            self._mostrar_popup("Erro de Formato", "O arquivo de versão no GitHub não está no formato JSON correto ou a estrutura esperada está ausente.")
            self.status_label.text = "Erro: Formato de arquivo de versão inválido."
        except Exception as e:
            self._mostrar_popup("Erro Inesperado", f"Ocorreu um erro ao verificar a atualização:\n{e}")
            self.status_label.text = "Erro: Tente novamente mais tarde."

    def _compare_versions(self, ver1, ver2):
        """Compara duas strings de versão (ex: '1.0', '1.10', '2.0').
           Retorna >0 se ver1 é maior, <0 se ver2 é maior, 0 se iguais."""
        parts1 = [int(p) for p in ver1.split('.')]
        parts2 = [int(p) for p in ver2.split('.')]
        
        for i in range(max(len(parts1), len(parts2))):
            p1 = parts1[i] if i < len(parts1) else 0
            p2 = parts2[i] if i < len(parts2) else 0
            if p1 > p2:
                return 1
            if p1 < p2:
                return -1
        return 0

    def _mostrar_update_selection_popup(self, versions):
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_content.add_widget(Label(text="Escolha uma atualização disponível:", size_hint_y=None, height=40, color=(1,1,1,1)))

        scroll_view = ScrollView(size_hint_y=1)
        version_list_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        version_list_layout.bind(minimum_height=version_list_layout.setter('height'))

        # Ordena as versões da mais nova para a mais antiga
        # Usa a função _compare_versions para uma ordenação correta de strings de versão
        versions.sort(key=lambda x: x.get('versao', '0.0'), reverse=True)

        for v_info in versions:
            versao = v_info.get("versao", "N/A")
            novidades = v_info.get("novidades", "Sem descrição.")
            link_download = v_info.get("link_download", "")
            release_date = v_info.get("release_date", "Data desconhecida")

            btn_text = f"[b]Versão {versao}[/b] (Lançamento: {release_date})\n[size=14]{novidades}[/size]"
            
            update_button = Button(
                text=btn_text,
                size_hint_y=None,
                height=90, # Aumentei a altura para mais texto
                text_size=(self.width * 0.7, None), # Ajusta a quebra de linha do texto no botão
                halign='left',
                valign='middle',
                markup=True, # Permite formatação de texto (bold, size)
                background_color=(0.1, 0.7, 0.4, 1), # Cor verde para as atualizações
                background_normal='' # Remove o fundo padrão do botão
            )
            # Adiciona um pequeno padding ao texto do botão para não ficar colado
            update_button.padding = [10, 10]

            update_button.bind(on_press=lambda btn, link=link_download: self._open_download_link(link))
            version_list_layout.add_widget(update_button)
        
        scroll_view.add_widget(version_list_layout)
        popup_content.add_widget(scroll_view)

        btn_close = Button(text="Fechar", size_hint_y=None, height=40, background_color=(0.7, 0.7, 0.7, 1))
        popup_content.add_widget(btn_close)

        self.update_popup = Popup(
            title="Atualizações Disponíveis", 
            content=popup_content, 
            size_hint=(0.9, 0.9) # Aumentei o tamanho do popup para melhor visualização
        )
        btn_close.bind(on_press=self.update_popup.dismiss)
        self.update_popup.open()

    def _open_download_link(self, link):
        if link:
            webbrowser.open(link)
            self._mostrar_popup("Download Iniciado", "A página de download foi aberta no seu navegador. O download pode começar automaticamente ou você precisará clicar para baixar.")
        else:
            self._mostrar_popup("Erro", "Link de download não disponível para esta versão.")
        if hasattr(self, 'update_popup') and self.update_popup:
            self.update_popup.dismiss()

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
    versao_app = "1.0" # Defina aqui a versão atual do seu aplicativo

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clientes = []
        self.nome_provedor = "David Nonato" 
        self.contato = ""
        self.limite_consumo = 0
        self.tema = "Claro"
        self.backup_path = os.path.join(os.path.expanduser("~"), "SalvaCityBackup")

    def build(self):
        Window.clearcolor = (0.15, 0.15, 0.15, 1)

        self.sm = ScreenManager()
        self.sm.add_widget(TelaPrincipal(name='principal'))
        self.sm.add_widget(TelaCadastro(name='cadastro'))
        self.sm.add_widget(TelaEditarCliente(name='editar'))
        self.sm.add_widget(TelaConectados(name='conectados'))
        self.sm.add_widget(TelaRelatorios(name='relatorios'))
        self.sm.add_widget(TelaConfiguracoes(name='configuracoes'))
        self.sm.add_widget(TelaAtualizacao(name='atualizacao'))

        if not os.path.exists(self.backup_path):
            os.makedirs(self.backup_path)

        # Salva o backup a cada 5 minutos (300 segundos)
        Clock.schedule_interval(lambda dt: self.salvar_backup(), 300)

        self.carregar_backup()

        return self.sm

    def salvar_backup(self):
        try:
            if not os.path.exists(self.backup_path):
                os.makedirs(self.backup_path)

            backup_file = os.path.join(self.backup_path, "backup_clientes.json")
            with open(backup_file, 'w', encoding='utf-8') as f:
                json_content = json.dumps(self.clientes, indent=4, ensure_ascii=False)
                f.write(json_content)
            # print(f"Backup salvo em: {backup_file}") # Descomente para depurar
        except Exception as e:
            print(f"ERRO CRÍTICO ao salvar backup: {e}")

    def carregar_backup(self, caminho=None):
        try:
            if caminho is None:
                caminho = os.path.join(self.backup_path, "backup_clientes.json")
            if os.path.exists(caminho):
                with open(caminho, 'r', encoding='utf-8') as f:
                    json_content = f.read()
                    self.clientes = json.loads(json_content)
                for cliente in self.clientes:
                    # Garante que 'bloqueado' é um booleano, importante para a lógica
                    cliente['bloqueado'] = bool(cliente.get('bloqueado', False))
            else:
                # print("Arquivo de backup não encontrado, iniciando com lista vazia.") # Descomente para depurar
                pass 
        except json.JSONDecodeError as e:
            print(f"ERRO: Arquivo de backup corrompido em {caminho}: {e}. Iniciando com lista vazia.")
            self.clientes = []
        except Exception as e:
            print(f"ERRO ao carregar backup de {caminho}: {e}. Iniciando com lista vazia.")
            self.clientes = []


if __name__ == "__main__":
    SalvaCityApp().run()