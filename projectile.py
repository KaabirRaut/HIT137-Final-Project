#!/usr/bin/env python3
"""
Projectile System for Wild Defender Game
=========================================

Handles projectiles fired by players and enemies.
"""

import pygame
from typing import Tuple
from utils import Vector2
from camera import Camera
from constants import EntityType, WHITE

class Projectile:
    """Projectile class with movement, speed, and damage"""
    
    def __init__(self, x: float, y: float, direction: Vector2, speed: float, 
                 damage: int, owner_type: EntityType, color: Tuple[int, int, int] = WHITE):
        self.position = Vector2(x, y)
        self.velocity = direction.normalize() * speed
        self.damage = damage
        self.owner_type = owner_type
        self.color = color
        self.radius = 3
        self.active = True
        self.rect = pygame.Rect(x - self.radius, y - self.radius, 
                               self.radius * 2, self.radius * 2)
    
    def update(self, dt: float):
        """Update projectile position and check bounds"""
        if not self.active:
            return
        
        # Update position
        self.position = self.position + self.velocity * dt
        self.rect.center = (int(self.position.x), int(self.position.y))
        
        # Deactivate if out of bounds
        if (self.position.x < -50 or self.position.x > 3000 or
            self.position.y < -50 or self.position.y > 1000):
            self.active = False
    
    def draw(self, screen: pygame.Surface, camera: Camera):
        """Draw projectile on screen"""
        if self.active:
            screen_rect = camera.apply(self.rect)
            pygame.draw.circle(screen, self.color, screen_rect.center, self.radius)
    
    def check_collision(self, target_rect: pygame.Rect) -> bool:
        """Check collision with target rectangle"""
        return self.active and self.rect.colliderect(target_rect)
