import sys
import os
from cx_Freeze import setup, Executable

# Obtenha o caminho absoluto para a pasta do seu projeto
base_dir = os.path.abspath(os.path.dirname(__file__))

# Crie a lista de arquivos e pastas de dados a serem incluídos
include_files = [
    os.path.join(base_dir, 'backend'),
    os.path.join(base_dir, 'ui'),
    os.path.join(base_dir, 'backup_salvacity.json'),
    os.path.join(base_dir, 'salvacity_version.json'),
    # ADICIONADO NOVAMENTE: tela_clientes_conectados.py pois sua imagem mostra ele na raiz
    os.path.join(base_dir, 'tela_clientes_conectados.py'),
]

# Definir as opções de compilação
build_exe_options = {
    "packages": [
        "kivy", "os", "json", "random", "webbrowser", "requests", "datetime", "sys",
        "kivy.lang", "kivy.lang.builder", "kivy.app", "kivy.uix.boxlayout",
        "kivy.uix.gridlayout", "kivy.uix.button", "kivy.uix.label",
        "kivy.uix.textinput", "kivy.uix.spinner", "kivy.uix.scrollview",
        "kivy.uix.popup", "kivy.clock", "kivy.graphics", "kivy.core.window",
        "kivy.uix.image", "kivy.core.text", "kivy.modules",
        "kivy.graphics.opengl", "kivy.graphics.texture", "kivy.vector",
    ],
    "excludes": [
        "tkinter",
        "unittest",
        "test",
        "pydoc",
        "__pycache__",
        "kivy.garden",
        "kivy.deps",
        "kivy.tools",
        "pygments",
        "docutils",
        "PIL",
    ],
    "include_files": include_files,
    "build_exe": "build/SalvaCity_Painel",
}

# Configurações específicas para o executável
icon = None

# Executável principal
executables = [
    Executable(
        "main.py",
        base="Win32GUI" if sys.platform == "win32" else None,
        icon=icon,
        target_name="SalvaCity_Painel.exe",
    )
]

# Configuração do setup
setup(
    name="SalvaCity_Painel",
    version="1.0",
    description="Painel de Gerenciamento de Provedor de Internet",
    options={"build_exe": build_exe_options},
    executables=executables,
)