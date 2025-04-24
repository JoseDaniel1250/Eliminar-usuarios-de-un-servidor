import paramiko
import os

# Configuración de rutas
backup_dir = "backups"
log_dir = "logs"

# Crear directorios si no existen
os.makedirs(backup_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)

# Leer lista de servidores
with open('servers.txt', 'r') as f:
    servidores = [line.strip().split(',') for line in f.readlines()]

# Leer lista de usuarios a eliminar
with open('usuarios_a_borrar.txt', 'r') as f:
    usuarios_a_borrar = [line.strip() for line in f.readlines()]

print("===== INICIANDO PROCESO DE ELIMINACIÓN DE USUARIOS =====")

for ssh_user, ssh_host, ssh_pass in servidores:
    print(f"\n=========================================")
    print(f"Conectando a {ssh_host} como {ssh_user}...")

    log_path = os.path.join(log_dir, f"{ssh_host.replace('.', '_')}.log")
    with open(log_path, "w") as log_file:

        try:
            # Crear cliente SSH
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ssh_host, username=ssh_user, password=ssh_pass, port=22)

            sftp = client.open_sftp()

            # Backup de archivos críticos
            for archivo in ["/etc/passwd", "/etc/shadow", "/etc/sudoers"]:
                try:
                    base = os.path.basename(archivo)
                    remote_backup = f"{archivo}.bak"
                    client.exec_command(f"sudo cp {archivo} {remote_backup}")
                    sftp.get(remote_backup, os.path.join(backup_dir, f"{base}_{ssh_host.replace('.', '_')}.bak"))
                    log_file.write(f"Backup de {archivo} realizado correctamente.\n")
                except Exception as e:
                    log_file.write(f"Error haciendo backup de {archivo}: {e}\n")

            # Eliminar usuarios
            for usuario in usuarios_a_borrar:
                stdin, stdout, stderr = client.exec_command(f"id -u {usuario}")
                if stdout.channel.recv_exit_status() == 0:
                    log_file.write(f" Usuario '{usuario}' existe. Procediendo a eliminar...\n")
                    client.exec_command(f"sudo userdel -r {usuario}")
                    log_file.write(f"Usuario '{usuario}' eliminado exitosamente.\n")
                else:
                    log_file.write(f" Usuario '{usuario}' no existe.\n")

            sftp.close()
            client.close()
            print(f"Proceso en {ssh_host} completado. Log guardado en {log_path}")

        except Exception as e:
            log_file.write(f"Error conectando a {ssh_host}: {e}\n")
            print(f" Error conectando a {ssh_host}. Verifica las credenciales o la red.")

print("\n Proceso finalizado. Revisa los logs y backups generados.")
