-- Supabase Schema for Fruit Ninja CV Leaderboard
-- Run this SQL in your Supabase SQL Editor

-- Create the leaderboard table
CREATE TABLE IF NOT EXISTS leaderboard (
  id BIGSERIAL PRIMARY KEY,
  player_name TEXT NOT NULL,
  score INTEGER NOT NULL CHECK (score >= 0),
  difficulty TEXT NOT NULL CHECK (difficulty IN ('easy', 'medium', 'hard')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_leaderboard_score 
ON leaderboard(score DESC);

CREATE INDEX IF NOT EXISTS idx_leaderboard_difficulty 
ON leaderboard(difficulty);

CREATE INDEX IF NOT EXISTS idx_leaderboard_player 
ON leaderboard(player_name);

CREATE INDEX IF NOT EXISTS idx_leaderboard_created 
ON leaderboard(created_at DESC);

-- Create a compound index for difficulty + score queries
CREATE INDEX IF NOT EXISTS idx_leaderboard_difficulty_score 
ON leaderboard(difficulty, score DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE leaderboard ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (read and insert)
-- Allow anyone to read leaderboard
CREATE POLICY "Enable read access for all users" 
ON leaderboard FOR SELECT 
USING (true);

-- Allow anyone to insert scores
CREATE POLICY "Enable insert access for all users" 
ON leaderboard FOR INSERT 
WITH CHECK (true);

-- Optional: Create a view for top scores by difficulty
CREATE OR REPLACE VIEW top_scores_by_difficulty AS
SELECT 
  difficulty,
  player_name,
  score,
  created_at,
  ROW_NUMBER() OVER (PARTITION BY difficulty ORDER BY score DESC) as rank
FROM leaderboard
ORDER BY difficulty, score DESC;

-- Optional: Create a materialized view for better performance on large datasets
CREATE MATERIALIZED VIEW IF NOT EXISTS leaderboard_stats AS
SELECT 
  difficulty,
  COUNT(*) as total_games,
  MAX(score) as highest_score,
  AVG(score) as average_score,
  MIN(score) as lowest_score
FROM leaderboard
GROUP BY difficulty;

-- Create an index on the materialized view
CREATE UNIQUE INDEX ON leaderboard_stats (difficulty);

-- Function to refresh stats (call periodically if using materialized view)
CREATE OR REPLACE FUNCTION refresh_leaderboard_stats()
RETURNS void AS $$
BEGIN
  REFRESH MATERIALIZED VIEW CONCURRENTLY leaderboard_stats;
END;
$$ LANGUAGE plpgsql;

-- Optional: Add a comment to the table
COMMENT ON TABLE leaderboard IS 'Stores player scores for Fruit Ninja CV game';
