# Supabase Leaderboard Setup Guide

## Quick Start

### 1. Create Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Sign up or log in
3. Click "New Project"
4. Fill in:
   - **Name**: `fruit-ninja-cv` (or your preferred name)
   - **Database Password**: Create a strong password
   - **Region**: Choose closest to you
5. Wait for project to initialize (~2 minutes)

### 2. Set Up Database Table

1. In your Supabase dashboard, go to **SQL Editor**
2. Copy and paste the contents of `supabase_schema.sql`
3. Click **Run** or press `Ctrl+Enter`
4. Verify the table was created in **Table Editor** → `leaderboard`

### 3. Get API Credentials

1. Go to **Project Settings** (gear icon)
2. Click **API** in the sidebar
3. Copy these values:
   - **Project URL** → This is your `SUPABASE_URL`
   - **anon/public key** → This is your `SUPABASE_KEY`

### 4. Configure Your App

1. Copy `.env.example` to `.env`:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your credentials:
   ```env
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

### 5. Test the Connection

Run the game with leaderboard:

```bash
python main.py --player-name "TestPlayer" --show-leaderboard
```

## Table Schema

```sql
leaderboard
├── id (BIGSERIAL, PRIMARY KEY)
├── player_name (TEXT, NOT NULL)
├── score (INTEGER, NOT NULL, CHECK >= 0)
├── difficulty (TEXT, NOT NULL, CHECK IN ('easy', 'medium', 'hard'))
└── created_at (TIMESTAMP WITH TIME ZONE, DEFAULT NOW())
```

## Row Level Security (RLS)

The schema automatically enables RLS with these policies:

- ✅ **Anyone can READ** scores (view leaderboard)
- ✅ **Anyone can INSERT** scores (submit scores)
- ❌ **No one can UPDATE** scores (prevent cheating)
- ❌ **No one can DELETE** scores (maintain history)

## Optional: View Leaderboard Data

### In Supabase Dashboard

1. Go to **Table Editor**
2. Click `leaderboard` table
3. View all scores, filter, and sort

### Using SQL

```sql
-- Top 10 overall
SELECT player_name, score, difficulty, created_at
FROM leaderboard
ORDER BY score DESC
LIMIT 10;

-- Top 10 by difficulty
SELECT player_name, score, created_at
FROM leaderboard
WHERE difficulty = 'hard'
ORDER BY score DESC
LIMIT 10;

-- Player statistics
SELECT
  player_name,
  COUNT(*) as games_played,
  MAX(score) as best_score,
  AVG(score) as avg_score
FROM leaderboard
GROUP BY player_name
ORDER BY best_score DESC;
```

## Troubleshooting

### "Supabase credentials not found"

- Check `.env` file exists in `proto/` directory
- Verify `SUPABASE_URL` and `SUPABASE_KEY` are set correctly
- Make sure there are no extra spaces or quotes

### "Error submitting score"

- Verify table exists in Supabase
- Check RLS policies are enabled
- Ensure your Supabase project is active (not paused)
- Check network connection

### "relation 'leaderboard' does not exist"

- Run `supabase_schema.sql` in SQL Editor
- Refresh the page after running SQL
- Check for SQL errors in the editor

### Performance Issues (many players)

- The schema includes optimized indexes
- Consider using the materialized view for stats
- Periodically run `SELECT refresh_leaderboard_stats();`

## Free Tier Limits

Supabase free tier includes:

- ✅ 500 MB database storage
- ✅ 5 GB bandwidth per month
- ✅ 50 MB file storage
- ✅ 2 GB RAM per database
- ⚠️ Projects pause after 1 week of inactivity (auto-resume on access)

**This is more than enough for the game!** Even with 10,000 score entries, you'll use less than 1 MB.

## Security Best Practices

1. **Never commit `.env` to git** (already in `.gitignore`)
2. **Use anon/public key** (not service_role key) in the app
3. **Keep database password secure**
4. **Enable RLS** (already done in schema)
5. Consider adding rate limiting if needed

## Advanced Features

### Add Player Authentication (Optional)

If you want users to have accounts:

1. Enable **Authentication** in Supabase
2. Add `user_id` column to leaderboard
3. Update RLS policies to link scores to users

### Add Real-time Updates (Optional)

Enable real-time subscriptions to see scores update live:

```python
# In leaderboard.py
def subscribe_to_updates(self, callback):
    self.client.table(self.table_name).on('INSERT', callback).subscribe()
```

### Export Data

Download all scores:

1. Go to **Table Editor** → `leaderboard`
2. Click **Export** → Download as CSV

## Need Help?

- **Supabase Docs**: https://supabase.com/docs
- **SQL Tutorial**: https://supabase.com/docs/guides/database
- **Python Client**: https://supabase.com/docs/reference/python/introduction
