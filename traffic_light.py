# traffic_light.py
# Define la clase TrafficLight para representar los semáforos de la simulación

import pygame
from config import *

class TrafficLight:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction  # "vertical" o "horizontal"
        self.state = "green"  # El estado inicial puede ser "green" o "red"

    def draw(self, screen):
        if self.direction == "vertical":
            # Semáforo vertical (Norte-Sur)
            pygame.draw.rect(screen, BLACK, (self.x, self.y, 20, 60))
            if self.state == "green":
                color = GREEN
            elif self.state == "red":
                color = RED
            elif self.state == "yellow":
                color = YELLOW
            pygame.draw.circle(screen, color, (self.x + 10, self.y + 30), 8)
        else:
            # Semáforo horizontal (Este-Oeste)
            pygame.draw.rect(screen, BLACK, (self.x, self.y, 60, 20))
            if self.state == "green":
                color = GREEN
            elif self.state == "red":
                color = RED
            elif self.state == "yellow":
                color = YELLOW
            pygame.draw.circle(screen, color, (self.x + 30, self.y + 10), 8)