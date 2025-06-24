from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class TelaPrincipal(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root_layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        root_layout.add_widget(Label(text="Painel do Provedor", font_size=32, size_hint_y=None, height=50))

        grid = GridLayout(cols=2, spacing=15, size_hint=(None, None))
        grid.bind(minimum_height=grid.setter('height'), minimum_width=grid.setter('width'))
        grid.size = (300, 200)  # largura e altura fixas

        # Categoria 1
        btn_cadastro = Button(text="Cadastrar Cliente", size_hint=(None, None), size=(140, 50), font_size=16,
                              background_color=(0.1, 0.6, 0.9, 1), background_normal='')
        btn_cadastro.bind(on_press=lambda x: setattr(self.manager, 'current', 'cadastro'))
        grid.add_widget(btn_cadastro)

        btn_clientes = Button(text="Clientes Conectados", size_hint=(None, None), size=(140, 50), font_size=16,
                             background_color=(0.1, 0.7, 0.4, 1), background_normal='')
        btn_clientes.bind(on_press=lambda x: setattr(self.manager, 'current', 'conectados'))
        grid.add_widget(btn_clientes)

        # Categoria 2
        btn_relatorios = Button(text="Relatórios", size_hint=(None, None), size=(140, 50), font_size=16,
                                background_color=(0.5, 0.5, 0.5, 1), background_normal='')
        # Aqui você pode adicionar funcionalidade ao botão relatorios
        grid.add_widget(btn_relatorios)

        btn_configuracoes = Button(text="Configurações", size_hint=(None, None), size=(140, 50), font_size=16,
                                   background_color=(0.7, 0.4, 0.1, 1), background_normal='')
        # Aqui você pode adicionar funcionalidade ao botão configurações
        grid.add_widget(btn_configuracoes)

        # Categoria 3 - sair
        btn_sair = Button(text="Sair", size_hint=(None, None), size=(300, 50), font_size=16,
                          background_color=(0.9, 0.2, 0.2, 1), background_normal='')
        btn_sair.bind(on_press=lambda x: App.get_running_app().stop())
        root_layout.add_widget(grid)
        root_layout.add_widget(btn_sair)

        self.add_widget(root_layout)

# As outras telas permanecem como antes...

class TelaCadastro(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        layout.add_widget(Label(text="Tela Cadastro", font_size=40))
        btn = Button(text="Ir para Clientes Conectados")
        btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'conectados'))
        layout.add_widget(btn)
        self.add_widget(layout)

class TelaConectados(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        layout.add_widget(Label(text="Tela Clientes Conectados", font_size=40))
        btn = Button(text="Voltar para Principal")
        btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'principal'))
        layout.add_widget(btn)
        self.add_widget(layout)

class MKAuthApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TelaPrincipal(name="principal"))
        sm.add_widget(TelaCadastro(name="cadastro"))
        sm.add_widget(TelaConectados(name="conectados"))
        return sm

if __name__ == "__main__":
    MKAuthApp().run()
