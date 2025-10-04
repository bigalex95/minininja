# Quick Reference Guide

## 🚀 Installation (First Time)

```bash
# Run automated setup
./setup.sh

# Or manually
uv sync  # or: pip install -e .
```

## 🔐 Leaderboard Setup (One Time)

### Quick Method (Interactive)

```bash
python setup_supabase.py
```

### Manual Method

1. Go to https://supabase.com and create account
2. Create new project
3. Run SQL from `supabase_schema.sql` in SQL Editor
4. Copy `.env.example` to `.env`
5. Add your credentials to `.env`

## 🎮 Running the Game

### Basic

```bash
python main.py
```

### With Leaderboard

```bash
python main.py --player-name "YourName" --show-leaderboard
```

### All Options

```bash
python main.py \
  --player-name "Pro" \
  --difficulty hard \
  --show-leaderboard \
  --width 1280 \
  --height 720 \
  --debug
```

## 📋 Command Options

| Option               | Values           | Default  | Description               |
| -------------------- | ---------------- | -------- | ------------------------- |
| `--player-name`      | string           | "Player" | Your name for leaderboard |
| `--difficulty`       | easy/medium/hard | medium   | Game difficulty           |
| `--show-leaderboard` | flag             | off      | Show top 10 after game    |
| `--width`            | number           | 640      | Window width              |
| `--height`           | number           | 480      | Window height             |
| `--debug`            | flag             | off      | Show hand landmarks       |
| `--no-trail`         | flag             | off      | Disable slash trail       |

## 🎯 Game Controls

| Action       | Control                         |
| ------------ | ------------------------------- |
| Slash fruits | Move hand quickly across screen |
| Pause        | Press 'P'                       |
| Quit         | Press 'Q' or ESC                |

## 📁 Project Structure

```
proto/
├── src/              # Source code
│   ├── core/         # Game logic
│   ├── cv/           # Computer vision
│   ├── leaderboard/  # Online features
│   └── ui/           # User interface
├── docs/             # Documentation
├── data/             # Game data
└── main.py           # Entry point
```

## 🧪 Testing

```bash
# Test structure
python test_structure.py

# Test game (no leaderboard needed)
python main.py --difficulty easy

# Test with leaderboard
python main.py --player-name "Test" --show-leaderboard
```

## 📚 Documentation

| File                     | Purpose                      |
| ------------------------ | ---------------------------- |
| `README.md`              | Main readme                  |
| `SETUP.md`               | Detailed setup guide         |
| `PROJECT_SUMMARY.md`     | What was changed             |
| `MIGRATION.md`           | Migration from old structure |
| `docs/SUPABASE_SETUP.md` | Leaderboard setup            |

## 🛠️ Common Tasks

### View Leaderboard Data

Go to Supabase dashboard → Table Editor → leaderboard

### Update Dependencies

```bash
uv sync  # or: pip install -e .
```

### Clean Old Files

```bash
mkdir old_files_backup
mv config.py entities.py fruit_ninja_game.py hand_tracker.py gesture_detector.py old_files_backup/
```

### Reset Leaderboard

In Supabase SQL Editor:

```sql
DELETE FROM leaderboard;
```

## 🐛 Troubleshooting

### "Supabase credentials not found"

- Copy `.env.example` to `.env`
- Add your Supabase URL and key to `.env`

### "Module not found"

- Run from `proto/` directory
- Reinstall: `uv sync`

### "Camera not detected"

- Check camera permissions
- Close other apps using camera
- Try different camera in config

### Import errors

```bash
cd /path/to/minininja/proto
python main.py
```

## 🔗 Useful Links

- **Supabase Dashboard**: https://app.supabase.com
- **GitHub Repo**: https://github.com/bigalex95/minininja
- **MediaPipe Docs**: https://google.github.io/mediapipe/

## 💡 Tips

- **Better Performance**: Use `--width 640 --height 480`
- **Debug Issues**: Add `--debug` flag
- **Practice Mode**: Use `--difficulty easy --no-trail`
- **Competition**: Use `--show-leaderboard` to see rankings

## 🎓 Learning Resources

- `ARCHITECTURE.md` - Code architecture
- `REFACTORING.md` - Refactoring notes
- Source code comments in `src/`

---

**Need help?** Run: `python main.py --help`
