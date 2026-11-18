# Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto de la Fase 4 del curso Programación (213023) - UNAD.
Sistema orientado a objetos en Python, sin base de datos, con manejo robusto de excepciones y logs.

## Estructura
- `entidades.py`: clase abstracta `EntidadBase`.
- `cliente.py`: `Cliente` con atributos privados y validaciones.
- `servicios.py`: `Servicio` (abstracta) + `ReservaSala`, `AlquilerEquipo`, `Asesoria`.
- `reserva.py`: `Reserva` (confirmar, cancelar, procesar).
- `excepciones.py`: excepciones personalizadas.
- `logger_config.py`: configuración de logging (archivo `logs/app.log`).
- `main.py`: simulación de 16 operaciones válidas e inválidas.

## Conceptos aplicados
- Abstracción, herencia, polimorfismo y encapsulación.
- Sobrecarga simulada con parámetros opcionales en `calcular_costo_total(horas, impuesto=0.0, descuento=0.0)`
  (Python no tiene sobrecarga nativa).
- `try/except`, `try/except/else`, `try/except/finally` y encadenamiento con `raise ... from`.
- Registro de eventos y errores en `logs/app.log`.

## Ejecución
```
python main.py
```
Requiere Python 3.8 o superior. No usa librerías externas.
