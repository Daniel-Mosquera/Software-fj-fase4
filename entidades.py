"""
entidades.py
Clase abstracta que representa las entidades generales del sistema.
"""
from abc import ABC, abstractmethod


class EntidadBase(ABC):
    """Toda entidad (Cliente, Servicio, Reserva) tiene un id único y se describe."""

    _contador = 0  # contador compartido para generar ids

    def __init__(self):
        EntidadBase._contador += 1
        self._id = EntidadBase._contador  # atributo protegido

    @property
    def id(self) -> int:
        """Id único de solo lectura."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Cada entidad debe describirse a sí misma (polimorfismo)."""
