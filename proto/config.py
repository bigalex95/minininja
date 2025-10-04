"""
Game configuration settings
"""

class GameConfig:
    """Configuration for the Fruit Ninja game"""
    
    # Display settings
    WINDOW_WIDTH = 640
    WINDOW_HEIGHT = 480
    WINDOW_TITLE = "Fruit Ninja CV"
    FPS = 30
    
    # Game mechanics
    FRUIT_SPAWN_INTERVAL = 1.5  # seconds
    FRUIT_RADIUS = 20
    FRUIT_VELOCITY = 5  # pixels per frame
    FRUIT_COLOR = (0, 255, 255)  # Yellow in BGR
    
    # Hand tracking settings
    MAX_HANDS = 1
    DETECTION_CONFIDENCE = 0.7
    TRACKING_CONFIDENCE = 0.7
    
    # Gesture detection settings
    GESTURE_HISTORY_SIZE = 10
    MIN_SLASH_VELOCITY = 0.03  # normalized units/frame
    
    # Trail settings
    TRAIL_MAX_POINTS = 50
    TRAIL_LIFETIME = 0.5  # seconds
    TRAIL_COLOR = (255, 255, 0)  # Cyan in BGR
    TRAIL_MAX_THICKNESS = 8
    TRAIL_COLLISION_WINDOW = 0.3  # seconds
    
    # Collision detection
    SLICE_THRESHOLD = 20  # pixels from trail to fruit
    
    # Debug settings
    DEBUG_MODE = False
    SHOW_HAND_LANDMARKS = False
    SHOW_FINGERTIP_MARKER = True


class DifficultyLevel:
    """Predefined difficulty levels"""
    
    EASY = {
        'spawn_interval': 2.0,
        'fruit_velocity': 3,
        'min_velocity': 0.05
    }
    
    MEDIUM = {
        'spawn_interval': 1.5,
        'fruit_velocity': 5,
        'min_velocity': 0.03
    }
    
    HARD = {
        'spawn_interval': 1.0,
        'fruit_velocity': 7,
        'min_velocity': 0.02
    }
