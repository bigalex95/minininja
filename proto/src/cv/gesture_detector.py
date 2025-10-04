from collections import deque
from enum import Enum

class Gesture(Enum):
    NONE = 0
    SLASHING = 1  # Any slashing motion detected

class GestureDetector:
    def __init__(self, history_size=10, min_velocity=0.03):
        # Store last N fingertip positions (normalized coordinates)
        self.history = deque(maxlen=history_size)
        self.min_velocity = min_velocity  # normalized units/frame

    def update(self, landmarks):
        """
        landmarks: list of (x, y) from HandTracker (index 8 = index fingertip)
        Returns: Gesture
        """
        if not landmarks or len(landmarks) < 9:
            self.history.clear()
            return Gesture.NONE

        fingertip = landmarks[8]  # MediaPipe index for index fingertip
        self.history.append(fingertip)

        if len(self.history) < 2:
            return Gesture.NONE

        # Compute average velocity over history
        dx = self.history[-1][0] - self.history[0][0]
        dy = self.history[-1][1] - self.history[0][1]
        frames = len(self.history) - 1
        vx, vy = dx / frames, dy / frames

        speed = (vx**2 + vy**2) ** 0.5
        if speed < self.min_velocity:
            return Gesture.NONE

        # Any fast motion is a slashing gesture
        return Gesture.SLASHING
    
    def get_trail_positions(self):
        """Returns the history of positions for drawing trail"""
        return list(self.history)