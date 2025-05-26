#!/usr/bin/env python3
"""
Player System for Wild Defender Game
=====================================

Handles player character with movement, combat, and state management.
"""

import pygame
from typing import List
from utils import Vector2
from camera import Camera
from constants import (
    GREEN, YELLOW, ORANGE, BLACK,
    EntityType
)

class Player:
    """Player class with movements, speed, jump, health, lives, and shooting"""
    
    def __init__(self, x: float, y: float):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.max_health = 100
        self.health = self.max_health
        self.max_lives = 3
        self.lives = self.max_lives
        self.speed = 200
        self.jump_speed = -350
        self.gravity = 800
        self.on_ground = False
        self.width = 35
        self.height = 45
        self.rect = pygame.Rect(x - self.width//2, y - self.height, self.width, self.height)
        self.direction = 1  # 1 for right, -1 for left
        self.last_shot_time = 0
        self.shoot_cooldown = 0.3
        self.power_up_timer = 0
        self.has_power_up = False
        
        # Animation states
        self.is_running = False
        self.is_jumping = False
        self.animation_time = 0
    
    def update(self, dt: float, keys_pressed):
        """Update player movement and state"""
        # Reset movement
        self.velocity.x = 0
        self.is_running = False
        
        # Handle horizontal movement
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.velocity.x = -self.speed
            self.direction = -1
            self.is_running = True
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.velocity.x = self.speed
            self.direction = 1
            self.is_running = True
        
        # Handle jumping
        if (keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]) and self.on_ground:
            self.velocity.y = self.jump_speed
            self.on_ground = False
            self.is_jumping = True
        
        # Apply physics
        self._apply_physics(dt)
        
        # Update power-up timer
        if self.has_power_up:
            self.power_up_timer -= dt
            if self.power_up_timer <= 0:
                self.has_power_up = False
        
        # Update animation
        self.animation_time += dt
        
        # Update rectangle position
        self.rect.centerx = int(self.position.x)
        self.rect.bottom = int(self.position.y)
    
    def _apply_physics(self, dt: float):
        """Apply gravity and movement physics"""
        # Apply gravity
        if not self.on_ground:
            self.velocity.y += self.gravity * dt
        
        # Update position
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        
        # Simple ground collision (assume ground at y = 600)
        if self.position.y >= 600:
            self.position.y = 600
            self.velocity.y = 0
            self.on_ground = True
            self.is_jumping = False
        else:
            self.on_ground = False
        
        # Keep player in bounds (simple world boundaries)
        self.position.x = max(20, min(self.position.x, 2980))
    
    def shoot(self, projectiles: List):
        """Shoot a projectile"""
        current_time = pygame.time.get_ticks() / 1000.0
        
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            # Import here to avoid circular imports
            from projectile import Projectile
            
            # Calculate shoot direction
            direction = Vector2(self.direction, 0)
            
            # Create projectile
            projectile_speed = 400 if not self.has_power_up else 600
            projectile_damage = 25 if not self.has_power_up else 40
            projectile_color = YELLOW if not self.has_power_up else ORANGE
            
            projectile = Projectile(
                self.position.x + (self.width // 2 * self.direction),
                self.position.y - self.height // 2,
                direction, projectile_speed, projectile_damage,
                EntityType.PLAYER, projectile_color
            )
            projectiles.append(projectile)
            self.last_shot_time = current_time
    
    def take_damage(self, damage: int):
        """Take damage and handle death"""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.die()
    
    def die(self):
        """Handle player death"""
        self.lives -= 1
        if self.lives > 0:
            self.health = self.max_health
            # Reset position to start of level
            self.position = Vector2(100, 600)
    
    def heal(self, amount: int):
        """Heal player"""
        self.health = min(self.max_health, self.health + amount)
    
    def add_life(self):
        """Add an extra life"""
        self.lives = min(5, self.lives + 1)  # Max 5 lives
    
    def activate_power_up(self):
        """Activate power-up"""
        self.has_power_up = True
        self.power_up_timer = 10.0  # 10 seconds
    
    def draw(self, screen: pygame.Surface, camera: Camera):
        """Draw player on screen"""
        screen_rect = camera.apply(self.rect)
        
        # Choose color based on state
        player_color = GREEN
        if self.has_power_up:
            # Flash between green and yellow when powered up
            player_color = YELLOW if int(self.animation_time * 10) % 2 else GREEN
        
        # Draw player body (wolf-like)
        pygame.draw.ellipse(screen, player_color, screen_rect)
        
        # Draw direction indicator (simple wolf head)
        head_x = screen_rect.centerx + (8 if self.direction > 0 else -8)
        head_y = screen_rect.y + 8
        
        # Head
        pygame.draw.circle(screen, player_color, (head_x, head_y), 8)
        
        # Eyes
        eye1_x = head_x + (3 if self.direction > 0 else -3)
        eye2_x = head_x + (1 if self.direction > 0 else -1)
        pygame.draw.circle(screen, BLACK, (eye1_x, head_y - 2), 2)
        pygame.draw.circle(screen, BLACK, (eye2_x, head_y + 1), 1)
        
        # Ears
        ear1_x = head_x + (2 if self.direction > 0 else -2)
        ear2_x = head_x - (2 if self.direction > 0 else -2)
        pygame.draw.circle(screen, player_color, (ear1_x, head_y - 6), 3)
        pygame.draw.circle(screen, player_color, (ear2_x, head_y - 5), 3)
