"""
main.py

Simulación de un cruce de caminos con semáforos en dos direcciones (NS y EW).
Incluye lógica de control por tiempo fijo para semáforos, generación aleatoria de vehículos,
detención por semáforo o congestión y análisis estadístico del cruce.

El sistema modela el comportamiento probabilístico de los conductores ante la luz ámbar,
permitiendo que algunos aceleren para cruzar y otros se detengan, con base en un valor configurable.

"""

import pygame
import random
from config import *
from traffic_light import TrafficLight
from vehicle import Vehicle
# from fuzzy_controller import get_green_time  # Lógica difusa no utilizada en esta versión

# Duraciones fijas para las fases del semáforo (en frames)
GREEN_DURATION = int(10 * FPS)
YELLOW_DURATION = int(2 * FPS)
RED_DURATION = GREEN_DURATION + YELLOW_DURATION

light_phase = "green"
in_yellow = False

# Contadores de vehículos
passed_ns = 0
passed_ew = 0
entered_ns = 0
entered_ew = 0
aceleraron_en_ambar_ns = 0
aceleraron_en_ambar_ew = 0

# Inicialización de Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Simulación de Cruce con Lógica Difusa")
clock = pygame.time.Clock()

# Crear semáforos con dirección y estado inicial correcto
traffic_lights = {
    "NS": TrafficLight(x=355, y=180, direction="vertical"),
    "EW": TrafficLight(x=465, y=325, direction="horizontal")
}
traffic_lights["NS"].state = "green"
traffic_lights["EW"].state = "red"
current_green = "NS"

# Listas de vehículos por dirección
vehicles_ns = []
vehicles_ew = []

def can_spawn(vehicle_list, direction):
    """
    Determina si puede generarse un nuevo vehículo en la lista dada,
    respetando una distancia mínima con el último vehículo creado.

    Args:
        vehicle_list (list): Lista de vehículos existentes en esa dirección.
        direction (str): Dirección del flujo de vehículos ("NS" o "EW").

    Returns:
        bool: True si hay suficiente espacio para generar otro vehículo.
    """
    if not vehicle_list:
        return True
    last = vehicle_list[-1]
    if direction == "NS":
        return last.y > VEHICLE_HEIGHT * 2
    else:
        return last.x > VEHICLE_HEIGHT * 2

def spawn_vehicles():
    """
    Genera vehículos nuevos aleatoriamente para cada dirección,
    según la probabilidad definida y si hay espacio suficiente.
    """
    if random.random() < VEHICLE_SPAWN_PROB and can_spawn(vehicles_ns, "NS"):
        vehicles_ns.append(Vehicle("NS"))
    if random.random() < VEHICLE_SPAWN_PROB and can_spawn(vehicles_ew, "EW"):
        vehicles_ew.append(Vehicle("EW"))

def update_vehicles():
    """
    Actualiza todos los vehículos en pantalla:
    - Mueve vehículos si el semáforo lo permite.
    - Registra si entraron al cruce o si pasaron completamente.
    - Identifica vehículos que aceleraron en luz ámbar.
    - Elimina los vehículos que salen de la pantalla.
    """
    global passed_ns, passed_ew, entered_ns, entered_ew
    global aceleraron_en_ambar_ns, aceleraron_en_ambar_ew

    for v in vehicles_ns[:]:
        v.update(traffic_lights["NS"].state, vehicles_ns, AMBAR_PASA)

        if not v.has_entered and v.y >= 300:
            v.has_entered = True
            entered_ns += 1
            if v.ambar_acelera and v.ambar_decidido and not v.acelero_en_ambar:
                aceleraron_en_ambar_ns += 1
                v.acelero_en_ambar = True

        if v.y > WINDOW_HEIGHT:
            vehicles_ns.remove(v)
            if traffic_lights["NS"].state == "green":
                passed_ns += 1

    for v in vehicles_ew[:]:
        v.update(traffic_lights["EW"].state, vehicles_ew, AMBAR_PASA)

        if not v.has_entered and v.x >= 400:
            v.has_entered = True
            entered_ew += 1
            if v.ambar_acelera and v.ambar_decidido and not v.acelero_en_ambar:
                aceleraron_en_ambar_ew += 1
                v.acelero_en_ambar = True

        if v.x > WINDOW_WIDTH:
            vehicles_ew.remove(v)
            if traffic_lights["EW"].state == "green":
                passed_ew += 1

def draw_all():
    """
    Dibuja todos los elementos visuales del sistema:
    - El fondo blanco
    - La intersección
    - Semáforos y vehículos en sus posiciones actuales
    """
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREY, (350, 250, 100, 100))  # Intersección
    for light in traffic_lights.values():
        light.draw(screen)
    for v in vehicles_ns + vehicles_ew:
        v.draw(screen)
    pygame.display.flip()

# Variables de control de tiempo de fase

timer = 0
current_green = "NS"

# Bucle principal del sistema:
# Controla la ejecución continua del ciclo de simulación, generación de vehículos,
# actualización de estados, transiciones de fases del semáforo y dibujo en pantalla.

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    spawn_vehicles()
    update_vehicles()

    timer += 1
    if light_phase == "green" and timer >= GREEN_DURATION:
        for key in traffic_lights:
            if traffic_lights[key].state == "green":
                traffic_lights[key].state = "yellow"
        light_phase = "yellow"
        timer = 0

    elif light_phase == "yellow" and timer >= YELLOW_DURATION:
        current_green = "EW" if current_green == "NS" else "NS"
        for key in traffic_lights:
            traffic_lights[key].state = "green" if key == current_green else "red"
        light_phase = "green"
        timer = 0

    draw_all()
    clock.tick(FPS)

pygame.quit()

# Reporte final
print("Simulación terminada.")
print(f"Total vehículos que pasaron en verde:")
print(f"Norte-Sur: {passed_ns}")
print(f"Este-Oeste: {passed_ew}")
print("Vehículos que entraron al cruce:")
print(f"NS: {entered_ns}")
print(f"EW: {entered_ew}")
print("Estadísticas de cruce con aceleración en ámbar:")
print(f"NS: {aceleraron_en_ambar_ns} vehículos")
print(f"EW: {aceleraron_en_ambar_ew} vehículos")