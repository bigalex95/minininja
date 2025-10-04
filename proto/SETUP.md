# Fruit Ninja CV - Setup and Configuration Guide

## Project Structure

```
proto/
├── src/                      # Source code (organized by module)
│   ├── __init__.py
│   ├── core/                 # Core game logic
│   │   ├── __init__.py
│   │   ├── config.py         # Game configuration
│   │   ├── entities.py       # Game entities (Fruit, Trail)
│   │   └── game.py           # Main game controller
│   ├── cv/                   # Computer vision components
│   │   ├── __init__.py
│   │   ├── hand_tracker.py   # MediaPipe hand tracking
│   │   └── gesture_detector.py  # Gesture detection
│   ├── leaderboard/          # Leaderboard functionality
│   │   ├── __init__.py
│   │   └── leaderboard.py    # Supabase integration
│   └── ui/                   # User interface components
│       ├── __init__.py
│       └── leaderboard_ui.py # Leaderboard rendering
├── main.py                   # Application entry point
├── pyproject.toml           # Project dependencies
├── .env.example             # Environment variables template
├── .env                     # Your secrets (not in git)
├── docs/                    # Documentation
├── scripts/                 # Setup and utility scripts
├── tests/                   # Test scripts
└── old_files_backup/        # Backup of old flat structure (can be removed)
```

## Setup Instructions

### 1. Install Dependencies

**Option A: Using uv (recommended)**

```bash
uv sync
```

**Option B: Using pip**

```bash
pip install -e .
```

### 2. Set Up Supabase

1. **Create a Supabase account** at https://supabase.com
2. **Create a new project**
3. **Create the leaderboard table** using the SQL editor:

```sql
CREATE TABLE leaderboard (
  id BIGSERIAL PRIMARY KEY,
  player_name TEXT NOT NULL,
  score INTEGER NOT NULL,
  difficulty TEXT NOT NULL CHECK (difficulty IN ('easy', 'medium', 'hard')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create an index for faster queries
CREATE INDEX idx_leaderboard_score ON leaderboard(score DESC);
CREATE INDEX idx_leaderboard_difficulty ON leaderboard(difficulty);
```

4. **Get your API credentials**:
   - Go to Project Settings → API
   - Copy the `Project URL` (SUPABASE_URL)
   - Copy the `anon/public` key (SUPABASE_KEY)

### 3. Configure Environment Variables

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit `.env` and add your Supabase credentials:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
```

### 4. Run the Game

Basic usage:

```bash
python main.py
```

With options:

```bash
# Set player name and show leaderboard
python main.py --player-name "YourName" --show-leaderboard

# Choose difficulty
python main.py --difficulty hard --player-name "Pro Player"

# Custom resolution
python main.py --width 1280 --height 720

# Debug mode
python main.py --debug
```

## Command Line Options

```
--difficulty {easy,medium,hard}
    Game difficulty level (default: medium)

--width WIDTH
    Window width in pixels (default: 640)

--height HEIGHT
    Window height in pixels (default: 480)

--debug
    Enable debug mode (show hand landmarks)

--no-trail
    Disable slash trail visualization

--player-name PLAYER_NAME
    Player name for leaderboard (default: Player)

--show-leaderboard
    Show leaderboard at game end
```

## Leaderboard Features

- **Online Leaderboard**: Scores are stored in Supabase cloud database
- **Multiple Players**: Track scores for different players
- **Difficulty Levels**: Separate leaderboards for each difficulty
- **Real-time Updates**: Scores are immediately available to all players
- **Top 10 Display**: View top 10 scores after each game

## Troubleshooting

### Leaderboard not working

1. Check your `.env` file has correct credentials
2. Verify the `leaderboard` table exists in Supabase
3. Check Supabase project is active (not paused)
4. Run with `--debug` flag to see detailed error messages

### Import errors

Make sure you're running from the `proto` directory:

```bash
cd /path/to/minininja/proto
python main.py
```

### Camera not detected

- Check camera permissions
- Try different camera indices in config
- Ensure no other app is using the camera

## Development

### Running Tests

```bash
python test_setup.py
```

### Adding Features

The modular structure makes it easy to extend:

- **New game modes**: Add to `src/core/`
- **New gestures**: Extend `src/cv/gesture_detector.py`
- **New UI elements**: Add to `src/ui/`
- **New data sources**: Add to `src/leaderboard/`

## Migration Notes

The old flat structure has been reorganized into a proper package structure:

- ✅ Old files have been moved to `old_files_backup/`
- ✅ New structure follows Python best practices
- ✅ All imports updated to use new paths
- ✅ Migration is complete - use the new structure

The `old_files_backup/` directory contains:

- `config.py` → now `src/core/config.py`
- `entities.py` → now `src/core/entities.py`
- `fruit_ninja_game.py` → now `src/core/game.py`
- `hand_tracker.py` → now `src/cv/hand_tracker.py`
- `gesture_detector.py` → now `src/cv/gesture_detector.py`
