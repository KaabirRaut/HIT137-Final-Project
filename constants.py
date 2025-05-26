#!/usr/bin/env python3
"""
Constants and Enums for Wild Defender Game
==========================================

Contains all game constants, colors, and enumerations used throughout the game.
"""

from enum import Enum

# Screen constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
BROWN = (139, 69, 19)
DARK_GREEN = (0, 100, 0)
SKY_BLUE = (135, 206, 235)

# Game states
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    LEVEL_COMPLETE = 5

# Entity types
class EntityType(Enum):
    PLAYER = 1
    ENEMY_SOLDIER = 2
    ENEMY_ARCHER = 3
    BOSS = 4
    PROJECTILE = 5
    COLLECTIBLE = 6
