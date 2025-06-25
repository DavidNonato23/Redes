from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from backend.mikrotik_api import enviar_comando

class TelaCadastroCliente(BoxLayout):
    def salvar_cliente(self):
        nome = self.ids.nome_input.text
        usuario = self.ids.usuario_input.text
        senha = self.ids.senha_input.text
        rate = self.ids.plano_input.text

        if not nome or not usuario or not senha or not rate:
            Popup(title="Erro", content=Label(text="Preencha todos os campos!"), size_hint=(0.6, 0.4)).open()
            return

        comando = f'/ppp secret add name={usuario} password={senha} service=pppoe profile=default comment="{nome}" rate-limit={rate}'
        resultado = enviar_comando(comando)

        Popup(title="Resultado", content=Label(text=resultado), size_hint=(0.7, 0.5)).open()
