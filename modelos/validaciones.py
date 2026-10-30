import re
from datetime import date, datetime

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def texto_obligatorio(valor, campo, minimo=3, maximo=80):
    texto = (valor or "").strip()
    if len(texto) < minimo:
        raise ValueError(f"{campo} debe tener al menos {minimo} caracteres.")
    if len(texto) > maximo:
        raise ValueError(f"{campo} no puede superar {maximo} caracteres.")
    return texto


def texto_opcional(valor, campo, maximo=250):
    texto = (valor or "").strip()
    if len(texto) > maximo:
        raise ValueError(f"{campo} no puede superar {maximo} caracteres.")
    return texto


def validar_email(email):
    valor = (email or "").strip().lower()
    if not EMAIL_REGEX.match(valor):
        raise ValueError("Ingrese un email válido (ejemplo: nombre@correo.com).")
    return valor


def entero_positivo(valor, campo):
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        raise ValueError(f"{campo} debe ser un número entero.") from None
    if numero <= 0:
        raise ValueError(f"{campo} debe ser mayor que 0.")
    return numero


def parsear_bool(valor, campo="Valor"):
    if isinstance(valor, bool):
        return valor
    texto = str(valor).strip().lower()
    if texto in ("si", "sí", "true", "1", "yes"):
        return True
    if texto in ("no", "false", "0"):
        return False
    raise ValueError(f"{campo} debe ser Sí o No.")


def parsear_fecha(valor, campo="Fecha"):
    if isinstance(valor, date) and not isinstance(valor, datetime):
        return valor.isoformat()
    texto = str(valor).strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(texto, fmt).date().isoformat()
        except ValueError:
            continue
    raise ValueError(f"{campo} debe tener formato AAAA-MM-DD (ejemplo: 2026-11-14).")


def siguiente_id(entidades):
    return max((e.id for e in entidades), default=0) + 1
