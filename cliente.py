"""
cliente.py
Clase Cliente con encapsulación (atributos privados) y validaciones estrictas.
"""
import re

from entidades import EntidadBase
from excepciones import ClienteInvalidoError

# Expresión regular simple para validar correos
_PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


class Cliente(EntidadBase):
    """Cliente de Software FJ. Los datos personales son privados."""

    def __init__(self, nombre, correo, telefono):
        super().__init__()
        # Se usan los setters para que TODA asignación pase por validación
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    # ---------- nombre ----------
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe ser texto de al menos 3 caracteres.")
        if any(c.isdigit() for c in valor):
            raise ClienteInvalidoError("El nombre no puede contener números.")
        self.__nombre = valor.strip().title()

    # ---------- correo ----------
    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not _PATRON_CORREO.match(valor.strip()):
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}")
        self.__correo = valor.strip().lower()

    # ---------- teléfono ----------
    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        try:
            # int() falla con letras; encadenamos esa causa con "from"
            int(str(valor))
        except ValueError as e:
            raise ClienteInvalidoError(f"El teléfono debe ser numérico: {valor!r}") from e
        if not 7 <= len(str(valor)) <= 10:
            raise ClienteInvalidoError("El teléfono debe tener entre 7 y 10 dígitos.")
        self.__telefono = str(valor)

    def describir(self) -> str:
        return f"Cliente #{self.id}: {self.nombre} | {self.correo} | Tel {self.telefono}"
