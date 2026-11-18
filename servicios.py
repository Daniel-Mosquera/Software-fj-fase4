"""
servicios.py
Clase abstracta Servicio y tres servicios especializados.
Demuestra herencia, polimorfismo, métodos sobrescritos y "sobrecarga".
"""
from abc import ABC, abstractmethod

from entidades import EntidadBase
from excepciones import (
    CalculoInconsistenteError,
    ParametroFaltanteError,
    ParametroInvalidoError,
    ServicioInvalidoError,
)


class Servicio(EntidadBase, ABC):
    """Clase abstracta: define lo que TODO servicio debe saber hacer."""

    def __init__(self, nombre, tarifa_hora, disponible=True):
        super().__init__()
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El servicio necesita un nombre.")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa por hora inválida: {tarifa_hora!r}")
        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self.disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    # ---------- métodos abstractos (cada hija los sobrescribe) ----------
    @abstractmethod
    def calcular_costo(self, horas) -> float:
        """Costo base (sin impuestos ni descuentos)."""

    @abstractmethod
    def describir(self) -> str:
        """Descripción del servicio."""

    @abstractmethod
    def validar_parametros(self, horas) -> None:
        """Valida los parámetros de la reserva según el tipo de servicio."""

    # ---------- método concreto con "sobrecarga" ----------
    def calcular_costo_total(self, horas, impuesto=0.0, descuento=0.0) -> float:
        """
        Sobrecarga mediante parámetros opcionales (Python no tiene sobrecarga nativa).
        Variantes de llamada:
            calcular_costo_total(3)                  -> solo costo base
            calcular_costo_total(3, 0.19)            -> con impuesto
            calcular_costo_total(3, 0.19, 0.10)      -> con impuesto y descuento
            calcular_costo_total(3, descuento=0.10)  -> solo descuento
        """
        if not (isinstance(impuesto, (int, float)) and 0 <= impuesto <= 1):
            raise CalculoInconsistenteError(f"Impuesto fuera de rango (0-1): {impuesto!r}")
        if not (isinstance(descuento, (int, float)) and 0 <= descuento <= 1):
            raise CalculoInconsistenteError(f"Descuento fuera de rango (0-1): {descuento!r}")

        self.validar_parametros(horas)
        base = self.calcular_costo(horas)
        total = base * (1 - descuento) * (1 + impuesto)
        if total < 0:
            raise CalculoInconsistenteError("El total calculado es negativo.")
        return round(total, 2)

    # ---------- validación común de horas ----------
    @staticmethod
    def _validar_horas(horas, minimo, maximo):
        if horas is None:
            raise ParametroFaltanteError("Falta la duración (horas) de la reserva.")
        if not isinstance(horas, (int, float)) or isinstance(horas, bool):
            raise ParametroInvalidoError(f"La duración debe ser numérica: {horas!r}")
        if not minimo <= horas <= maximo:
            raise ParametroInvalidoError(f"Duración {horas}h fuera de rango ({minimo}-{maximo}h).")


class ReservaSala(Servicio):
    """Servicio 1: reserva de salas."""

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}")
        self._capacidad = capacidad

    def calcular_costo(self, horas) -> float:
        recargo = 1.10 if self._capacidad > 20 else 1.0  # salas grandes +10%
        return self._tarifa_hora * horas * recargo

    def describir(self) -> str:
        return f"Sala '{self._nombre}' (capacidad {self._capacidad}) - ${self._tarifa_hora:,.0f}/h"

    def validar_parametros(self, horas) -> None:
        self._validar_horas(horas, 1, 12)


class AlquilerEquipo(Servicio):
    """Servicio 2: alquiler de equipos."""

    def __init__(self, nombre, tarifa_hora, tipo_equipo, deposito, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(deposito, (int, float)) or deposito < 0:
            raise ServicioInvalidoError(f"Depósito inválido: {deposito!r}")
        self._tipo_equipo = tipo_equipo
        self._deposito = float(deposito)

    def calcular_costo(self, horas) -> float:
        return self._tarifa_hora * horas + self._deposito  # el depósito se suma una vez

    def describir(self) -> str:
        return (f"Equipo '{self._nombre}' ({self._tipo_equipo}) - "
                f"${self._tarifa_hora:,.0f}/h + depósito ${self._deposito:,.0f}")

    def validar_parametros(self, horas) -> None:
        self._validar_horas(horas, 1, 72)


class Asesoria(Servicio):
    """Servicio 3: asesorías especializadas."""

    _MULTIPLICADOR = {"junior": 1.0, "senior": 1.5}

    def __init__(self, nombre, tarifa_hora, especialidad, nivel="junior", disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if nivel not in self._MULTIPLICADOR:
            raise ServicioInvalidoError(f"Nivel inválido (junior/senior): {nivel!r}")
        self._especialidad = especialidad
        self._nivel = nivel

    def calcular_costo(self, horas) -> float:
        return self._tarifa_hora * horas * self._MULTIPLICADOR[self._nivel]

    def describir(self) -> str:
        return (f"Asesoría '{self._nombre}' en {self._especialidad} "
                f"({self._nivel}) - ${self._tarifa_hora:,.0f}/h")

    def validar_parametros(self, horas) -> None:
        self._validar_horas(horas, 1, 8)
