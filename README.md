# MiniNinja 🥷

## Overview

MiniNinja is an interactive, camera-based fruit-slicing game where players use hand gestures to slice flying fruits—no touch, no controllers, just vision. Built with real-time hand tracking and swipe detection, it turns your webcam into a dojo for mini ninjas.

## Problem Statement

Traditional gesture-based games often require wearables, touchscreens, or complex setups. MiniNinja solves this by using **only a standard webcam** and **on-device computer vision** to enable intuitive, contactless interaction. This is interesting for CV because it combines:

- Real-time hand landmark estimation (21-point 3D pose)
- Temporal gesture recognition (swipe direction/speed)
- Low-latency rendering for responsive gameplay  
  All while running locally—no cloud, no internet.

## Dataset

MiniNinja does not use a static dataset. Instead, it processes **live video streams** from a webcam:

- **Input**: Real-time RGB video (640×480+ @ 30 FPS)
- **Annotations**: Hand landmarks generated on-the-fly by MediaPipe Hands (21-point 3D hand model)
- **Gesture labels**: Dynamically inferred from fingertip motion and velocity
  - Detects **omnidirectional slashing** (any fast motion)
  - Uses temporal window (0.3s) for trail-based collision detection
  - Configurable sensitivity thresholds for different difficulty levels

> 💡 _No pre-collected dataset is needed—interaction is continuous and user-driven._

## Method / Approach

### Architecture

- **Input**: Webcam feed → RGB frame (flipped for mirror effect)
- **Hand Detection**: MediaPipe Hands (BlazePalm + Hand Landmark CNN)
  - 21-point hand landmark detection
  - Configurable detection/tracking confidence thresholds
- **Gesture Engine**:
  - Temporal velocity analysis of index fingertip (landmark #8)
  - History-based motion tracking (10 frames)
  - Omnidirectional slash detection (any fast motion counts)
- **Trail System**:
  - Visual feedback with fading effect (0.5s lifetime)
  - Trail-based collision detection (checks last 0.3s of motion)
- **Game Logic**:
  - Fruit spawning with configurable intervals
  - Physics-based upward movement
  - Collision detection with automatic state management
  - Real-time scoring
- **Output**: Annotated frame with fruits, trail, score, and optional debug info

### Key Libraries

| Layer        | Technology                             |
| ------------ | -------------------------------------- |
| Prototype    | Python, OpenCV, MediaPipe              |
| Production   | C++, OpenCV, MediaPipe (C++ API), Qt 6 |
| Build System | CMake (production), UV (prototype)     |
| Rendering    | Qt Widgets / QImage                    |

### Prototype Architecture Highlights

The Python prototype demonstrates clean software design:

- **Modular structure**: Separate modules for config, entities, tracking, and game logic
- **Entity encapsulation**: Game objects manage their own state and behavior
- **Configuration management**: Centralized settings with multiple difficulty presets
- **CLI interface**: Professional command-line interface with argparse
- **Extensibility**: Easy to add new features (documented with code examples)

## Results

### Performance (on mid-range laptop: i5, 8GB RAM)

- **End-to-end latency**: ~60–80 ms (camera → slice response)
- **Hand tracking**: 25–30 FPS (stable under good lighting)
- **Gesture detection**: Near-instant response with omnidirectional slashing
- **Trail rendering**: Smooth 30 FPS with up to 50 trail points
- **Game mechanics**: Reliable collision detection with trail-based system

### Difficulty Levels

The prototype includes three difficulty presets:

- **Easy**: 2.0s spawn interval, slower fruits (3 px/frame), relaxed gesture detection
- **Medium**: 1.5s spawn interval, moderate speed (5 px/frame), balanced sensitivity
- **Hard**: 1.0s spawn interval, fast fruits (7 px/frame), precise gesture required

### Example Output

![MiniNinja gameplay](assets/demo.gif)  
_Player slicing fruits with hand swipes. Juice splashes on hit!_

> 📌 _Demo video/GIF recommended in `assets/`_

## Project Structure

```
minininja/
├── proto/              # Python prototype with complete game implementation
│   ├── main.py        # CLI entry point with multiple options
│   ├── config.py      # Centralized configuration and difficulty levels
│   ├── entities.py    # Game entities (Fruit, Trail)
│   ├── fruit_ninja_game.py  # Main game controller
│   ├── hand_tracker.py      # MediaPipe hand tracking wrapper
│   ├── gesture_detector.py  # Gesture detection algorithm
│   └── README.md      # Detailed proto documentation
├── src/               # C++ production implementation (planned)
├── tests/             # Unit and integration tests
├── assets/            # Images, sounds, and media files
└── docs/              # Additional documentation
```

## Usage

### Run Python Prototype

```bash
# 1. Clone repo
git clone https://github.com/bigalex95/minininja.git
cd minininja/proto

# 2. Install dependencies (using uv - recommended)
uv sync

# Or with pip
pip install -e .

# 3. Run with default settings
uv run python main.py

# Or with custom options
uv run python main.py --difficulty hard --debug
uv run python main.py --width 1280 --height 720

# See all options
uv run python main.py --help
```

### Prototype Features

- **CLI with multiple options**: difficulty levels, resolution, debug mode
- **Omnidirectional slashing**: Slash in any direction (not just 4 cardinal directions)
- **Visual trail effect**: Fading trail that follows your finger movements
- **Configurable settings**: Easily adjust game parameters in `config.py`
- **Clean architecture**: Modular design with separate concerns

📖 **Full documentation**: See `proto/README.md` for detailed usage, configuration, and development guide.
