#!/usr/bin/env python3
"""
Fruit Ninja CV - A computer vision-based Fruit Ninja game
Main entry point for the application
"""
import argparse
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from src.core.game import FruitNinjaGame
from src.core.config import GameConfig, DifficultyLevel
from src.leaderboard import Leaderboard
from src.ui import LeaderboardUI


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Fruit Ninja CV - Slice fruits with hand gestures!',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Start with default settings
  %(prog)s --difficulty hard  # Start with hard difficulty
  %(prog)s --debug            # Enable debug mode with landmarks
  %(prog)s --width 1280 --height 720  # Custom resolution
        """
    )
    
    parser.add_argument(
        '--difficulty',
        choices=['easy', 'medium', 'hard'],
        default='medium',
        help='Game difficulty level (default: medium)'
    )
    
    parser.add_argument(
        '--width',
        type=int,
        default=640,
        help='Window width in pixels (default: 640)'
    )
    
    parser.add_argument(
        '--height',
        type=int,
        default=480,
        help='Window height in pixels (default: 480)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode (show hand landmarks)'
    )
    
    parser.add_argument(
        '--no-trail',
        action='store_true',
        help='Disable slash trail visualization'
    )
    
    parser.add_argument(
        '--player-name',
        type=str,
        default='Player',
        help='Player name for leaderboard (default: Player)'
    )
    
    parser.add_argument(
        '--show-leaderboard',
        action='store_true',
        help='Show leaderboard at game end'
    )
    
    return parser.parse_args()


def create_config(args):
    """Create game configuration from arguments"""
    config = GameConfig()
    
    # Apply window size
    config.WINDOW_WIDTH = args.width
    config.WINDOW_HEIGHT = args.height
    
    # Apply difficulty settings
    difficulty_map = {
        'easy': DifficultyLevel.EASY,
        'medium': DifficultyLevel.MEDIUM,
        'hard': DifficultyLevel.HARD
    }
    
    difficulty = difficulty_map[args.difficulty]
    config.FRUIT_SPAWN_INTERVAL = difficulty['spawn_interval']
    config.FRUIT_VELOCITY = difficulty['fruit_velocity']
    config.MIN_SLASH_VELOCITY = difficulty['min_velocity']
    
    # Apply debug settings
    if args.debug:
        config.DEBUG_MODE = True
        config.SHOW_HAND_LANDMARKS = True
        config.SHOW_FINGERTIP_MARKER = True
    
    # Trail settings
    if args.no_trail:
        config.TRAIL_LIFETIME = 0.1  # Very short trail
    
    return config


def main():
    """Main entry point"""
    args = parse_args()
    
    print("=" * 50)
    print("  Fruit Ninja CV - Hand Gesture Edition")
    print("=" * 50)
    print(f"Difficulty: {args.difficulty.upper()}")
    print(f"Resolution: {args.width}x{args.height}")
    print(f"Debug Mode: {'ON' if args.debug else 'OFF'}")
    print(f"Player: {args.player_name}")
    print("=" * 50)
    print()
    
    try:
        config = create_config(args)
        game = FruitNinjaGame(config=config)
        final_score = game.run()
        
        # Handle leaderboard submission
        if final_score is not None and final_score > 0:
            print(f"\n🎉 Final Score: {final_score}")
            
            # Try to submit to leaderboard
            try:
                leaderboard = Leaderboard()
                if leaderboard.submit_score(args.player_name, final_score, args.difficulty):
                    print("✅ Score submitted to leaderboard!")
                    
                    # Show top scores if requested
                    if args.show_leaderboard:
                        print("\n" + "=" * 50)
                        print("  TOP 10 SCORES")
                        print("=" * 50)
                        top_scores = leaderboard.get_top_scores(limit=10, difficulty=args.difficulty)
                        for idx, entry in enumerate(top_scores, 1):
                            player = entry['player_name']
                            score = entry['score']
                            marker = "👑" if player == args.player_name else "  "
                            print(f"{marker} {idx:2d}. {player:20s} - {score:5d}")
                else:
                    print("⚠️  Could not submit score to leaderboard")
            except Exception as e:
                print(f"⚠️  Leaderboard unavailable: {e}")
                print(f"   Make sure to set up the database table. Run: python scripts/setup_database.py")
        
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}", file=sys.stderr)
        if args.debug:
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()
