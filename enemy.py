#!/usr/bin/env python3
"""
Enemy System for Wild Defender Game
====================================

Handles enemy AI, behavior, and combat mechanics.
"""

import pygame
from typing import List
from utils import Vector2
from camera import Camera
from constants import (
    RED, PURPLE, DARK_GRAY, WHITE, GREEN, ORANGE,
    EntityType
)

class Enemy:
    """Enemy class with AI, health, movement, and shooting"""
    
    def __init__(self, x: float, y: float, enemy_type: str):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.enemy_type = enemy_type
        self.active = True
        self.on_ground = False
        
        # Set properties based on enemy type
        if enemy_type == 'soldier':
            self.max_health = 50
            self.speed = 80
            self.damage = 15
            self.color = RED
            self.width = 30
            self.height = 40
            self.shoot_cooldown = 2.0
            self.detection_range = 300
        elif enemy_type == 'archer':
            self.max_health = 30
            self.speed = 60
            self.damage = 20
            self.color = PURPLE
            self.width = 25
            self.height = 35
            self.shoot_cooldown = 1.5
            self.detection_range = 400
        elif enemy_type == 'boss':
            self.max_health = 200
            self.speed = 40
            self.damage = 30
            self.color = DARK_GRAY
            self.width = 60
            self.height = 80
            self.shoot_cooldown = 1.0
            self.detection_range = 500
        
        self.health = self.max_health
        self.rect = pygame.Rect(x - self.width//2, y - self.height, self.width, self.height)
        self.last_shot_time = 0
        self.direction = 1  # 1 for right, -1 for left
        self.ai_state = 'patrol'  # 'patrol', 'chase', 'attack'
        self.patrol_start_x = x
        self.patrol_range = 200
        
        # Physics constants
        self.gravity = 800
        self.jump_speed = -300
    
    def update(self, dt: float, player_pos: Vector2, projectiles: List):
        """Update enemy AI, movement, and behavior"""
        if not self.active:
            return
        
        # Calculate distance to player
        distance_to_player = (self.position - player_pos).magnitude()
        
        # AI State Machine
        if distance_to_player <= self.detection_range:
            if distance_to_player <= 100:
                self.ai_state = 'attack'
            else:
                self.ai_state = 'chase'
        else:
            self.ai_state = 'patrol'
        
        # Execute AI behavior
        if self.ai_state == 'patrol':
            self._patrol(dt)
        elif self.ai_state == 'chase':
            self._chase_player(player_pos, dt)
        elif self.ai_state == 'attack':
            self._attack_player(player_pos, dt, projectiles)
        
        # Apply physics
        self._apply_physics(dt)
        
        # Update rectangle position
        self.rect.centerx = int(self.position.x)
        self.rect.bottom = int(self.position.y)
    
    def _patrol(self, dt: float):
        """Patrol behavior - move back and forth"""
        if self.position.x <= self.patrol_start_x - self.patrol_range:
            self.direction = 1
        elif self.position.x >= self.patrol_start_x + self.patrol_range:
            self.direction = -1
        
        self.velocity.x = self.speed * self.direction * 0.5  # Slower patrol speed
    
    def _chase_player(self, player_pos: Vector2, dt: float):
        """Chase behavior - move towards player"""
        direction_to_player = (player_pos - self.position).normalize()
        self.velocity.x = direction_to_player.x * self.speed
        self.direction = 1 if direction_to_player.x > 0 else -1
    
    def _attack_player(self, player_pos: Vector2, dt: float, projectiles: List):
        """Attack behavior - shoot at player"""
        current_time = pygame.time.get_ticks() / 1000.0
        
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            # Import here to avoid circular imports
            from projectile import Projectile
            
            # Shoot at player
            direction_to_player = (player_pos - self.position).normalize()
            
            # Create projectile
            projectile = Projectile(
                self.position.x, self.position.y - self.height // 2,
                direction_to_player, 200, self.damage,
                EntityType.ENEMY_SOLDIER if self.enemy_type == 'soldier' else EntityType.ENEMY_ARCHER,
                RED if self.enemy_type != 'boss' else ORANGE
            )
            projectiles.append(projectile)
            self.last_shot_time = current_time
        
        # Stop moving when attacking
        self.velocity.x = 0
    
    def _apply_physics(self, dt: float):
        """Apply gravity and movement"""
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
        else:
            self.on_ground = False
    
    def take_damage(self, damage: int) -> bool:
        """Take damage and return True if enemy is defeated"""
        self.health -= damage
        if self.health <= 0:
            self.active = False
            return True
        return False
    
    def draw(self, screen: pygame.Surface, camera: Camera):
        """Draw enemy on screen"""
        if not self.active:
            return
        
        screen_rect = camera.apply(self.rect)
        
        # Draw enemy body
        pygame.draw.rect(screen, self.color, screen_rect)
        
        # Draw direction indicator (simple face)
        face_x = screen_rect.centerx + (5 if self.direction > 0 else -5)
        pygame.draw.circle(screen, WHITE, (face_x, screen_rect.y + 10), 3)
        
        # Draw health bar
        if self.health < self.max_health:
            health_bar_width = 40
            health_bar_height = 6
            health_percentage = self.health / self.max_health
            
            # Background
            health_bg_rect = pygame.Rect(
                screen_rect.centerx - health_bar_width // 2,
                screen_rect.y - 15,
                health_bar_width,
                health_bar_height
            )
            pygame.draw.rect(screen, RED, health_bg_rect)
            
            # Foreground
            health_fg_rect = pygame.Rect(
                screen_rect.centerx - health_bar_width // 2,
                screen_rect.y - 15,
                int(health_bar_width * health_percentage),
                health_bar_height
            )
            pygame.draw.rect(screen, GREEN, health_fg_rect)
