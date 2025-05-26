#!/usr/bin/env python3
"""
Camera System for Wild Defender Game
====================================

Handles dynamic camera that smoothly follows the player.
"""

import pygame

class Camera:
    """Dynamic camera that follows the player smoothly"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0
        self.smoothing = 0.1
        
    def update(self, target_x: float, target_y: float, world_width: int, world_height: int):
        """Update camera position to follow target smoothly"""
        # Set target position (center the target on screen)
        self.target_x = target_x - self.width // 2
        self.target_y = target_y - self.height // 2
        
        # Smoothly interpolate to target
        self.x += (self.target_x - self.x) * self.smoothing
        self.y += (self.target_y - self.y) * self.smoothing
        
        # Clamp camera to world bounds
        self.x = max(0, min(self.x, world_width - self.width))
        self.y = max(0, min(self.y, world_height - self.height))
    
    def apply(self, entity_rect: pygame.Rect) -> pygame.Rect:
        """Apply camera offset to entity rectangle"""
        return pygame.Rect(entity_rect.x - self.x, entity_rect.y - self.y, 
                          entity_rect.width, entity_rect.height)
