"""
Game entities: Fruit, Trail, etc.
"""
import time
from collections import deque


class Fruit:
    """Represents a fruit in the game"""
    
    def __init__(self, x, y, radius=20, color=(0, 255, 255)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.alive = True
    
    def update(self, velocity):
        """Update fruit position"""
        self.y -= velocity
    
    def is_offscreen(self, min_y=-50):
        """Check if fruit is off screen"""
        return self.y < min_y
    
    def check_collision(self, x, y, threshold=20):
        """Check if a point collides with this fruit"""
        if not self.alive:
            return False
        dist = ((self.x - x)**2 + (self.y - y)**2) ** 0.5
        return dist < (self.radius + threshold)


class TrailPoint:
    """Represents a point in the slash trail"""
    
    def __init__(self, x, y, timestamp, lifetime=0.5):
        self.x = x
        self.y = y
        self.timestamp = timestamp
        self.lifetime = lifetime
    
    def is_expired(self, current_time):
        """Check if this trail point has expired"""
        return (current_time - self.timestamp) > self.lifetime
    
    def get_alpha(self, current_time):
        """Get alpha value (0-1) based on age for fading effect"""
        age = current_time - self.timestamp
        return max(0, 1 - (age / self.lifetime))


class Trail:
    """Manages the slash trail"""
    
    def __init__(self, max_points=50, lifetime=0.5):
        self.points = deque(maxlen=max_points)
        self.lifetime = lifetime
    
    def add_point(self, x, y):
        """Add a new point to the trail"""
        self.points.append(TrailPoint(x, y, time.time(), self.lifetime))
    
    def update(self):
        """Remove expired trail points"""
        current_time = time.time()
        while self.points and self.points[0].is_expired(current_time):
            self.points.popleft()
    
    def get_recent_points(self, time_window=0.3):
        """Get trail points within a recent time window"""
        current_time = time.time()
        return [p for p in self.points if (current_time - p.timestamp) <= time_window]
    
    def clear(self):
        """Clear all trail points"""
        self.points.clear()
