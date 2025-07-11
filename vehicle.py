"""
vehicle.py

Contiene la definición de la clase Vehicle, que representa a cada automóvil en la simulación.
Cada vehículo responde a las condiciones del semáforo, mantiene distancia con otros vehículos
y puede tomar decisiones probabilísticas ante la luz ámbar.

"""

import pygame
import random
from config import *

class Vehicle:
    """
    Clase que representa un vehículo que circula en la simulación.

    Atributos:
        direction (str): Dirección de circulación ("NS" o "EW").
        x, y (int): Coordenadas actuales del vehículo.
        dx, dy (int): Velocidad de desplazamiento por eje.
        stopped (bool): Si el vehículo está detenido.
        has_entered (bool): True si ya ingresó al cruce.
        personal_space (int): Distancia mínima con respecto al vehículo anterior.
        ambar_decidido (bool): True si ya tomó decisión frente al semáforo amarillo.
        ambar_acelera (bool): True si decidió acelerar en ámbar.
        acelero_en_ambar (bool): True si efectivamente cruzó el cruce acelerando en ámbar.
        color (tuple): Color del vehículo.
    """
    def __init__(self, direction):
        """
        Inicializa un nuevo vehículo en la dirección indicada.

        Args:
            direction (str): 'NS' (norte-sur) o 'EW' (este-oeste)
        """
        self.direction = direction
        self.stopped = False
        self.has_entered = False
        self.personal_space = max(6, min(20, int(random.gauss(12, 3))))
        self.ambar_decidido = False
        self.ambar_acelera = False
        self.original_speed = VEHICLE_SPEED
        self.acelero_en_ambar = False

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

    def update(self, light_state, others, ambar_pasa):
        """
        Actualiza la posición y estado del vehículo según el semáforo y el tráfico.

        Args:
            light_state (str): Estado actual del semáforo ("green", "yellow", "red").
            others (list): Lista de vehículos en la misma dirección.
            ambar_pasa (float): Probabilidad de que el vehículo decida cruzar en luz ámbar.
        """
        self.stopped = False

        # Verifica distancia de seguridad con vehículo de adelante
        for other in others:
            if other == self:
                continue
            if self.direction == "NS" and 0 < (other.y - self.y - VEHICLE_HEIGHT) < VEHICLE_HEIGHT + self.personal_space:
                self.stopped = True
                return
            if self.direction == "EW" and 0 < (other.x - self.x - VEHICLE_HEIGHT) < VEHICLE_HEIGHT + self.personal_space:
                self.stopped = True
                return

        # Comportamiento frente a luz ámbar
        if light_state == "yellow":
            if not self.ambar_decidido:
                self.ambar_acelera = random.random() < ambar_pasa
                self.ambar_decidido = True

            if self.ambar_acelera:
                self.x += int(self.dx * 1.5)
                self.y += int(self.dy * 1.5)
                return
            else:
                if not self.has_entered:
                    self.stopped = True
                    return

        # Detención en rojo si aún no ha ingresado al cruce
        if self.direction == "NS":
            if not self.has_entered and light_state == "red" and self.y + VEHICLE_HEIGHT >= 250 and self.y < 300:
                self.stopped = True
                return
        elif self.direction == "EW":
            if not self.has_entered and light_state == "red" and self.x + VEHICLE_HEIGHT >= 350 and self.x < 400:
                self.stopped = True
                return

        # Movimiento normal (verde o ya dentro del cruce)
        self.x += self.dx
        self.y += self.dy

        # Reinicia decisión si ya cruzó
        if self.has_entered:
            self.ambar_decidido = False

    def draw(self, screen):
        """
        Dibuja el vehículo en pantalla.

        Args:
            screen (pygame.Surface): Superficie donde se dibujará el vehículo.
        """
        display_color = BLACK if self.stopped else self.color
        if self.direction == "NS":
            rect = pygame.Rect(self.x, self.y, VEHICLE_WIDTH, VEHICLE_HEIGHT)
        else:
            rect = pygame.Rect(self.x, self.y, VEHICLE_HEIGHT, VEHICLE_WIDTH)
        pygame.draw.rect(screen, display_color, rect)