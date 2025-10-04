#!/usr/bin/env python3
"""
Quick test script to verify the project structure and imports
"""
import sys
import os

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from src.core import GameConfig, DifficultyLevel, Fruit, Trail, FruitNinjaGame
        print("✅ Core modules imported successfully")
    except Exception as e:
        print(f"❌ Core modules import failed: {e}")
        return False
    
    try:
        from src.cv import HandTracker, GestureDetector, Gesture
        print("✅ CV modules imported successfully")
    except Exception as e:
        print(f"❌ CV modules import failed: {e}")
        return False
    
    try:
        from src.ui import LeaderboardUI
        print("✅ UI modules imported successfully")
    except Exception as e:
        print(f"❌ UI modules import failed: {e}")
        return False
    
    # Test leaderboard (may fail if no .env)
    try:
        from src.leaderboard import Leaderboard
        print("✅ Leaderboard module imported successfully")
        
        # Try to initialize (will fail without credentials)
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            if os.getenv('SUPABASE_URL') and os.getenv('SUPABASE_KEY'):
                lb = Leaderboard()
                print("✅ Leaderboard initialized with credentials")
            else:
                print("⚠️  Leaderboard module works but no credentials in .env")
        except Exception as e:
            print(f"⚠️  Leaderboard init failed (expected if no .env): {e}")
    except Exception as e:
        print(f"❌ Leaderboard module import failed: {e}")
        return False
    
    return True

def test_structure():
    """Verify directory structure"""
    print("\nChecking project structure...")
    
    # Add parent directory to path if running from tests/
    if os.path.basename(os.getcwd()) == 'tests':
        sys.path.insert(0, os.path.dirname(os.getcwd()))
        os.chdir(os.path.dirname(os.getcwd()))
    
    required_dirs = [
        'src',
        'src/core',
        'src/cv',
        'src/leaderboard',
        'src/ui',
        'data',
        'docs',
        'tests',
        'scripts'
    ]
    
    required_files = [
        'main.py',
        'pyproject.toml',
        '.env.example',
        '.gitignore',
        'README.md',
        'SETUP.md',
        'scripts/setup.sh',
        'scripts/setup_supabase.py',
        'docs/supabase_schema.sql',
        'docs/SUPABASE_SETUP.md',
        'docs/PROJECT_STRUCTURE.md',
        'docs/CLEANUP_SUMMARY.md',
        'tests/test_structure.py'
    ]
    
    all_good = True
    
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ missing")
            all_good = False
    
    for file_path in required_files:
        if os.path.isfile(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} missing")
            all_good = False
    
    return all_good

def main():
    print("=" * 60)
    print("Fruit Ninja CV - Structure & Import Test")
    print("=" * 60)
    print()
    
    structure_ok = test_structure()
    print()
    imports_ok = test_imports()
    
    print()
    print("=" * 60)
    if structure_ok and imports_ok:
        print("✅ All tests passed!")
        print()
        print("Next steps:")
        print("1. Set up Supabase credentials in .env")
        print("2. Run: python main.py --player-name 'YourName'")
    else:
        print("❌ Some tests failed. Check the output above.")
        return 1
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
