# Simulador de Cruce Vehicular con Semáforos y Lógica de Decisión en Ámbar

Este proyecto implementa una simulación visual en 2D de un cruce vial con semáforos en dos direcciones: norte-sur (NS) y este-oeste (EW). Los vehículos son generados de manera aleatoria y responden a las señales de tráfico, respetando el semáforo y la distancia entre ellos. El sistema incluye lógica probabilística para simular decisiones en luz ámbar (acelerar o detenerse).

## 📋 Características

- Semáforos totalmente funcionales con transiciones verde–ámbar–rojo.
- Comportamiento independiente por dirección (Norte-Sur y Este-Oeste).
- Aparición aleatoria de vehículos de vehículos.
- Decisión aleatoria si el vehículo incrementa su velocidad ante la luz ámbar.
- Los vehículos se detienen a una distancia aleatoria del siguiente cuando hay luz roja.
- Registro estadístico:
  - Vehículos que pasaron
  - Vehículos que cruzaron
  - Vehículos que aceleraron con luz ámbar
- Visualización con `pygame`.

## 🗂 Estructura del Proyecto

├── main.py # Ejecuta la simulación
├── config.py # Constantes y parámetros globales
├── vehicle.py # Clase de vehículo y su lógica de movimiento
├── traffic_light.py # Clase de semáforo
├── fuzzy_controller.py # (opcional) Control difuso de tiempos
├── README.md # Documentación del proyecto


## ⚙️ Requisitos

- Python 3.10
- pygame 2.5.2
- numpy 1.24.4
- scikit-fuzzy 0.4.2
