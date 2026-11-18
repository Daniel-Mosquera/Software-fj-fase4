"""
main.py
Simulación de 15 operaciones (válidas e inválidas) de Software FJ.
El programa NUNCA se detiene ante un error: cada operación está protegida.
"""
from cliente import Cliente
from excepciones import ErrorSoftwareFJ
from logger_config import obtener_logger
from reserva import Reserva
from servicios import Asesoria, AlquilerEquipo, ReservaSala

logger = obtener_logger()

# Listas internas (en lugar de base de datos)
clientes, servicios, reservas = [], [], []


def ejecutar(numero, titulo, operacion):
    """Ejecuta una operación protegida con try/except/else/finally."""
    logger.info(f"--- Operación {numero}: {titulo} ---")
    try:
        resultado = operacion()
    except ErrorSoftwareFJ as e:
        # Error controlado del dominio; si tiene causa encadenada, también se registra
        causa = f" | causa: {e.__cause__!r}" if e.__cause__ else ""
        logger.error(f"Error controlado en operación {numero}: {e}{causa}")
    except Exception as e:
        # Error inesperado: se registra con traza y el programa sigue
        logger.exception(f"Error INESPERADO en operación {numero}: {e}")
    else:
        logger.info(f"Operación {numero} exitosa -> {resultado}")
    finally:
        logger.debug(f"Operación {numero} finalizada")


def registrar_cliente(*args):
    c = Cliente(*args)
    clientes.append(c)
    return c.describir()


def registrar_servicio(clase, *args):
    s = clase(*args)
    servicios.append(s)
    return s.describir()


def nueva_reserva(cliente, servicio, horas, impuesto=0.0, descuento=0.0):
    r = Reserva(cliente, servicio, horas)
    r.procesar(impuesto, descuento)
    reservas.append(r)  # solo se guarda si se procesó sin errores
    return r.describir()


def main():
    logger.info("===== INICIO SIMULACIÓN SOFTWARE FJ =====")

    # 1-3 Clientes
    ejecutar(1, "Cliente válido", lambda: registrar_cliente("Ana Torres", "ana@correo.com", "3101234567"))
    ejecutar(2, "Cliente inválido (correo)", lambda: registrar_cliente("Luis Pérez", "luis-correo", "3109876543"))
    ejecutar(3, "Cliente inválido (teléfono con letras)", lambda: registrar_cliente("Marta Ríos", "marta@correo.com", "31O1234"))

    # 4-7 Servicios
    ejecutar(4, "Sala válida", lambda: registrar_servicio(ReservaSala, "Sala Ejecutiva", 50000, 25))
    ejecutar(5, "Servicio inválido (tarifa negativa)", lambda: registrar_servicio(AlquilerEquipo, "Proyector", -100, "Video", 20000))
    ejecutar(6, "Equipo válido", lambda: registrar_servicio(AlquilerEquipo, "Portátil Pro", 15000, "Computo", 30000))
    ejecutar(7, "Asesoría válida", lambda: registrar_servicio(Asesoria, "Asesoría Cloud", 80000, "Cloud", "senior"))

    # Protección: si el paso 1 falló, no habría cliente; aquí sí existe
    ana, sala, equipo, asesoria = clientes[0], servicios[0], servicios[1], servicios[2]

    # 8-15 Reservas y casos límite
    ejecutar(8, "Reserva exitosa (IVA 19% y descuento 10%)", lambda: nueva_reserva(ana, sala, 3, 0.19, 0.10))
    ejecutar(9, "Reserva de equipo exitosa", lambda: nueva_reserva(ana, equipo, 10, 0.19))

    equipo.disponible = False  # simulamos servicio no disponible
    ejecutar(10, "Reserva con servicio no disponible", lambda: nueva_reserva(ana, equipo, 2))
    equipo.disponible = True

    ejecutar(11, "Reserva sin duración (parámetro faltante)", lambda: nueva_reserva(ana, asesoria, None))
    ejecutar(12, "Reserva con duración fuera de rango", lambda: nueva_reserva(ana, asesoria, 20))
    ejecutar(13, "Reserva con cliente inválido (None)", lambda: nueva_reserva(None, sala, 2))
    ejecutar(14, "Cálculo inconsistente (descuento 150%)", lambda: nueva_reserva(ana, sala, 2, 0.19, 1.5))

    def cancelar_dos_veces():
        r = reservas[0]
        r.cancelar()
        r.cancelar()  # segunda vez -> OperacionNoPermitidaError

    ejecutar(15, "Cancelar la misma reserva dos veces", cancelar_dos_veces)

    ejecutar(16, "Error inesperado (división por cero)", lambda: 1 / 0)

    logger.info("===== RESUMEN FINAL =====")
    for r in reservas:
        logger.info(r.describir())
    logger.info("===== FIN: el sistema siguió estable ante todos los errores =====")


if __name__ == "__main__":
    main()
