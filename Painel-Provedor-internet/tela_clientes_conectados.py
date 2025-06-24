from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from backend.mikrotik_api import enviar_comando

class TelaClientesConectados(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        resultado = enviar_comando("/ppp active print")
        self.add_widget(Label(text="Clientes Conectados:", font_size=18))

        scroll = ScrollView()
        label = Label(text=resultado, size_hint_y=None)
        label.bind(texture_size=label.setter('size'))
        scroll.add_widget(label)
        self.add_widget(scroll)
