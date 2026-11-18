"""
logger_config.py
Configura el logging: todo evento y error se guarda en logs/app.log
(y además se muestra en consola).
"""
import logging
import os

# Ruta del archivo de logs (junto a este archivo, carpeta logs/)
RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "app.log")


def obtener_logger(nombre: str = "software_fj") -> logging.Logger:
    """Devuelve un logger configurado (se configura una sola vez)."""
    logger = logging.getLogger(nombre)
    if logger.handlers:  # ya configurado, no duplicar handlers
        return logger

    logger.setLevel(logging.DEBUG)
    os.makedirs(os.path.dirname(RUTA_LOG), exist_ok=True)

    formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")

    # Handler 1: archivo de logs (obligatorio en la actividad)
    archivo = logging.FileHandler(RUTA_LOG, encoding="utf-8")
    archivo.setFormatter(formato)
    logger.addHandler(archivo)

    # Handler 2: consola, para ver lo que pasa mientras corre
    consola = logging.StreamHandler()
    consola.setLevel(logging.INFO)
    consola.setFormatter(formato)
    logger.addHandler(consola)

    return logger
