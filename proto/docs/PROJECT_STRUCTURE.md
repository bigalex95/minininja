# Project Structure

Clean, organized structure for the Fruit Ninja CV prototype.

## Directory Tree

```
proto/
├── .env                      # Environment variables (not in git)
├── .env.example              # Environment template
├── .gitignore               # Git ignore rules
├── .python-version          # Python version
├── README.md                # Main readme (you are here)
├── SETUP.md                 # Setup instructions
├── main.py                  # Application entry point
├── pyproject.toml           # Project configuration & dependencies
├── uv.lock                  # Dependency lock file
│
├── src/                     # Source code
│   ├── __init__.py
│   ├── core/                # Core game logic
│   │   ├── __init__.py
│   │   ├── config.py        # Game configuration
│   │   ├── entities.py      # Game entities (Fruit, Trail)
│   │   └── game.py          # Main game controller
│   ├── cv/                  # Computer vision
│   │   ├── __init__.py
│   │   ├── hand_tracker.py  # MediaPipe hand tracking
│   │   └── gesture_detector.py  # Gesture detection
│   ├── leaderboard/         # Online leaderboard
│   │   ├── __init__.py
│   │   └── leaderboard.py   # Supabase integration
│   └── ui/                  # User interface
│       ├── __init__.py
│       └── leaderboard_ui.py  # UI rendering
│
├── docs/                    # Documentation
│   ├── README.md           # Documentation index
│   ├── ARCHITECTURE.md     # Original architecture
│   ├── ARCHITECTURE_UPDATED.md  # Updated architecture
│   ├── MIGRATION.md        # Migration guide
│   ├── PROJECT_SUMMARY.md  # Project summary
│   ├── QUICK_REFERENCE.md  # Quick command reference
│   ├── QUICK_START.md      # Quick start guide
│   ├── REFACTORING.md      # Refactoring notes
│   ├── SUPABASE_SETUP.md   # Leaderboard setup
│   └── supabase_schema.sql # Database schema
│
├── scripts/                 # Setup & utility scripts
│   ├── README.md           # Scripts documentation
│   ├── setup.sh            # Main setup script
│   └── setup_supabase.py   # Supabase setup helper
│
├── tests/                   # Test scripts
│   ├── README.md           # Test documentation
│   ├── test_structure.py   # Structure validation
│   └── test_setup.py       # Setup test (legacy)
│
├── data/                    # Game data directory
│   └── .gitkeep            # Keep directory in git
│
└── old_files_backup/        # Backup of old flat structure
    ├── config.py
    ├── entities.py
    ├── fruit_ninja_game.py
    ├── gesture_detector.py
    └── hand_tracker.py
```

## Module Organization

### Source Code (`src/`)

All application code is organized by functionality:

- **`core/`** - Game logic, entities, configuration
- **`cv/`** - Computer vision (hand tracking, gestures)
- **`leaderboard/`** - Online features (database integration)
- **`ui/`** - User interface components

### Documentation (`docs/`)

All documentation files in one place:

- Setup guides
- Architecture documentation
- API references
- Migration notes

### Scripts (`scripts/`)

Utility scripts for setup and maintenance:

- `setup.sh` - Main installation script
- `setup_supabase.py` - Interactive leaderboard setup

### Tests (`tests/`)

Test and validation scripts:

- `test_structure.py` - Validates project structure
- `test_setup.py` - Legacy setup test

## Key Files

### Root Level

- **`main.py`** - Application entry point
- **`pyproject.toml`** - Dependencies and project metadata
- **`README.md`** - Project overview
- **`SETUP.md`** - Setup instructions
- **`.env`** - Environment variables (create from `.env.example`)

### Configuration

- **`.env.example`** - Template for environment variables
- **`.gitignore`** - Files to exclude from git
- **`pyproject.toml`** - Project configuration

## Import Paths

With the organized structure, imports follow this pattern:

