"""
Main game class for Fruit Ninja CV
"""
import cv2
import random
import time

from ..cv.hand_tracker import HandTracker
from ..cv.gesture_detector import GestureDetector, Gesture
from .entities import Fruit, Trail
from .config import GameConfig


class FruitNinjaGame:
    """Main game controller"""
    
    def __init__(self, config=None):
        self.config = config or GameConfig()
        self.width = self.config.WINDOW_WIDTH
        self.height = self.config.WINDOW_HEIGHT
        
        # Game state
        self.fruits = []
        self.score = 0
        self.last_spawn = time.time()
        self.running = False
        
        # Components
        self.hand_tracker = HandTracker(
            max_hands=self.config.MAX_HANDS,
            detection_conf=self.config.DETECTION_CONFIDENCE,
            tracking_conf=self.config.TRACKING_CONFIDENCE
        )
        self.gesture_detector = GestureDetector(
            history_size=self.config.GESTURE_HISTORY_SIZE,
            min_velocity=self.config.MIN_SLASH_VELOCITY
        )
        self.trail = Trail(
            max_points=self.config.TRAIL_MAX_POINTS,
            lifetime=self.config.TRAIL_LIFETIME
        )

    def spawn_fruit(self):
        """Spawn a new fruit at the bottom of the screen"""
        x = random.randint(50, self.width - 50)
        y = self.height + 50  # Start below screen
        fruit = Fruit(
            x, y,
            radius=self.config.FRUIT_RADIUS,
            color=self.config.FRUIT_COLOR
        )
        self.fruits.append(fruit)

    def update_physics(self):
        """Update fruit positions and remove off-screen fruits"""
        for fruit in self.fruits:
            fruit.update(self.config.FRUIT_VELOCITY)
        
        # Remove off-screen fruits and sliced fruits
        self.fruits = [f for f in self.fruits if f.alive and not f.is_offscreen()]

    def check_slice(self, gesture):
        """Check if slashing gesture hits any fruits"""
        if gesture == Gesture.NONE:
            return
        
        # Get recent trail points for collision detection
        recent_points = self.trail.get_recent_points(
            self.config.TRAIL_COLLISION_WINDOW
        )
        
        # Check collision between trail and fruits
        for trail_point in recent_points:
            for fruit in self.fruits:
                if fruit.alive and fruit.check_collision(
                    trail_point.x,
                    trail_point.y,
                    self.config.SLICE_THRESHOLD
                ):
                    fruit.alive = False  # Mark fruit as sliced
                    self.score += 1
                    break  # Move to next trail point

    def update_trail(self, fingertip_pos):
        """Add new point to trail and remove expired ones"""
        if fingertip_pos:
            x = int(fingertip_pos[0] * self.width)
            y = int(fingertip_pos[1] * self.height)
            self.trail.add_point(x, y)
        
        self.trail.update()
    
    def draw_trail(self, frame):
        """Draw the slash trail with fading effect"""
        if len(self.trail.points) < 2:
            return
        
        current_time = time.time()
        trail_color = self.config.TRAIL_COLOR
        
        # Draw lines between consecutive points
        for i in range(1, len(self.trail.points)):
            pt1 = self.trail.points[i-1]
            pt2 = self.trail.points[i]
            
            # Calculate alpha for fading effect
            alpha = pt2.get_alpha(current_time)
            
            # Color based on alpha with fading
            color = tuple(int(c * alpha) for c in trail_color)
            thickness = max(1, int(self.config.TRAIL_MAX_THICKNESS * alpha))
            
            cv2.line(frame, (pt1.x, pt1.y), (pt2.x, pt2.y), color, thickness)
    
    def render(self, frame):
        # Draw trail first (behind everything)
        self.draw_trail(frame)
        
        # Draw fruits
        for fruit in self.fruits:
            if fruit.alive:
                cv2.circle(frame, (fruit.x, fruit.y), fruit.radius, fruit.color, -1)
        
        # Draw score
        cv2.putText(frame, f"Score: {self.score}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    def run(self):
        """Main game loop"""
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        
        self.running = True
        print(f"Starting {self.config.WINDOW_TITLE}...")
        print("Press 'q' to quit")

        while self.running:
            ret, frame = cap.read()
            if not ret:
                break

            # Flip for mirror effect
            frame = cv2.flip(frame, 1)

            # Spawn fruit at configured interval
            if time.time() - self.last_spawn > self.config.FRUIT_SPAWN_INTERVAL:
                self.spawn_fruit()
                self.last_spawn = time.time()

            # Process hand
            landmarks = self.hand_tracker.process_frame(frame)
            gesture = self.gesture_detector.update(landmarks)
            
            # Get fingertip position for trail and collision detection
            fingertip_pos = landmarks[8] if landmarks and len(landmarks) > 8 else None
            
            # Update trail
            self.update_trail(fingertip_pos)
            
            # Update game
            self.update_physics()
            self.check_slice(gesture)
            self.render(frame)

            # Debug visualizations
            if self.config.SHOW_HAND_LANDMARKS and landmarks:
                self.hand_tracker.draw_landmarks(frame, landmarks)
            
            if self.config.SHOW_FINGERTIP_MARKER and fingertip_pos:
                fx = int(fingertip_pos[0] * self.width)
                fy = int(fingertip_pos[1] * self.height)
                cv2.circle(frame, (fx, fy), 8, (0, 255, 255), -1)
                    
            # Show gesture status
            if gesture == Gesture.SLASHING:
                cv2.putText(frame, "SLASHING!", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            cv2.imshow(self.config.WINDOW_TITLE, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()

        cap.release()
        cv2.destroyAllWindows()
        print(f"Game Over! Final Score: {self.score}")
        return self.score
    
    def stop(self):
        """Stop the game"""
        self.running = False