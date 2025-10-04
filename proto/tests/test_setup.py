#!/usr/bin/env python3
"""
Quick validation script to test imports and configuration
"""
import sys


def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from config import GameConfig, DifficultyLevel
        print("✓ config module")
    except Exception as e:
        print(f"✗ config module: {e}")
        return False
    
    try:
        from entities import Fruit, Trail, TrailPoint
        print("✓ entities module")
    except Exception as e:
        print(f"✗ entities module: {e}")
        return False
    
    try:
        from hand_tracker import HandTracker
        print("✓ hand_tracker module")
    except Exception as e:
        print(f"✗ hand_tracker module: {e}")
        return False
    
    try:
        from gesture_detector import GestureDetector, Gesture
        print("✓ gesture_detector module")
    except Exception as e:
        print(f"✗ gesture_detector module: {e}")
        return False
    
    try:
        from fruit_ninja_game import FruitNinjaGame
        print("✓ fruit_ninja_game module")
    except Exception as e:
        print(f"✗ fruit_ninja_game module: {e}")
        return False
    
    return True


def test_configuration():
    """Test configuration setup"""
    print("\nTesting configuration...")
    
    try:
        from config import GameConfig, DifficultyLevel
        
        config = GameConfig()
        assert config.WINDOW_WIDTH == 640
        assert config.WINDOW_HEIGHT == 480
        print("✓ Default config")
        
        easy = DifficultyLevel.EASY
        assert 'spawn_interval' in easy
        assert 'fruit_velocity' in easy
        print("✓ Difficulty levels")
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


def test_game_creation():
    """Test game instantiation"""
    print("\nTesting game creation...")
    
    try:
        from fruit_ninja_game import FruitNinjaGame
        from config import GameConfig
        
        config = GameConfig()
        game = FruitNinjaGame(config)
        
        assert game.width == 640
        assert game.height == 480
        assert game.score == 0
        assert len(game.fruits) == 0
        print("✓ Game instantiation")
        
        return True
    except Exception as e:
        print(f"✗ Game creation failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("  Fruit Ninja CV - Validation")
    print("=" * 50)
    print()
    
    all_passed = True
    
    all_passed &= test_imports()
    all_passed &= test_configuration()
    all_passed &= test_game_creation()
    
    print()
    print("=" * 50)
    if all_passed:
        print("✓ All tests passed!")
        print("=" * 50)
        print()
        print("Ready to run: uv run python main.py")
        return 0
    else:
        print("✗ Some tests failed")
        print("=" * 50)
        return 1


if __name__ == "__main__":
    sys.exit(main())
