import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_hands=1, detection_conf=0.7, tracking_conf=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def process_frame(self, frame):
        """
        Returns list of hand landmarks (each landmark = (x, y) normalized [0,1])
        or None if no hand detected.
        """
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        if not results.multi_hand_landmarks:
            return None

        hands = []
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = []
            for lm in hand_landmarks.landmark:
                # Store normalized (x, y) — resolution independent!
                landmarks.append((lm.x, lm.y))
            hands.append(landmarks)
        return hands[0]  # Return first hand only

    def draw_landmarks(self, frame, landmarks):
        """Optional: for debugging"""
        if landmarks:
            h, w = frame.shape[:2]
            for x, y in landmarks:
                px, py = int(x * w), int(y * h)
                cv2.circle(frame, (px, py), 3, (0, 255, 0), -1)