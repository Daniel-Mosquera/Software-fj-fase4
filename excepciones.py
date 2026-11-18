"""
excepciones.py
Excepciones personalizadas del sistema Software FJ.
Todas heredan de ErrorSoftwareFJ para poder capturarlas en bloque.
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base de todo el sistema."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Datos de cliente inválidos (nombre, correo, teléfono)."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Datos de servicio inválidos (nombre, tarifa, atributos propios)."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio existe pero no está disponible para reservar."""


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Falta un parámetro obligatorio (por ejemplo, la duración)."""


class ParametroInvalidoError(ErrorSoftwareFJ):
    """Un parámetro tiene tipo o valor incorrecto."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """La reserva no se pudo crear o procesar."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """La operación no es válida para el estado actual (ej. cancelar dos veces)."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """El cálculo de costos produjo valores inconsistentes."""
