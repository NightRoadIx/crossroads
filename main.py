# main.py
# Archivo principal del proyecto de simulación de cruce de caminos con lógica difusa
# Este archivo inicializa pygame, configura la ventana, y ejecuta el bucle principal
import pygame
import random
from config import *
from traffic_light import TrafficLight
from vehicle import Vehicle
# from fuzzy_controller import get_green_time

GREEN_DURATION = int(10 * FPS)
YELLOW_DURATION = int(2 * FPS)
RED_DURATION = GREEN_DURATION + YELLOW_DURATION

light_phase = "green"
in_yellow = False

# Contadores de vehículos que pasan
passed_ns = 0
passed_ew = 0
# Contadores de vehículos que ingresaron al cruce
entered_ns = 0
entered_ew = 0

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Simulación de Cruce con Lógica Difusa")
clock = pygame.time.Clock()

# Crear semáforos para las dos calles principales
# Coordenadas aproximadas del cruce, puedes ajustarlas a tu gusto
traffic_lights = {
    "NS": TrafficLight(x=355, y=180, direction="vertical"),  # Norte-Sur
    "EW": TrafficLight(x=465, y=325, direction="horizontal")  # Este-Oeste
}
# Iniciar correctamente los semáforos
traffic_lights["NS"].state = "green"
traffic_lights["EW"].state = "red"
current_green = "NS"  # Asegura coherencia con la lógica de cambio

# Lista para almacenar vehículos
vehicles_ns = []
vehicles_ew = []

# Funciones auxiliares
def can_spawn(vehicle_list, direction):
    if not vehicle_list:
        return True
    last = vehicle_list[-1]
    if direction == "NS":
        return last.y > VEHICLE_HEIGHT * 2
    else:
        return last.x > VEHICLE_HEIGHT * 2

def spawn_vehicles():
    if random.random() < VEHICLE_SPAWN_PROB and can_spawn(vehicles_ns, "NS"):
        vehicles_ns.append(Vehicle("NS"))
    if random.random() < VEHICLE_SPAWN_PROB and can_spawn(vehicles_ew, "EW"):
        vehicles_ew.append(Vehicle("EW"))

def update_vehicles():
    global passed_ns, passed_ew, entered_ns, entered_ew

    for v in vehicles_ns[:]:
        v.update(traffic_lights["NS"].state, vehicles_ns)

        # Solo se marca como entrado cuando realmente ya cruzó el centro del cruce
        if not v.has_entered and v.y >= 300:
            v.has_entered = True
            entered_ns += 1

        if v.y > WINDOW_HEIGHT:
            vehicles_ns.remove(v)
            if traffic_lights["NS"].state == "green":
                passed_ns += 1

    for v in vehicles_ew[:]:
        v.update(traffic_lights["EW"].state, vehicles_ew)

        if not v.has_entered and v.x >= 400:
            v.has_entered = True
            entered_ew += 1

        if v.x > WINDOW_WIDTH:
            vehicles_ew.remove(v)
            if traffic_lights["EW"].state == "green":
                passed_ew += 1

def draw_all():
    screen.fill(WHITE)

    # Dibujar intersección (simplificada)
    pygame.draw.rect(screen, GREY, (350, 250, 100, 100))

    for light in traffic_lights.values():
        light.draw(screen)
    for v in vehicles_ns + vehicles_ew:
        v.draw(screen)

    pygame.display.flip()

# Variables para control del tiempo de luz verde por lógica difusa
timer = 0
current_green = "NS"
#green_duration = get_green_time(len(vehicles_ns), len(vehicles_ew))

# Bucle principal
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

print("Simulación terminada.")
print(f"Total vehículos que pasaron en verde:")
print(f"Norte-Sur: {passed_ns}")
print(f"Este-Oeste: {passed_ew}")
print("Vehículos que entraron al cruce:")
print(f"NS: {entered_ns}")
print(f"EW: {entered_ew}")
