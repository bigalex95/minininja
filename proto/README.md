# Fruit Ninja CV - Prototype

A computer vision-based Fruit Ninja game using hand gesture recognition via MediaPipe.

## 🎮 Features

- **Hand Gesture Recognition**: Slice fruits with your hand movements detected by your webcam
- **Visual Slash Trail**: See a fading trail that follows your finger movements
- **Omnidirectional Slashing**: Slash in any direction - horizontal, vertical, diagonal, or circular
- **Multiple Difficulty Levels**: Easy, Medium, and Hard modes
- **Configurable Settings**: Customize resolution, trail effects, and debug options

## 📋 Requirements

- Python 3.11+
- Webcam
- Dependencies listed in `pyproject.toml`

## 🚀 Quick Start

### Installation

```bash
# Install dependencies with uv
uv sync

# Or with pip
pip install -e .
```

### Running the Game

```bash
# Using uv
uv run main.py

# Or if installed
python main.py

# Or directly
python -m main
```

## 🎯 Usage

### Basic Commands

```bash
# Start with default settings (medium difficulty)
uv run main.py

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
- They move upward and disappear if not sliced

### Slashing Detection

- The game tracks your index fingertip position
- Creates a visual trail that fades over 0.5 seconds
- Detects when your trail intersects with fruits
- Any fast motion in any direction counts as a slash

### Scoring

- Each sliced fruit adds 1 point to your score
- Final score is displayed when you quit

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

### Adding New Features

1. **Game Entities**: Add to `entities.py`
2. **Configuration**: Add settings to `config.py`
3. **Game Logic**: Modify `fruit_ninja_game.py`
4. **CLI Options**: Update argument parser in `main.py`

### Running in Debug Mode

```bash
uv run main.py --debug
```

This will show:

- Hand landmarks (green dots)
- Fingertip marker (yellow dot)
- Current gesture status

## 📝 License

See LICENSE file in the root directory.

## 🤝 Contributing

This is a prototype. Feel free to experiment and improve!
