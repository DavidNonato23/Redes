
import sqlite3
from backend.mikrotik_api import enviar_comando

def cadastrar_cliente(nome, usuario, senha, plano_id):
    conn = sqlite3.connect('db/banco.db')
    cursor = conn.cursor()
    cursor.execute("SELECT rate_limit FROM planos WHERE id=?", (plano_id,))
    rate = cursor.fetchone()[0]

    comando = f'/ppp secret add name={usuario} password={senha} service=pppoe profile=default comment="{nome}" rate-limit={rate}'
    enviar_comando(comando)

    cursor.execute("INSERT INTO clientes (nome, usuario, senha, plano_id) VALUES (?, ?, ?, ?)",
                   (nome, usuario, senha, plano_id))
    conn.commit()
    conn.close()
