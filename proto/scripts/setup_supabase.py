#!/usr/bin/env python3
"""
Interactive Supabase setup helper
Guides users through the setup process
"""
import sys
import os

# Add parent directory to path if running from scripts/
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)
os.chdir(project_root)

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def print_step(num, text):
    print(f"\n📋 Step {num}: {text}")
    print("-" * 70)

def main():
    print_header("Fruit Ninja CV - Supabase Setup Helper")
    
    print("This helper will guide you through setting up Supabase for the leaderboard.")
    print("\nYou'll need:")
    print("  • A Supabase account (free)")
    print("  • ~5 minutes of your time")
    print("\nPress Enter to continue...")
    input()
    
    # Step 1: Create account
    print_step(1, "Create Supabase Account")
    print("1. Go to: https://supabase.com")
    print("2. Click 'Start your project'")
    print("3. Sign up with GitHub, Google, or Email")
    print("\nHave you created your account? (y/n): ", end="")
    if input().lower() != 'y':
        print("Please create an account first, then run this script again.")
        return
    
    # Step 2: Create project
    print_step(2, "Create New Project")
    print("1. Click 'New Project'")
    print("2. Fill in:")
    print("   • Name: fruit-ninja-cv (or your choice)")
    print("   • Database Password: Create a strong password")
    print("   • Region: Choose closest to your location")
    print("3. Click 'Create new project'")
    print("4. Wait ~2 minutes for setup to complete")
    print("\nIs your project created and ready? (y/n): ", end="")
    if input().lower() != 'y':
        print("Please wait for the project to finish setting up, then run this script again.")
        return
    
    # Step 3: Create table
    print_step(3, "Create Leaderboard Table")
    print("1. In your project dashboard, click 'SQL Editor' in the left sidebar")
    print("2. Click 'New query'")
    print("3. Copy the SQL from: docs/supabase_schema.sql")
    print("4. Paste it into the SQL editor")
    print("5. Click 'Run' or press Ctrl+Enter")
    print("\nYou should see: 'Success. No rows returned'")
    print("\nHave you created the table? (y/n): ", end="")
    if input().lower() != 'y':
        print("Please create the table first, then run this script again.")
        return
    
    # Step 4: Get credentials
    print_step(4, "Get API Credentials")
    print("1. Click the ⚙️ 'Project Settings' icon (bottom left)")
    print("2. Click 'API' in the sidebar")
    print("3. Find these two values:")
    print("   • Project URL")
    print("   • anon/public key")
    print("\nReady to enter your credentials? (y/n): ", end="")
    if input().lower() != 'y':
        print("Come back when you have your credentials ready!")
        return
    
    # Get credentials
    print("\nEnter your Supabase URL (e.g., https://xxxxx.supabase.co):")
    supabase_url = input("> ").strip()
    
    print("\nEnter your Supabase anon/public key:")
    print("(It's a long string starting with 'eyJ...')")
    supabase_key = input("> ").strip()
    
    # Validate inputs
    if not supabase_url.startswith('https://') or 'supabase.co' not in supabase_url:
        print("⚠️  Warning: URL doesn't look right. Make sure it starts with https:// and contains supabase.co")
    
    if not supabase_key.startswith('eyJ'):
        print("⚠️  Warning: Key doesn't look right. Make sure you copied the anon/public key, not the service_role key.")
    
    # Write to .env
    print_step(5, "Creating .env File")
    
    env_content = f"""# Supabase Configuration
SUPABASE_URL={supabase_url}
SUPABASE_KEY={supabase_key}

# Game Configuration (optional overrides)
# WINDOW_WIDTH=640
# WINDOW_HEIGHT=480
# DEBUG_MODE=false
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        print("\nManually create .env with these contents:")
        print(env_content)
        return
    
    # Test connection
    print_step(6, "Testing Connection")
    print("Let's test if everything works...")
    
    try:
        os.environ['SUPABASE_URL'] = supabase_url
        os.environ['SUPABASE_KEY'] = supabase_key
        
        from src.leaderboard import Leaderboard
        
        lb = Leaderboard()
        print("✅ Connection successful!")
        
        # Try to fetch leaderboard
        print("\nFetching current leaderboard...")
        scores = lb.get_top_scores(limit=5)
        
        if scores:
            print(f"✅ Found {len(scores)} scores in leaderboard!")
        else:
            print("✅ Leaderboard is empty (no scores yet)")
        
    except Exception as e:
        print(f"⚠️  Connection test failed: {e}")
        print("\nThis might be normal if you just set everything up.")
        print("Try running the game to test it properly.")
    
    # Success!
    print_header("Setup Complete! 🎉")
    
    print("Your leaderboard is ready to use!")
    print("\nNext steps:")
    print("  1. Run the game:")
    print("     python main.py --player-name 'YourName' --show-leaderboard")
    print("\n  2. Play and set some high scores!")
    print("\n  3. View your scores in Supabase:")
    print(f"     {supabase_url}/project/default/editor")
    print("\nHave fun! 🍉🔪")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        print("\nFor manual setup, see: docs/SUPABASE_SETUP.md")
