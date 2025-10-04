"""
Leaderboard UI rendering
"""
import cv2
import numpy as np
from typing import List, Dict


class LeaderboardUI:
    """Renders leaderboard overlay on game screen"""
    
    def __init__(self, width: int = 640, height: int = 480):
        self.width = width
        self.height = height
        
        # UI Colors
        self.bg_color = (0, 0, 0)  # Black
        self.header_color = (255, 200, 0)  # Gold
        self.text_color = (255, 255, 255)  # White
        self.highlight_color = (0, 255, 0)  # Green
        self.overlay_alpha = 0.85
        
        # Font settings
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.title_scale = 1.0
        self.text_scale = 0.6
        self.thickness = 2
    
    def draw_leaderboard(self, frame: np.ndarray, scores: List[Dict], 
                         current_player: str = None) -> np.ndarray:
        """
        Draw leaderboard overlay on frame
        
        Args:
            frame: Video frame to draw on
            scores: List of score entries
            current_player: Highlight this player's name
            
        Returns:
            Frame with leaderboard overlay
        """
        # Create semi-transparent overlay
        overlay = frame.copy()
        
        # Calculate leaderboard dimensions
        board_width = 400
        board_height = min(500, 100 + len(scores) * 40)
        x_offset = (self.width - board_width) // 2
        y_offset = (self.height - board_height) // 2
        
        # Draw background rectangle
        cv2.rectangle(
            overlay,
            (x_offset, y_offset),
            (x_offset + board_width, y_offset + board_height),
            self.bg_color,
            -1
        )
        
        # Draw border
        cv2.rectangle(
            overlay,
            (x_offset, y_offset),
            (x_offset + board_width, y_offset + board_height),
            self.header_color,
            3
        )
        
        # Draw title
        title = "LEADERBOARD"
        title_size = cv2.getTextSize(title, self.font, self.title_scale, self.thickness)[0]
        title_x = x_offset + (board_width - title_size[0]) // 2
        title_y = y_offset + 50
        
        cv2.putText(
            overlay,
            title,
            (title_x, title_y),
            self.font,
            self.title_scale,
            self.header_color,
            self.thickness
        )
        
        # Draw header line
        cv2.line(
            overlay,
            (x_offset + 20, y_offset + 70),
            (x_offset + board_width - 20, y_offset + 70),
            self.header_color,
            2
        )
        
        # Draw scores
        y_pos = y_offset + 110
        for idx, entry in enumerate(scores, 1):
            player_name = entry.get('player_name', 'Unknown')
            score = entry.get('score', 0)
            
            # Determine text color
            text_color = self.highlight_color if player_name == current_player else self.text_color
            
            # Draw rank and name
            rank_text = f"{idx}."
            name_text = player_name[:15]  # Truncate long names
            score_text = str(score)
            
            cv2.putText(
                overlay,
                rank_text,
                (x_offset + 30, y_pos),
                self.font,
                self.text_scale,
                text_color,
                1
            )
            
            cv2.putText(
                overlay,
                name_text,
                (x_offset + 70, y_pos),
                self.font,
                self.text_scale,
                text_color,
                1
            )
            
            # Right-align score
            score_size = cv2.getTextSize(score_text, self.font, self.text_scale, 1)[0]
            score_x = x_offset + board_width - 30 - score_size[0]
            
            cv2.putText(
                overlay,
                score_text,
                (score_x, y_pos),
                self.font,
                self.text_scale,
                text_color,
                1
            )
            
            y_pos += 40
        
        # Blend overlay with original frame
        cv2.addWeighted(overlay, self.overlay_alpha, frame, 1 - self.overlay_alpha, 0, frame)
        
        return frame
    
    def draw_score_submission(self, frame: np.ndarray, message: str) -> np.ndarray:
        """
        Draw score submission notification
        
        Args:
            frame: Video frame to draw on
            message: Message to display
            
        Returns:
            Frame with notification
        """
        overlay = frame.copy()
        
        # Calculate box dimensions
        box_width = 400
        box_height = 100
        x_offset = (self.width - box_width) // 2
        y_offset = 50
        
        # Draw background
        cv2.rectangle(
            overlay,
            (x_offset, y_offset),
            (x_offset + box_width, y_offset + box_height),
            self.bg_color,
            -1
        )
        
        # Draw border
        cv2.rectangle(
            overlay,
            (x_offset, y_offset),
            (x_offset + box_width, y_offset + box_height),
            self.highlight_color,
            2
        )
        
        # Draw message
        text_size = cv2.getTextSize(message, self.font, self.text_scale, 1)[0]
        text_x = x_offset + (box_width - text_size[0]) // 2
        text_y = y_offset + (box_height + text_size[1]) // 2
        
        cv2.putText(
            overlay,
            message,
            (text_x, text_y),
            self.font,
            self.text_scale,
            self.highlight_color,
            1
        )
        
        # Blend
        cv2.addWeighted(overlay, 0.9, frame, 0.1, 0, frame)
        
        return frame
