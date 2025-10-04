"""
Fruit Ninja CV - A computer vision-based Fruit Ninja game
"""

__version__ = "0.1.0"
__author__ = "bigalex95"

from .fruit_ninja_game import FruitNinjaGame
from .config import GameConfig, DifficultyLevel
from .gesture_detector import GestureDetector, Gesture
from .hand_tracker import HandTracker

__all__ = [
    "FruitNinjaGame",
    "GameConfig",
    "DifficultyLevel",
    "GestureDetector",
    "Gesture",
    "HandTracker",
]
