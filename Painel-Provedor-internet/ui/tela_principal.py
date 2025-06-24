
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class TelaPrincipal(BoxLayout):
    def cadastrar_cliente(self):
        popup = Popup(title='Cadastro', content=Label(text='Função em construção'), size_hint=(0.6, 0.4))
        popup.open()

    def listar_clientes(self):
        popup = Popup(title='Clientes', content=Label(text='Função em construção'), size_hint=(0.6, 0.4))
        popup.open()

    def gerenciar_planos(self):
        popup = Popup(title='Planos', content=Label(text='Função em construção'), size_hint=(0.6, 0.4))
        popup.open()
