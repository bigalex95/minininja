# 🚨 Quick Fix: Database Table Not Found

## The Problem

Your Supabase credentials are correct, but the `leaderboard` table doesn't exist in your database yet.

## The Solution (2 minutes)

### Step 1: Go to Supabase Dashboard

Open: **https://app.supabase.com**

### Step 2: Open SQL Editor

1. Click your project
2. Click **"SQL Editor"** in the left sidebar
3. Click **"+ New query"**

### Step 3: Copy This SQL

```sql
CREATE TABLE IF NOT EXISTS leaderboard (
  id BIGSERIAL PRIMARY KEY,
  player_name TEXT NOT NULL,
  score INTEGER NOT NULL CHECK (score >= 0),
  difficulty TEXT NOT NULL CHECK (difficulty IN ('easy', 'medium', 'hard')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_leaderboard_score
ON leaderboard(score DESC);

CREATE INDEX IF NOT EXISTS idx_leaderboard_difficulty
ON leaderboard(difficulty);

-- Enable Row Level Security
ALTER TABLE leaderboard ENABLE ROW LEVEL SECURITY;

-- Allow anyone to read
CREATE POLICY "Enable read access for all users"
ON leaderboard FOR SELECT
USING (true);

-- Allow anyone to insert scores
CREATE POLICY "Enable insert access for all users"
ON leaderboard FOR INSERT
WITH CHECK (true);
```

### Step 4: Run the SQL

- Click **"Run"** button (or press `Ctrl+Enter`)
- You should see: ✅ **"Success. No rows returned"**

### Step 5: Verify Setup

Run this in your terminal:

```bash
python scripts/setup_database.py
```

You should now see: ✅ **"Table 'leaderboard' exists and is accessible!"**

### Step 6: Play!

```bash
python main.py --player-name "YourName" --show-leaderboard
```

## Troubleshooting

### "Table already exists" Error

That's fine! The table is already there. Just verify with:

```bash
python scripts/setup_database.py
```

### "Permission denied" Error

Make sure you're using the **anon/public key** (not the service_role key) in your `.env` file.

### Still Not Working?

1. Check you're in the right Supabase project
2. Refresh the Supabase page after creating the table
3. Try viewing the table in **Table Editor** → should see `leaderboard` table

---

**Need the full schema?** See `docs/supabase_schema.sql` for the complete version with all features.
