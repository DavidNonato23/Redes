
import paramiko

def enviar_comando(comando, ip='192.168.88.1', usuario='admin', senha='admin'):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=usuario, password=senha)
        stdin, stdout, stderr = ssh.exec_command(comando)
        saida = stdout.read().decode()
        ssh.close()
        return saida
    except Exception as e:
        return f"Erro: {str(e)}"
