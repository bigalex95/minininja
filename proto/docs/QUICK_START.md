# Quick Start Guide

## 🚀 Running the Game

### Basic Usage

```bash
# Default settings
python main.py

# Or with uv
uv run python main.py
```

### With Options

```bash
# Easy difficulty
uv run python main.py --difficulty easy

# Hard difficulty with debug mode
uv run python main.py --difficulty hard --debug

# Custom resolution
uv run python main.py --width 1280 --height 720

# All options combined
uv run python main.py --difficulty hard --width 1280 --height 720 --debug
```

## 📁 File Guide

| File                         | Purpose           | When to Edit                    |
| ---------------------------- | ----------------- | ------------------------------- |
| `main.py`                    | Entry point & CLI | Add new command-line options    |
| `src/core/config.py`         | All settings      | Change game behavior/parameters |
| `src/core/entities.py`       | Game objects      | Add new entity types            |
| `src/core/game.py`           | Game logic        | Modify game mechanics           |
| `src/cv/hand_tracker.py`     | Hand detection    | Tweak CV parameters             |
| `src/cv/gesture_detector.py` | Motion detection  | Change gesture detection        |
| `tests/test_setup.py`        | Validation        | Test your changes               |

## 🎮 Quick Configuration Changes

### Make Game Easier

Edit `src/core/config.py`:

```python
FRUIT_SPAWN_INTERVAL = 2.5  # Slower spawning
FRUIT_VELOCITY = 3          # Slower fruits
MIN_SLASH_VELOCITY = 0.05   # Less sensitive
```

### Make Trail More Visible

Edit `src/core/config.py`:

```python
TRAIL_LIFETIME = 1.0        # Trail lasts longer
TRAIL_MAX_THICKNESS = 12    # Thicker trail
TRAIL_COLOR = (0, 255, 255) # Yellow trail
```

### Enable Debug Mode Permanently

Edit `src/core/config.py`:

```python
DEBUG_MODE = True
SHOW_HAND_LANDMARKS = True
SHOW_FINGERTIP_MARKER = True
```

## 🔧 Common Tasks

### Add a New CLI Option

1. Edit `main.py`, add to `parse_args()`:

```python
parser.add_argument('--my-option', ...)
```

2. Use in `create_config()`:

```python
if args.my_option:
    config.MY_SETTING = args.my_option
```

### Add a New Entity Type

1. Add class to `src/core/entities.py`:

```python
class Bomb:
    def __init__(self, x, y):
        ...
```

2. Use in `src/core/game.py`:

```python
from src.core.entities import Fruit, Trail, Bomb

self.bombs = []  # In __init__
# Add spawn, update, render logic
```

### Change Gesture Detection

Edit `src/cv/gesture_detector.py`:

```python
# Adjust sensitivity
def __init__(self, history_size=10, min_velocity=0.03):
    ...

# Or add new gesture types
class Gesture(Enum):
    NONE = 0
    SLASHING = 1
    CIRCLE = 2  # New!
```

## 🧪 Testing Your Changes

```bash
# Quick validation
uv run python test_setup.py

# Run game with debug mode
uv run python main.py --debug

# Check help text
uv run python main.py --help
```

## 📊 Understanding the Flow

```
main.py
  ↓ (parse args)
src/core/config.py
  ↓ (create GameConfig)
src/core/game.py
  ↓ (initialize game)
  ├─→ src/cv/hand_tracker.py (detect hand)
  ├─→ src/cv/gesture_detector.py (detect motion)
  ├─→ src/core/entities.py (manage fruits/trail)
  └─→ render & display
```

## 🎯 Difficulty Comparison

| Setting        | Easy   | Medium | Hard   |
| -------------- | ------ | ------ | ------ |
| Spawn Interval | 2.0s   | 1.5s   | 1.0s   |
| Fruit Speed    | 3 px/f | 5 px/f | 7 px/f |
| Min Velocity   | 0.05   | 0.03   | 0.02   |

## 🐛 Quick Troubleshooting

### "Camera not working"

```bash
# Test camera index
# Edit src/core/game.py line ~130
cap = cv2.VideoCapture(1)  # Try different numbers: 0, 1, 2
```

### "Hand not detected"

```bash
# Run with debug mode
python main.py --debug

# If still not working, lower confidence
# Edit src/core/config.py:
DETECTION_CONFIDENCE = 0.5
TRACKING_CONFIDENCE = 0.5
```

### "Gestures too sensitive / not sensitive enough"

```bash
# Too sensitive (false positives)
python main.py --difficulty hard  # Higher threshold

# Not sensitive enough
python main.py --difficulty easy  # Lower threshold

# Or edit src/core/config.py:
MIN_SLASH_VELOCITY = 0.05  # Higher = less sensitive
MIN_SLASH_VELOCITY = 0.01  # Lower = more sensitive
```

## 📚 Documentation Index

- **README.md** - Full documentation, installation, usage
- **ARCHITECTURE.md** - Technical design, data flow, components
- **REFACTORING.md** - Before/after comparison, changes made
- **QUICK_START.md** - This file, quick reference

## 🎨 Customization Ideas

### Change Fruit Color

Edit `src/core/config.py`:

```python
FRUIT_COLOR = (0, 0, 255)  # Red
FRUIT_COLOR = (255, 0, 0)  # Blue
FRUIT_COLOR = (0, 255, 0)  # Green
```

### Make Fruits Bigger

Edit `src/core/config.py`:

```python
FRUIT_RADIUS = 30  # Default is 20
```

### Change Window Title

Edit `src/core/config.py`:

```python
WINDOW_TITLE = "My Awesome Fruit Game!"
```

### Multiple Fruit Colors

Edit `src/core/game.py`, `spawn_fruit()`:

```python
import random
colors = [(0, 255, 255), (0, 255, 0), (0, 0, 255)]
fruit = Fruit(
    x, y,
    radius=self.config.FRUIT_RADIUS,
    color=random.choice(colors)
)
```

## ⌨️ Keyboard Shortcuts

| Key | Action    |
| --- | --------- |
| `q` | Quit game |

## 🔄 Project Commands

```bash
# Validation
uv run python test_setup.py

# Run game
uv run python main.py

# View help
uv run python main.py --help

# Sync dependencies
uv sync

# Update dependencies
uv lock --upgrade
```

---

**Pro Tip**: Always run `test_setup.py` after making changes to ensure nothing broke!
