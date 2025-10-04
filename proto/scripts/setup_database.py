#!/usr/bin/env python3
"""
Setup Supabase database table for leaderboard
"""
import sys
import os

# Add parent directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)
os.chdir(project_root)

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    print("=" * 70)
    print("  Supabase Database Setup")
    print("=" * 70)
    print()
    
    # Check credentials
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Error: Supabase credentials not found!")
        print()
        print("Please set up your .env file with:")
        print("  SUPABASE_URL=your_supabase_url")
        print("  SUPABASE_KEY=your_supabase_key")
        print()
        print("Run this to set up credentials:")
        print("  python scripts/setup_supabase.py")
        return 1
    
    print(f"✅ Supabase URL found: {supabase_url[:30]}...")
    print(f"✅ Supabase Key found: {supabase_key[:30]}...")
    print()
    
    # Try to connect
    try:
        from supabase import create_client
        client = create_client(supabase_url, supabase_key)
        print("✅ Successfully connected to Supabase!")
        print()
    except Exception as e:
        print(f"❌ Error connecting to Supabase: {e}")
        return 1
    
    # Instructions for creating the table
    print("=" * 70)
    print("  Database Table Setup Instructions")
    print("=" * 70)
    print()
    print("You need to create the 'leaderboard' table in Supabase.")
    print()
    print("📝 Steps:")
    print("1. Go to your Supabase dashboard: https://app.supabase.com")
    print("2. Select your project")
    print("3. Click 'SQL Editor' in the left sidebar")
    print("4. Click 'New query'")
    print("5. Copy and paste the SQL from: docs/supabase_schema.sql")
    print("6. Click 'Run' or press Ctrl+Enter")
    print()
    print("=" * 70)
    print()
    
    # Show the SQL
    schema_file = os.path.join(project_root, 'docs', 'supabase_schema.sql')
    if os.path.exists(schema_file):
        print("📄 SQL Schema (from docs/supabase_schema.sql):")
        print("=" * 70)
        with open(schema_file, 'r') as f:
            content = f.read()
            # Show first part of schema
            lines = content.split('\n')
            essential_lines = []
            in_table = False
            for line in lines:
                if 'CREATE TABLE' in line and 'leaderboard' in line:
                    in_table = True
                if in_table:
                    essential_lines.append(line)
                    if line.strip().endswith(');'):
                        break
            
            if essential_lines:
                print('\n'.join(essential_lines))
            else:
                # Fallback: show basic schema
                print("""
CREATE TABLE IF NOT EXISTS leaderboard (
  id BIGSERIAL PRIMARY KEY,
  player_name TEXT NOT NULL,
  score INTEGER NOT NULL CHECK (score >= 0),
  difficulty TEXT NOT NULL CHECK (difficulty IN ('easy', 'medium', 'hard')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
                """.strip())
        print("=" * 70)
        print()
    
    # Test if table exists
    print("🔍 Testing if table exists...")
    try:
        response = client.table('leaderboard').select('*').limit(1).execute()
        print("✅ Table 'leaderboard' exists and is accessible!")
        print()
        
        # Check if there are any scores
        count_response = client.table('leaderboard').select('*', count='exact').execute()
        score_count = len(count_response.data) if count_response.data else 0
        
        if score_count > 0:
            print(f"📊 Found {score_count} score(s) in the leaderboard")
            print()
            print("Top 5 scores:")
            top_scores = client.table('leaderboard').select('*').order('score', desc=True).limit(5).execute()
            for idx, entry in enumerate(top_scores.data, 1):
                print(f"  {idx}. {entry['player_name']:20s} - {entry['score']:5d} ({entry['difficulty']})")
        else:
            print("📊 Leaderboard is empty (no scores yet)")
        
        print()
        print("=" * 70)
        print("✅ Setup Complete!")
        print("=" * 70)
        print()
        print("You're ready to play with leaderboard!")
        print("Run: python main.py --player-name 'YourName' --show-leaderboard")
        return 0
        
    except Exception as e:
        print(f"❌ Table 'leaderboard' not found or not accessible")
        print(f"   Error: {e}")
        print()
        print("⚠️  Please create the table using the SQL above")
        print()
        print("After creating the table, run this script again to verify.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
