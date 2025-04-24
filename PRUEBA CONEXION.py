import paramiko
import os

# Configuración de rutas
log_dir = "logs_prueba"
os.makedirs(log_dir, exist_ok=True)

# Leer lista de servidores
with open('servers.txt', 'r') as f:
    servidores = [line.strip().split(',') for line in f.readlines()]

print("===== INICIANDO PRUEBA DE CONEXIÓN Y SUDO =====")

for ssh_user, ssh_host, ssh_pass in servidores:
    print(f"\n=========================================")
    print(f"Conectando a {ssh_host} como {ssh_user}...")

    log_path = os.path.join(log_dir, f"{ssh_host.replace('.', '_')}_prueba.log")
    with open(log_path, "w") as log_file:

        try:
            # Crear cliente SSH
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ssh_host, username=ssh_user, password=ssh_pass, port=22)

            # Comando de prueba con sudo
            comando = "sudo -S ls /root"
            stdin, stdout, stderr = client.exec_command(comando)
            stdin.write(f"{ssh_pass}\n")
            stdin.flush()

            salida = stdout.read().decode()
            errores = stderr.read().decode()

            log_file.write("=== SALIDA DEL COMANDO ===\n")
            log_file.write(salida + "\n")

            log_file.write("=== ERRORES DEL COMANDO ===\n")
            log_file.write(errores + "\n")

            client.close()
            print(f"Prueba en {ssh_host} completada. Log guardado en {log_path}")

        except Exception as e:
            log_file.write(f"Error conectando a {ssh_host}: {e}\n")
            print(f" Error conectando a {ssh_host}. Verifica las credenciales o la red.")

print("\n Prueba finalizada. Revisa los logs generados.")
