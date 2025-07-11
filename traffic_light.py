"""
traffic_light.py

Contiene la definición de la clase TrafficLight, que representa cada semáforo en la simulación.
Permite mostrar visualmente el estado (rojo, amarillo o verde) y adaptar su orientación
vertical u horizontal según el flujo vehicular correspondiente.

"""

import pygame
from config import *

class TrafficLight:
    """
    Clase que representa un semáforo en la intersección.

    Atributos:
        x (int): Posición horizontal en pantalla.
        y (int): Posición vertical en pantalla.
        direction (str): Dirección del semáforo ("vertical" o "horizontal").
        state (str): Estado del semáforo ("green", "yellow", "red").
    """
    def __init__(self, x, y, direction):
        """
        Inicializa un semáforo con posición, orientación y estado inicial.

        Args:
            x (int): Coordenada horizontal.
            y (int): Coordenada vertical.
            direction (str): "vertical" para NS, "horizontal" para EW.
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.state = "green"

    def draw(self, screen):
        """
        Dibuja el semáforo en la pantalla con su orientación y color correspondiente.

        Args:
            screen (pygame.Surface): Superficie donde se dibujará el semáforo.
        """
        if self.direction == "vertical":
            pygame.draw.rect(screen, BLACK, (self.x, self.y, 20, 60))
            if self.state == "green":
                color = GREEN
            elif self.state == "red":
                color = RED
            elif self.state == "yellow":
                color = YELLOW
            pygame.draw.circle(screen, color, (self.x + 10, self.y + 30), 8)

        else:  # horizontal
            pygame.draw.rect(screen, BLACK, (self.x, self.y, 60, 20))
            if self.state == "green":
                color = GREEN
            elif self.state == "red":
                color = RED
            elif self.state == "yellow":
                color = YELLOW
            pygame.draw.circle(screen, color, (self.x + 30, self.y + 10), 8)