
import sqlite3

def cadastrar_plano(nome, velocidade, rate_limit):
    conn = sqlite3.connect('db/banco.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO planos (nome, velocidade, rate_limit) VALUES (?, ?, ?)",
                   (nome, velocidade, rate_limit))
    conn.commit()
    conn.close()
