# Fruit Ninja CV - Python Prototype

A computer vision-based Fruit Ninja game using hand gesture recognition via MediaPipe with **online leaderboard** support!

## 🎮 Features

- **Hand Gesture Recognition**: Slice fruits with your hand movements detected by your webcam
- **Visual Slash Trail**: See a fading trail that follows your finger movements
- **Omnidirectional Slashing**: Slash in any direction - horizontal, vertical, diagonal, or circular
- **Multiple Difficulty Levels**: Easy, Medium, and Hard modes
- **🏆 Online Leaderboard**: Submit scores and compete with players worldwide via Supabase
- **Player Profiles**: Track your scores and rank
- **Configurable Settings**: Customize resolution, trail effects, and debug options

## 📋 Requirements

- Python 3.11+
- Webcam
- Supabase account (free) for leaderboard functionality

## 🚀 Quick Start

### 1. Installation

Run the automated setup script:

```bash
./setup.sh
```

Or manually:

```bash
# Install dependencies with uv (recommended)
uv sync

# Or with pip
pip install -e .
```

### 2. Configure Leaderboard (Optional but Recommended)

1. **Create a Supabase account** at https://supabase.com (free)
2. **Follow the setup guide** in `docs/SUPABASE_SETUP.md`
3. **Copy your credentials** to `.env`:
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase URL and API key
   ```

See [docs/SUPABASE_SETUP.md](docs/SUPABASE_SETUP.md) for detailed instructions.

### 3. Run the Game

```bash
# Basic usage
python main.py

# With player name and leaderboard
python main.py --player-name "YourName" --show-leaderboard

# Choose difficulty
python main.py --difficulty hard

# Custom resolution
python main.py --width 1280 --height 720
```

## 🎯 Usage Examples

### Basic Commands

```bash
# Start with default settings (medium difficulty)
python main.py

# Choose difficulty level
uv run main.py --difficulty easy
uv run main.py --difficulty hard

# Custom resolution
uv run main.py --width 1280 --height 720

# Enable debug mode (show hand landmarks)
uv run main.py --debug

# Disable trail effect
uv run main.py --no-trail

# Combine options
uv run main.py --difficulty hard --width 1280 --height 720 --debug
```

### In-Game Controls

- **Move your hand**: The game tracks your index finger
- **Make slashing motions**: Any fast movement will slice fruits
- **Press 'q'**: Quit the game

## 🏗️ Project Structure

```
proto/
├── main.py                 # Entry point with CLI
├── config.py              # Game configuration and difficulty settings
├── entities.py            # Game entities (Fruit, Trail, etc.)
├── fruit_ninja_game.py    # Main game logic
├── hand_tracker.py        # MediaPipe hand tracking wrapper
├── gesture_detector.py    # Gesture detection algorithm
├── pyproject.toml         # Project dependencies
└── README.md              # This file
```

## 🎨 Game Mechanics

### Fruit Spawning

- Fruits spawn at the bottom of the screen at regular intervals
- They move upward continuously
- Disappear automatically when they move off-screen (top)
- Sliced fruits are removed from the game immediately

### Slashing Detection

- The game tracks your index fingertip position in real-time
- Creates a visual trail that fades over 0.5 seconds
- Trail points within the last 0.3 seconds are checked for collisions
- When your trail intersects with a fruit (within collision threshold), the fruit is instantly sliced
- Any fast motion in any direction counts as a slashing gesture
- Only active (alive) fruits can be sliced

### Collision System

- **Trail-based collision**: Uses recent trail points instead of just current finger position
- **Collision threshold**: Configurable distance (default: 20 pixels from fruit center)
- **Automatic state management**: Fruits automatically mark themselves as sliced on collision
- **Efficient cleanup**: Sliced and off-screen fruits are removed in the same update cycle

### Scoring

- Each successfully sliced fruit adds 1 point to your score
- Score is displayed in real-time at the top-left corner
- Final score is shown when you quit the game

## ⚙️ Configuration

Edit `config.py` to customize:

- **Display Settings**: Window size, FPS, title
- **Game Mechanics**: Spawn rate, fruit properties, velocity
- **Hand Tracking**: Detection/tracking confidence thresholds
- **Gesture Detection**: Sensitivity, history size
- **Trail Effects**: Color, thickness, lifetime, fade duration
- **Debug Options**: Toggle landmarks, markers, etc.

### Difficulty Levels

**Easy**

- Spawn interval: 2.0 seconds
- Fruit velocity: 3 pixels/frame
- Min slash velocity: 0.05

**Medium** (Default)

- Spawn interval: 1.5 seconds
- Fruit velocity: 5 pixels/frame
- Min slash velocity: 0.03

**Hard**

- Spawn interval: 1.0 seconds
- Fruit velocity: 7 pixels/frame
- Min slash velocity: 0.02

## 🐛 Troubleshooting

### Camera not working

- Ensure your webcam is connected and not in use by another application
- Try changing the camera index in `fruit_ninja_game.py` (line with `cv2.VideoCapture(0)`)

### Hand not detected

- Ensure good lighting conditions
- Keep your hand in view of the camera
- Adjust `DETECTION_CONFIDENCE` and `TRACKING_CONFIDENCE` in `config.py`

### Gestures not recognized

- Move your hand faster
- Lower `MIN_SLASH_VELOCITY` in `config.py` or choose easy difficulty
- Enable debug mode to see detection: `--debug`

## 🔧 Development

### Code Architecture Highlights

The prototype uses clean object-oriented design:

- **Entities encapsulate their own logic**: `Fruit.check_collision()` handles both collision detection and state updates
- **Trail management is automatic**: Points are added, aged, and removed automatically
- **Single responsibility**: Each class has a clear, focused purpose
- **Easy to extend**: Add new entity types by following the `Fruit` class pattern

### Adding New Features

1. **Game Entities**: Add to `entities.py` (follow `Fruit` or `Trail` as examples)
2. **Configuration**: Add settings to `config.py` with sensible defaults
3. **Game Logic**: Modify `fruit_ninja_game.py` game loop methods
4. **CLI Options**: Update argument parser in `main.py`

Example: Adding a new entity type

```python
# In entities.py
class Bomb(Fruit):
    def __init__(self, x, y):
        super().__init__(x, y, radius=25, color=(0, 0, 255))  # Red bomb
        self.is_bomb = True

    def check_collision(self, x, y, threshold=20):
        if super().check_collision(x, y, threshold):
            return True  # Game over or penalty logic in main game
        return False
```

### Running in Debug Mode

```bash
uv run main.py --debug
```

This will show:

- Hand landmarks (green dots)
- Fingertip marker (yellow/cyan dot)
- Current gesture status ("SLASHING!" when detected)
- Real-time trail visualization

## 📝 License

See LICENSE file in the root directory.

## 🤝 Contributing

This is a prototype. Feel free to experiment and improve!
