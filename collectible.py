#!/usr/bin/env python3
"""
Collectible System for Wild Defender Game
==========================================

Handles collectible items like health boosts, extra lives, and power-ups.
"""

import pygame
import math
from utils import Vector2
from camera import Camera
from constants import GREEN, BLUE, YELLOW, WHITE, ORANGE

class Collectible:
    """Collectible class for health boosts, extra lives, etc."""
    
    def __init__(self, x: float, y: float, collectible_type: str):
        self.position = Vector2(x, y)
        self.type = collectible_type  # 'health', 'life', 'power'
        self.rect = pygame.Rect(x - 15, y - 15, 30, 30)
        self.active = True
        self.bob_offset = 0
        self.bob_speed = 3
        
        # Set properties based on type
        if collectible_type == 'health':
            self.color = GREEN
            self.value = 25
        elif collectible_type == 'life':
            self.color = BLUE
            self.value = 1
        elif collectible_type == 'power':
            self.color = YELLOW
            self.value = 1
    
    def update(self, dt: float):
        """Update collectible animation"""
        if self.active:
            self.bob_offset += self.bob_speed * dt
            # Create floating effect
            float_y = math.sin(self.bob_offset) * 3
            self.rect.centery = int(self.position.y + float_y)
    
    def draw(self, screen: pygame.Surface, camera: Camera):
        """Draw collectible on screen"""
        if self.active:
            screen_rect = camera.apply(self.rect)
            if self.type == 'health':
                # Draw health cross
                pygame.draw.rect(screen, self.color, screen_rect)
                pygame.draw.rect(screen, WHITE, 
                               (screen_rect.centerx - 2, screen_rect.y + 5, 4, 20))
                pygame.draw.rect(screen, WHITE, 
                               (screen_rect.x + 5, screen_rect.centery - 2, 20, 4))
            elif self.type == 'life':
                # Draw life star
                pygame.draw.circle(screen, self.color, screen_rect.center, 15)
                pygame.draw.circle(screen, WHITE, screen_rect.center, 10)
            elif self.type == 'power':
                # Draw power lightning
                pygame.draw.circle(screen, self.color, screen_rect.center, 15)
                pygame.draw.circle(screen, ORANGE, screen_rect.center, 10)
    
    def collect(self):
        """Mark collectible as collected"""
        self.active = False