```python
# Core modules
from src.core import GameConfig, DifficultyLevel
from src.core import Fruit, Trail, FruitNinjaGame

# CV modules
from src.cv import HandTracker, GestureDetector, Gesture

# Leaderboard
from src.leaderboard import Leaderboard

# UI
from src.ui import LeaderboardUI
```

## Running from Different Locations

### From Project Root (Recommended)
```bash
python main.py
python tests/test_structure.py
python scripts/setup_supabase.py
```

### From Scripts Directory
```bash
cd scripts
./setup.sh                    # Works (uses relative paths)
python setup_supabase.py      # Works (auto-detects root)
```

### From Tests Directory
```bash
cd tests
python test_structure.py      # Works (auto-detects root)
```

## Design Principles

### 1. Separation of Concerns
Each module has a specific responsibility:
- `core` = game logic
- `cv` = computer vision
- `leaderboard` = online features
- `ui` = visual components

### 2. Clear Dependencies
```
main.py → core → cv
       ↓      ↓
       leaderboard
       ui
```

### 3. Documentation Organization
All docs in `docs/`, easy to find and navigate

### 4. Utility Separation
Scripts in `scripts/`, tests in `tests/`

### 5. Clean Root
Only essential files in project root

## Benefits of This Structure

✅ **Easy to Navigate** - Find files by functionality
✅ **Easy to Extend** - Add new modules without clutter
✅ **Professional** - Follows Python best practices
✅ **Scalable** - Structure supports growth
✅ **Testable** - Clear separation enables testing
✅ **Documented** - All docs in one place

## Comparison with Old Structure

### Before (Flat)
```
proto/
├── config.py
├── entities.py
├── fruit_ninja_game.py
├── hand_tracker.py
├── gesture_detector.py
├── main.py
├── README.md
├── SETUP.md
├── ARCHITECTURE.md
├── MIGRATION.md
├── ...15 more files...
└── pyproject.toml
```
❌ Hard to find files
❌ Root directory cluttered
❌ No clear organization

### After (Organized)
```
proto/
├── main.py
├── README.md
├── SETUP.md
├── pyproject.toml
├── src/          # Source code
├── docs/         # Documentation
├── scripts/      # Setup scripts
├── tests/        # Tests
└── data/         # Game data
```
✅ Clear organization
✅ Easy to navigate
✅ Professional structure

## Navigation Tips

### Find Documentation
```bash
ls docs/                    # List all docs
cat docs/README.md          # Documentation index
```

### Find Source Code
```bash
ls src/                     # List modules
ls src/core/                # Core game files
ls src/cv/                  # Computer vision files
```

### Run Scripts
```bash
./scripts/setup.sh                    # Main setup
python scripts/setup_supabase.py      # Supabase setup
python tests/test_structure.py        # Validate structure
```

### View Help
```bash
python main.py --help                 # Game options
cat docs/QUICK_REFERENCE.md           # Command reference
cat SETUP.md                          # Setup guide
```

## Adding New Features

### New Game Feature
Add to `src/core/` (e.g., `src/core/powerups.py`)

### New CV Feature
Add to `src/cv/` (e.g., `src/cv/face_detector.py`)

### New UI Component
Add to `src/ui/` (e.g., `src/ui/scoreboard.py`)

### New Documentation
Add to `docs/` (e.g., `docs/API.md`)

### New Test
Add to `tests/` (e.g., `tests/test_game.py`)

## Maintenance

### Clean Caches
```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

### Update Dependencies
```bash
uv sync                     # Update from pyproject.toml
```

### Validate Structure
```bash
python tests/test_structure.py
```

## Need Help?

- **Setup**: See `SETUP.md`
- **Quick Start**: See `docs/QUICK_START.md`
- **Commands**: See `docs/QUICK_REFERENCE.md`
- **Architecture**: See `docs/ARCHITECTURE_UPDATED.md`
- **Migration**: See `docs/MIGRATION.md`
