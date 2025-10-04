# Migration Guide - Proto Restructure

## What Changed?

The prototype has been reorganized from a flat file structure to a proper Python package structure with modular organization and added leaderboard functionality.

## File Migration Map

### Old Structure → New Structure

```
OLD                          NEW
─────────────────────────────────────────────────────────
config.py                 →  src/core/config.py
entities.py               →  src/core/entities.py
fruit_ninja_game.py       →  src/core/game.py
hand_tracker.py           →  src/cv/hand_tracker.py
gesture_detector.py       →  src/cv/gesture_detector.py
(new)                     →  src/leaderboard/leaderboard.py
(new)                     →  src/ui/leaderboard_ui.py
main.py                   →  main.py (updated imports)
```

### New Files Added

- `.env.example` - Environment variable template
- `.gitignore` - Git ignore rules
- `setup.sh` - Automated setup script
- `SETUP.md` - Setup documentation
- `supabase_schema.sql` - Database schema
- `docs/SUPABASE_SETUP.md` - Supabase guide
- `test_structure.py` - Structure validation
- `src/__init__.py` - Package init files
- `src/core/__init__.py`
- `src/cv/__init__.py`
- `src/leaderboard/__init__.py`
- `src/ui/__init__.py`

## Import Changes

### Before (Old)

```python
from config import GameConfig, DifficultyLevel
from entities import Fruit, Trail
from fruit_ninja_game import FruitNinjaGame
from hand_tracker import HandTracker
from gesture_detector import GestureDetector, Gesture
```

### After (New)

```python
from src.core import GameConfig, DifficultyLevel, Fruit, Trail, FruitNinjaGame
from src.cv import HandTracker, GestureDetector, Gesture
from src.leaderboard import Leaderboard
from src.ui import LeaderboardUI
```

## Backward Compatibility

The old files remain in place for backward compatibility. You can:

1. **Keep both**: Old files remain functional
2. **Migrate gradually**: Test with new structure, keep old as backup
3. **Clean up later**: Remove old files once confident

## Cleaning Up Old Files

Once you've tested and confirmed everything works:

```bash
# Create backup directory
mkdir old_files_backup

# Move old files to backup
mv config.py old_files_backup/
mv entities.py old_files_backup/
mv fruit_ninja_game.py old_files_backup/
mv hand_tracker.py old_files_backup/
mv gesture_detector.py old_files_backup/
mv test_setup.py old_files_backup/

# Or delete them if confident
# rm config.py entities.py fruit_ninja_game.py hand_tracker.py gesture_detector.py test_setup.py
```

## Testing the New Structure

Run the structure test:

```bash
python test_structure.py
```

Try running the game:

```bash
python main.py --player-name "Test" --difficulty easy
```

## New Features

### 1. Online Leaderboard

- Submit scores to cloud database
- View top 10 players
- Track personal best scores
- Filter by difficulty level

### 2. Environment Variables

- Secure credential management
- Easy configuration
- No hardcoded secrets

### 3. Better Organization

- Modular code structure
- Clear separation of concerns
- Easier to extend and maintain

## Troubleshooting

### Import Errors

If you get import errors, make sure you're running from the `proto/` directory:

```bash
cd /path/to/minininja/proto
python main.py
```

### Missing Dependencies

Reinstall dependencies:

```bash
uv sync
# or
pip install -e .
```

### Old Files Conflicting

If you have both old and new files, Python might import the wrong ones. Options:

1. Remove old files
2. Rename old files (add `.old` extension)
3. Move old files to subdirectory

### Leaderboard Not Working

1. Check `.env` file exists and has correct credentials
2. Verify Supabase table is created
3. Run with `--show-leaderboard` to see errors

## Benefits of New Structure

### Before

```
proto/
├── config.py
├── entities.py
├── fruit_ninja_game.py
├── hand_tracker.py
├── gesture_detector.py
└── main.py
```

❌ Flat structure
❌ No clear organization
❌ Hard to find related code
❌ No package structure

### After

```
proto/
├── src/
│   ├── core/         # Game logic
│   ├── cv/           # Computer vision
│   ├── leaderboard/  # Online features
│   └── ui/           # User interface
├── docs/             # Documentation
├── main.py           # Entry point
└── ...
```

✅ Organized by module
✅ Clear separation of concerns
✅ Easy to find code
✅ Proper package structure
✅ Room for growth

## Next Steps

1. **Test the new structure**: Run `python test_structure.py`
2. **Set up Supabase**: Follow `docs/SUPABASE_SETUP.md`
3. **Configure .env**: Copy `.env.example` and add credentials
4. **Try the leaderboard**: Run with `--show-leaderboard`
5. **Clean up old files**: Once confident, remove backups

## Questions?

- Check `SETUP.md` for setup instructions
- Check `docs/SUPABASE_SETUP.md` for leaderboard setup
- Review `ARCHITECTURE.md` for code organization
- Run `python main.py --help` for command options
