"""
Core game logic and entities
"""

from .config import GameConfig, DifficultyLevel
from .entities import Fruit, Trail, TrailPoint
from .game import FruitNinjaGame

__all__ = [
    'GameConfig',
    'DifficultyLevel',
    'Fruit',
    'Trail',
    'TrailPoint',
    'FruitNinjaGame',
]
