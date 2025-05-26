# Side-Scrolling 2D Game - Wolf vs Humans

A comprehensive side-scrolling 2D game built with Pygame featuring a wolf hero fighting against human enemies across multiple levels.

## Game Features

### Core Gameplay
- **Animal Hero**: Play as a wolf with smooth movement, jumping, and shooting abilities
- **Human Enemies**: Fight against soldiers, archers, and powerful boss enemies
- **3 Levels**: Progressive difficulty with unique challenges and boss fights
- **Dynamic Camera**: Smooth camera system that follows the player
- **Health System**: Player and enemy health bars with visual feedback

### Object-Oriented Design
- **Complete OOP Implementation**: Classes, encapsulation, inheritance, and polymorphism
- **Player Class**: Movement, jumping, shooting, health management, lives system
- **Projectile Class**: Physics-based movement, collision detection, damage system
- **Enemy Class**: AI behavior with patrol, chase, and attack states
- **Collectible Class**: Health boosts, extra lives, and power-ups

### Advanced Features
- **Enemy AI**: Sophisticated state machine (Patrol to Chase to Attack)
- **Boss Battles**: Unique boss enemies with special abilities
- **Scoring System**: Points for enemies defeated, collectibles, and level completion
- **Power-ups**: Speed boost, rapid fire, and invincibility collectibles
- **Game States**: Menu, playing, paused, game over, level complete

## Controls

| Action | Keys |
|--------|------|
| Move | WASD or Arrow Keys |
| Jump | Space, Up Arrow, or W |
| Shoot | X |
| Pause | P |
| Restart (Game Over) | R |

## Installation and Running

### Prerequisites
- Python 3.7+
- Virtual environment (recommended)

### Setup
1. **Clone/Download the project**
   ```bash
   cd /path/to/project/directory
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .env
   ```

3. **Activate virtual environment**
   ```bash
   # On macOS/Linux:
   source .env/bin/activate
   
   # On Windows:
   .env\Scripts\activate
   ```

4. **Install Pygame**
   ```bash
   pip install pygame
   ```

5. **Run the game**
   ```bash
   python game.py
   ```

## File Structure

The codebase has been organized into multiple modules for better maintainability:

### Core Modules
- **`game.py`** - Main game class and game loop
- **`player.py`** - Player character with movement, combat, and state management
- **`enemy.py`** - Enemy AI with different types and behaviors
- **`projectile.py`** - Projectile physics and collision system
- **`collectible.py`** - Collectible items (health, lives, power-ups)
- **`camera.py`** - Dynamic camera system that follows the player
- **`utils.py`** - Utility classes like Vector2 for mathematical operations
- **`constants.py`** - Game constants, colors, and enumerations

### Support Files
- **`test_features.py`** - Automated feature verification script
- **`README.md`** - Project documentation
- **`game_original.py`** - Backup of original monolithic implementation

### Running the Game
Each module is self-contained with proper imports. The main entry point is:
```bash
python game.py
```

## Code Structure

### Main Classes

#### Player Class
- **Movement**: WASD/Arrow key controls with smooth acceleration
- **Jumping**: Space/Up/W with gravity and ground collision
- **Shooting**: X key fires projectiles in facing direction
- **Health**: 100 HP with visual health bar
- **Lives**: 3 lives system with respawn mechanics

#### Enemy Class Hierarchy
- **Base Enemy**: Common behavior and properties
- **SoldierEnemy**: Melee combat with patrol behavior
- **ArcherEnemy**: Ranged attacks with strategic positioning
- **BossEnemy**: High health, multiple attack patterns

#### Projectile Class
- **Physics**: Velocity-based movement with collision detection
- **Damage System**: Different damage values for player vs enemy projectiles
- **Visual Effects**: Particle effects on impact

#### Collectible Class
- **HealthCollectible**: Restores player health
- **ExtraLifeCollectible**: Grants additional lives
- **PowerUpCollectible**: Temporary ability enhancements

### Game Systems

#### Camera System
- **Smooth Following**: Dynamic camera that smoothly tracks player
- **Boundary Constraints**: Prevents camera from showing outside level bounds
- **Offset Management**: Proper world-to-screen coordinate conversion

#### AI System
- **State Machine**: Enemies transition between Patrol, Chase, and Attack states
- **Pathfinding**: Basic AI movement toward player when in range
- **Attack Patterns**: Different enemies have unique attack behaviors

#### Physics System
- **Gravity**: Realistic falling mechanics
- **Collision Detection**: Rectangle-based collision for all game objects
- **Ground Detection**: Platform collision for jumping mechanics

## Game Design

### Level Progression
1. **Level 1**: Tutorial level with basic enemies
2. **Level 2**: Increased difficulty with archers
3. **Level 3**: Final challenge with boss enemy

### Scoring System
- **Enemy Defeats**: 100-300 points per enemy
- **Collectibles**: 50-200 points per item
- **Level Completion**: 1000 bonus points
- **Boss Defeats**: 500-1000 points

### Visual Design
- **Color-coded Elements**: Clear visual distinction between game objects
- **Health Bars**: Red health bars with smooth animations
- **UI Elements**: Clean interface with score, lives, and level display
- **Background**: Gradient sky with ground texture

## Technical Implementation

### Performance Optimizations
- **Efficient Collision Detection**: Only check relevant object pairs
- **Sprite Management**: Proper cleanup of destroyed objects
- **Frame Rate Control**: 60 FPS with delta time calculations

### Code Quality
- **Documentation**: Comprehensive docstrings and comments
- **Type Hints**: Python type annotations for better code clarity
- **Error Handling**: Robust error handling for edge cases
- **Modular Design**: Separate classes for different game systems

## Requirements Checklist

**OOP Implementation**
- Classes with proper encapsulation
- Inheritance hierarchy for enemies
- Polymorphism in enemy behaviors

**Player Class**
- Movement (WASD/Arrow keys)
- Jumping (Space/Up/W)
- Shooting (X key)
- Health system (100 HP)
- Lives system (3 lives)

**Projectile Class**
- Physics-based movement
- Speed and damage properties
- Collision detection

**Enemy Class**
- AI behavior system
- Health management
- Movement patterns

**Collectible Class**
- Health boosts
- Extra lives
- Visual feedback

**Game Features**
- 3 levels with boss enemies
- Scoring system
- Health bars
- Game over screen with restart
- Dynamic camera system
