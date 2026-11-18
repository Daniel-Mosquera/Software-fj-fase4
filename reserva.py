"""
reserva.py
Clase Reserva: integra cliente, servicio, duración y estado.
Usa try/except/else/finally y encadenamiento de excepciones.
"""
from cliente import Cliente
from entidades import EntidadBase
from excepciones import (
    ErrorSoftwareFJ,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)
from logger_config import obtener_logger
from servicios import Servicio

logger = obtener_logger()

PENDIENTE, CONFIRMADA, CANCELADA = "PENDIENTE", "CONFIRMADA", "CANCELADA"


class Reserva(EntidadBase):
    def __init__(self, cliente, servicio, horas):
        super().__init__()
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un Servicio válido.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible.")
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = PENDIENTE
        self._total = None

    @property
    def estado(self) -> str:
        return self._estado

    def confirmar(self) -> None:
        """Pasa de PENDIENTE a CONFIRMADA."""
        if self._estado != PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva #{self.id}: estado {self._estado}.")
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self._servicio.nombre}' ya no está disponible.")
        self._estado = CONFIRMADA
        logger.info(f"Reserva #{self.id} CONFIRMADA")

    def cancelar(self) -> None:
        """Cancela la reserva (no se puede cancelar dos veces)."""
        if self._estado == CANCELADA:
            raise OperacionNoPermitidaError(f"La reserva #{self.id} ya estaba cancelada.")
        self._estado = CANCELADA
        logger.info(f"Reserva #{self.id} CANCELADA")

    def procesar(self, impuesto=0.0, descuento=0.0) -> float:
        """
        Calcula el costo total y confirma la reserva.
        Muestra try/except/else/finally y encadenamiento (raise ... from).
        """
        try:
            total = self._servicio.calcular_costo_total(self._horas, impuesto, descuento)
            self.confirmar()
        except ErrorSoftwareFJ as e:
            logger.error(f"Fallo al procesar reserva #{self.id}: {e}")
            # Encadenamiento: el error original queda como causa (__cause__)
            raise ReservaInvalidaError(f"No se pudo procesar la reserva #{self.id}") from e
        else:
            # Solo se ejecuta si NO hubo excepción
            self._total = total
            logger.info(f"Reserva #{self.id} procesada. Total: ${total:,.2f}")
            return total
        finally:
            # Se ejecuta SIEMPRE (haya error o no)
            logger.debug(f"Fin de procesar() para reserva #{self.id}")

    def describir(self) -> str:
        total = f"${self._total:,.2f}" if self._total is not None else "sin calcular"
        return (f"Reserva #{self.id} | {self._cliente.nombre} | {self._servicio.nombre} | "
                f"{self._horas}h | {self._estado} | total {total}")
