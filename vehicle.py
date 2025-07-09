# vehicle.py
# Define la clase Vehicle para representar los autos que se mueven en la simulación
import pygame
import random
from config import *

class Vehicle:
    def __init__(self, direction):
        # La dirección puede ser 'NS' (norte-sur) o 'EW' (este-oeste)
        self.direction = direction
        self.stopped = False  # Estado del vehículo: detenido o en movimiento
        self.has_entered = False  # Para registrar solo una vez cuando entra al cruce
        self.personal_space = max(6, min(20, int(random.gauss(12, 3))))

        if direction == "NS":
            self.x = 385
            self.y = 0 - VEHICLE_HEIGHT
            self.dx = 0
            self.dy = VEHICLE_SPEED
        else:
            self.x = 0 - VEHICLE_HEIGHT
            self.y = 315
            self.dx = VEHICLE_SPEED
            self.dy = 0

        self.color = BLUE

    def update(self, light_state, others):
        self.stopped = False
        next_pos = (self.y + VEHICLE_HEIGHT if self.direction == "NS" else self.x + VEHICLE_HEIGHT)
        stopping_distance = 10

        for other in others:
            if other == self:
                continue
            if self.direction == "NS" and 0 < (other.y - self.y - VEHICLE_HEIGHT) < VEHICLE_HEIGHT + self.personal_space :
                self.stopped = True
                return
            if self.direction == "EW" and 0 < (other.x - self.x - VEHICLE_HEIGHT) < VEHICLE_HEIGHT + self.personal_space :
                self.stopped = True
                return

        # Solo detener antes del cruce si el semáforo está en rojo
        if self.direction == "NS":
            if not self.has_entered and light_state == "red" and self.y + VEHICLE_HEIGHT >= 250:
                self.stopped = True
                return
        elif self.direction == "EW":
            if not self.has_entered and light_state == "red" and self.x + VEHICLE_HEIGHT >= 350:
                self.stopped = True
                return

        # Avanza
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        display_color = BLACK if self.stopped else self.color
        if self.direction == "NS":
            rect = pygame.Rect(self.x, self.y, VEHICLE_WIDTH, VEHICLE_HEIGHT)
        else:
            rect = pygame.Rect(self.x, self.y, VEHICLE_HEIGHT, VEHICLE_WIDTH)
        pygame.draw.rect(screen, display_color, rect)