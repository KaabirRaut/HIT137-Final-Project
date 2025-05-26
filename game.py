#!/usr/bin/env python3
"""
Wild Defender - A Side-Scrolling 2D Game
=========================================

A game featuring an animal hero (wolf) defending against human enemies
across 3 progressively challenging levels with boss battles.

Author: KABIR RAUT
Features:
- Player class with movement, jumping, shooting, health, and lives
- Projectile system with damage mechanics
- Enemy AI with different types and behaviors
- Collectible items (health boosts, extra lives, power-ups)
- 3 levels with increasing difficulty and boss enemies
- Scoring system based on enemies defeated and collectibles
- Health bars for players and enemies
- Game over screen with restart functionality
- Dynamic camera following the player smoothly
"""

import pygame
import sys
from typing import List

# Import our custom modules
from constants import *
from utils import Vector2
from camera import Camera
from projectile import Projectile
from collectible import Collectible
from enemy import Enemy
from player import Player

# Initialize Pygame
pygame.init()

class Game:
    """Main game class managing all game systems"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Wild Defender - Animal vs Humans")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 72)
        
        # Game state
        self.state = GameState.MENU
        self.current_level = 1
        self.max_level = 3
        self.score = 0
        self.paused = False
        
        # World settings
        self.world_width = 3000
        self.world_height = 800
        
        # Initialize camera
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Initialize game objects
        self.player = Player(100, 600)
        self.enemies: List[Enemy] = []
        self.projectiles: List[Projectile] = []
        self.collectibles: List[Collectible] = []
        
        # Level data
        self.level_data = {
            1: {
                'enemies': [
                    {'type': 'soldier', 'x': 400, 'y': 600},
                    {'type': 'soldier', 'x': 800, 'y': 600},
                    {'type': 'archer', 'x': 1200, 'y': 600},
                    {'type': 'soldier', 'x': 1600, 'y': 600},
                ],
                'collectibles': [
                    {'type': 'health', 'x': 300, 'y': 570},
                    {'type': 'power', 'x': 1000, 'y': 570},
                    {'type': 'life', 'x': 1800, 'y': 570},
                ],
                'boss': {'type': 'boss', 'x': 2500, 'y': 600}
            },
            2: {
                'enemies': [
                    {'type': 'archer', 'x': 300, 'y': 600},
                    {'type': 'soldier', 'x': 600, 'y': 600},
                    {'type': 'archer', 'x': 900, 'y': 600},
                    {'type': 'soldier', 'x': 1200, 'y': 600},
                    {'type': 'archer', 'x': 1500, 'y': 600},
                    {'type': 'soldier', 'x': 1800, 'y': 600},
                ],
                'collectibles': [
                    {'type': 'health', 'x': 250, 'y': 570},
                    {'type': 'power', 'x': 750, 'y': 570},
                    {'type': 'health', 'x': 1350, 'y': 570},
                    {'type': 'life', 'x': 2000, 'y': 570},
                ],
                'boss': {'type': 'boss', 'x': 2700, 'y': 600}
            },
            3: {
                'enemies': [
                    {'type': 'soldier', 'x': 250, 'y': 600},
                    {'type': 'archer', 'x': 450, 'y': 600},
                    {'type': 'soldier', 'x': 650, 'y': 600},
                    {'type': 'archer', 'x': 850, 'y': 600},
                    {'type': 'soldier', 'x': 1050, 'y': 600},
                    {'type': 'archer', 'x': 1250, 'y': 600},
                    {'type': 'soldier', 'x': 1450, 'y': 600},
                    {'type': 'archer', 'x': 1650, 'y': 600},
                ],
                'collectibles': [
                    {'type': 'health', 'x': 200, 'y': 570},
                    {'type': 'power', 'x': 600, 'y': 570},
                    {'type': 'health', 'x': 1100, 'y': 570},
                    {'type': 'power', 'x': 1600, 'y': 570},
                    {'type': 'life', 'x': 2200, 'y': 570},
                ],
                'boss': {'type': 'boss', 'x': 2800, 'y': 600}
            }
        }
        
        self.load_level(self.current_level)
    
    def load_level(self, level: int):
        """Load a specific level"""
        if level > self.max_level:
            # Game completed
            self.state = GameState.GAME_OVER
            return
        
        self.current_level = level
        data = self.level_data[level]
        
        # Clear existing objects
        self.enemies.clear()
        self.projectiles.clear()
        self.collectibles.clear()
        
        # Reset player position
        self.player.position = Vector2(100, 600)
        
        # Load enemies
        for enemy_data in data['enemies']:
            enemy = Enemy(enemy_data['x'], enemy_data['y'], enemy_data['type'])
            self.enemies.append(enemy)
        
        # Load boss
        boss_data = data['boss']
        boss = Enemy(boss_data['x'], boss_data['y'], boss_data['type'])
        self.enemies.append(boss)
        
        # Load collectibles
        for collectible_data in data['collectibles']:
            collectible = Collectible(collectible_data['x'], collectible_data['y'], collectible_data['type'])
            self.collectibles.append(collectible)
    
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    if event.key == pygame.K_RETURN:
                        self.state = GameState.PLAYING
                        self.load_level(1)
                
                elif self.state == GameState.PLAYING:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.PAUSED
                    elif event.key == pygame.K_x:
                        # Shoot
                        self.player.shoot(self.projectiles)
                
                elif self.state == GameState.PAUSED:
                    if event.key == pygame.K_ESCAPE:
                        self.state = GameState.PLAYING
                
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_r:
                        # Restart game
                        self.restart_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                
                elif self.state == GameState.LEVEL_COMPLETE:
                    if event.key == pygame.K_RETURN:
                        self.load_level(self.current_level + 1)
                        self.state = GameState.PLAYING
        
        return True
    
    def restart_game(self):
        """Restart the game"""
        self.current_level = 1
        self.score = 0
        self.player = Player(100, 600)
        self.load_level(1)
        self.state = GameState.PLAYING
    
    def update(self, dt: float):
        """Update all game systems"""
        if self.state == GameState.PLAYING:
            keys_pressed = pygame.key.get_pressed()
            
            # Update player
            self.player.update(dt, keys_pressed)
            
            # Update camera to follow player
            self.camera.update(self.player.position.x, self.player.position.y, 
                             self.world_width, self.world_height)
            
            # Update enemies
            for enemy in self.enemies[:]:
                enemy.update(dt, self.player.position, self.projectiles)
                if not enemy.active:
                    self.enemies.remove(enemy)
                    self.score += 100  # Points for defeating enemy
            
            # Update projectiles
            for projectile in self.projectiles[:]:
                projectile.update(dt)
                if not projectile.active:
                    self.projectiles.remove(projectile)
            
            # Update collectibles
            for collectible in self.collectibles[:]:
                collectible.update(dt)
                if not collectible.active:
                    self.collectibles.remove(collectible)
            
            # Check collisions
            self.check_collisions()
            
            # Check level completion
            if not self.enemies:
                self.state = GameState.LEVEL_COMPLETE
                self.score += 1000  # Bonus for completing level
            
            # Check game over
            if self.player.lives <= 0:
                self.state = GameState.GAME_OVER
    
    def check_collisions(self):
        """Check all collision interactions"""
        # Player projectiles vs enemies
        for projectile in self.projectiles[:]:
            if projectile.owner_type == EntityType.PLAYER:
                for enemy in self.enemies[:]:
                    if enemy.active and projectile.check_collision(enemy.rect):
                        if enemy.take_damage(projectile.damage):
                            self.score += 50  # Bonus for hitting enemy
                        projectile.active = False
                        break
        
        # Enemy projectiles vs player
        for projectile in self.projectiles[:]:
            if (projectile.owner_type in [EntityType.ENEMY_SOLDIER, EntityType.ENEMY_ARCHER] and
                projectile.check_collision(self.player.rect)):
                self.player.take_damage(projectile.damage)
                projectile.active = False
        
        # Player vs collectibles
        for collectible in self.collectibles[:]:
            if collectible.active and collectible.rect.colliderect(self.player.rect):
                if collectible.type == 'health':
                    self.player.heal(collectible.value)
                    self.score += 10
                elif collectible.type == 'life':
                    self.player.add_life()
                    self.score += 50
                elif collectible.type == 'power':
                    self.player.activate_power_up()
                    self.score += 25
                collectible.collect()
        
        # Player vs enemies (melee damage)
        for enemy in self.enemies:
            if enemy.active and enemy.rect.colliderect(self.player.rect):
                # Simple melee damage (once per second)
                current_time = pygame.time.get_ticks() / 1000.0
                if not hasattr(enemy, 'last_melee_time'):
                    enemy.last_melee_time = 0
                
                if current_time - enemy.last_melee_time >= 1.0:
                    self.player.take_damage(enemy.damage // 2)
                    enemy.last_melee_time = current_time
    
    def draw_background(self):
        """Draw game background"""
        # Sky gradient
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(135 * (1 - color_ratio) + 255 * color_ratio)
            g = int(206 * (1 - color_ratio) + 255 * color_ratio)
            b = int(235 * (1 - color_ratio) + 255 * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Ground
        ground_y = SCREEN_HEIGHT - 200
        pygame.draw.rect(self.screen, BROWN, (0, ground_y, SCREEN_WIDTH, 200))
        
        # Simple hills in background
        for i in range(5):
            hill_x = i * 300 - int(self.camera.x * 0.5) % 1500
            hill_y = ground_y - 50
            pygame.draw.circle(self.screen, DARK_GREEN, (hill_x, hill_y), 80)
    
    def draw_ui(self):
        """Draw user interface elements"""
        # Health bar
        health_percentage = self.player.health / self.player.max_health
        health_bar_width = 200
        health_bar_height = 20
        
        # Health bar background
        health_bg_rect = pygame.Rect(20, 20, health_bar_width, health_bar_height)
        pygame.draw.rect(self.screen, RED, health_bg_rect)
        
        # Health bar foreground
        health_fg_rect = pygame.Rect(20, 20, int(health_bar_width * health_percentage), health_bar_height)
        pygame.draw.rect(self.screen, GREEN, health_fg_rect)
        
        # Health text
        health_text = self.small_font.render(f"Health: {self.player.health}/{self.player.max_health}", True, WHITE)
        self.screen.blit(health_text, (20, 45))
        
        # Lives
        lives_text = self.small_font.render(f"Lives: {self.player.lives}", True, WHITE)
        self.screen.blit(lives_text, (20, 70))
        
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH - 200, 20))
        
        # Level
        level_text = self.font.render(f"Level: {self.current_level}", True, WHITE)
        self.screen.blit(level_text, (SCREEN_WIDTH - 200, 60))
        
        # Power-up indicator
        if self.player.has_power_up:
            power_text = self.small_font.render(f"POWER UP! {self.player.power_up_timer:.1f}s", True, YELLOW)
            self.screen.blit(power_text, (SCREEN_WIDTH // 2 - 100, 20))
        
        # Controls hint
        controls_text = self.small_font.render("Controls: WASD/Arrows to move, X to shoot, ESC to pause", True, WHITE)
        self.screen.blit(controls_text, (20, SCREEN_HEIGHT - 30))
    
    def draw_menu(self):
        """Draw main menu"""
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.large_font.render("WILD DEFENDER", True, GREEN)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font.render("Animal Hero vs Human Enemies", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 80))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Instructions
        instructions = [
            "You are a wolf defending the wilderness from human invaders!",
            "",
            "CONTROLS:",
            "WASD or Arrow Keys - Move",
            "X - Shoot",
            "ESC - Pause",
            "",
            "Collect power-ups and defeat all enemies to advance!",
            "",
            "Press ENTER to start"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 25))
            self.screen.blit(text, text_rect)
    
    def draw_pause_screen(self):
        """Draw pause screen overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.large_font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_text, pause_rect)
        
        # Instructions
        instruction_text = self.font.render("Press ESC to resume", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(instruction_text, instruction_rect)
    
    def draw_game_over(self):
        """Draw game over screen"""
        self.screen.fill(BLACK)
        
        # Game over text
        if self.current_level > self.max_level:
            # Game completed
            game_over_text = self.large_font.render("CONGRATULATIONS!", True, GREEN)
            subtitle_text = self.font.render("You have defended the wilderness!", True, WHITE)
        else:
            # Game over
            game_over_text = self.large_font.render("GAME OVER", True, RED)
            subtitle_text = self.font.render("The wilderness has fallen...", True, WHITE)
        
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(game_over_text, game_over_rect)
        
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 80))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Final score
        score_text = self.font.render(f"Final Score: {self.score}", True, YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        # Instructions
        restart_text = self.small_font.render("Press R to restart or ESC to quit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_level_complete(self):
        """Draw level complete screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Level complete text
        complete_text = self.large_font.render("LEVEL COMPLETE!", True, GREEN)
        complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(complete_text, complete_rect)
        
        # Instructions
        if self.current_level < self.max_level:
            instruction_text = self.font.render("Press ENTER for next level", True, WHITE)
        else:
            instruction_text = self.font.render("Press ENTER to finish game", True, WHITE)
        
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(instruction_text, instruction_rect)
    
    def draw(self):
        """Main draw method"""
        if self.state == GameState.MENU:
            self.draw_menu()
        
        elif self.state in [GameState.PLAYING, GameState.PAUSED, GameState.LEVEL_COMPLETE]:
            # Draw background
            self.draw_background()
            
            # Draw game objects
            self.player.draw(self.screen, self.camera)
            
            for enemy in self.enemies:
                enemy.draw(self.screen, self.camera)
            
            for projectile in self.projectiles:
                projectile.draw(self.screen, self.camera)
            
            for collectible in self.collectibles:
                collectible.draw(self.screen, self.camera)
            
            # Draw UI
            self.draw_ui()
            
            # Draw overlays
            if self.state == GameState.PAUSED:
                self.draw_pause_screen()
            elif self.state == GameState.LEVEL_COMPLETE:
                self.draw_level_complete()
        
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            # Handle events
            running = self.handle_events()
            
            # Update game
            self.update(dt)
            
            # Draw everything
            self.draw()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
