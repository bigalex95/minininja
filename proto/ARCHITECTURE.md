# Fruit Ninja CV - Architecture

## Module Dependency Graph

```
main.py (Entry Point)
    │
    ├─→ fruit_ninja_game.py (Game Controller)
    │       │
    │       ├─→ config.py (Configuration)
    │       │       └─→ GameConfig
    │       │       └─→ DifficultyLevel
    │       │
    │       ├─→ entities.py (Game Objects)
    │       │       ├─→ Fruit
    │       │       ├─→ Trail
    │       │       └─→ TrailPoint
    │       │
    │       ├─→ hand_tracker.py (CV Processing)
    │       │       └─→ HandTracker
    │       │               └─→ mediapipe
    │       │
    │       └─→ gesture_detector.py (Motion Detection)
    │               └─→ GestureDetector
    │                       └─→ Gesture (Enum)
    │
    └─→ config.py (CLI Configuration)
```

## Component Responsibilities

### Core Components

#### `main.py`

- **Purpose**: Application entry point
- **Responsibilities**:
  - Parse command-line arguments
  - Create game configuration
  - Initialize and run the game
  - Handle errors and user interrupts
- **External Dependencies**: argparse, sys

#### `config.py`

- **Purpose**: Centralized configuration
- **Responsibilities**:
  - Define all game settings
  - Provide difficulty presets
  - Expose configuration constants
- **External Dependencies**: None

#### `fruit_ninja_game.py`

- **Purpose**: Game controller and main loop
- **Responsibilities**:
  - Manage game state (score, fruits, trail)
  - Coordinate all game components
  - Handle video capture and rendering
  - Process game loop (spawn, update, check, render)
- **Internal Dependencies**: config, entities, hand_tracker, gesture_detector
- **External Dependencies**: cv2, random, time

### Supporting Components

#### `entities.py`

- **Purpose**: Game entity definitions
- **Responsibilities**:
  - Define Fruit class with physics and collision
  - Define Trail and TrailPoint for visual effects
  - Encapsulate entity behavior
- **External Dependencies**: time, collections

#### `hand_tracker.py`

- **Purpose**: Hand detection and tracking
- **Responsibilities**:
  - Initialize MediaPipe Hands
  - Process video frames
  - Extract hand landmarks
  - Provide drawing utilities
- **External Dependencies**: cv2, mediapipe

#### `gesture_detector.py`

- **Purpose**: Motion analysis
- **Responsibilities**:
  - Track fingertip movement history
  - Calculate velocity
  - Detect slashing gestures
  - Provide trail positions
- **External Dependencies**: collections

### Utility Components

#### `test_setup.py`

- **Purpose**: Validation and testing
- **Responsibilities**:
  - Verify all imports work
  - Test configuration setup
  - Validate game instantiation
  - Provide setup feedback
- **External Dependencies**: sys

#### `__init__.py`

- **Purpose**: Package initialization
- **Responsibilities**:
  - Define package exports
  - Provide version info
  - Enable `from proto import *`
- **External Dependencies**: None

## Data Flow

```
User Hand Movement
    ↓
Webcam (cv2.VideoCapture)
    ↓
HandTracker.process_frame()
    ↓
landmarks [(x, y), ...]
    ↓
    ├─→ GestureDetector.update(landmarks)
    │       ↓
    │   Gesture.SLASHING or Gesture.NONE
    │
    └─→ Trail.add_point(fingertip)
            ↓
        Trail points with timestamps
            ↓
        FruitNinjaGame.check_slice()
            ↓
        Collision detection
            ↓
        Score update
            ↓
        Render frame with trail
            ↓
        Display (cv2.imshow)
```

## State Management

### Game State

```python
FruitNinjaGame
├── fruits: List[Fruit]           # Active fruits
├── score: int                     # Current score
├── last_spawn: float             # Last spawn timestamp
├── running: bool                  # Game running flag
├── trail: Trail                   # Slash trail
├── hand_tracker: HandTracker     # CV component
└── gesture_detector: GestureDetector  # Motion detector
```

### Fruit State

```python
Fruit
├── x: int            # X position
├── y: int            # Y position
├── radius: int       # Collision radius
├── color: tuple      # BGR color
└── alive: bool       # Active flag
```

### Trail State

```python
Trail
└── points: deque[TrailPoint]  # Trail points (max 50)

TrailPoint
├── x: int            # X position
├── y: int            # Y position
├── timestamp: float  # Creation time
└── lifetime: float   # How long it lasts
```

## Configuration Hierarchy

```
CLI Arguments
    ↓
create_config()
    ↓
GameConfig (with overrides)
    ↓
    ├─→ WINDOW_WIDTH, WINDOW_HEIGHT
    ├─→ FRUIT_SPAWN_INTERVAL
    ├─→ FRUIT_VELOCITY
    ├─→ MIN_SLASH_VELOCITY
    ├─→ TRAIL_LIFETIME
    └─→ DEBUG_MODE, SHOW_*
        ↓
FruitNinjaGame.__init__(config)
    ↓
Game components initialized with config
```

## Extensibility Points

### Adding New Features

1. **New Entity Type**:

   - Add class to `entities.py`
   - Update game loop in `fruit_ninja_game.py`

2. **New Configuration**:

   - Add to `GameConfig` in `config.py`
   - Use in relevant component

3. **New CLI Option**:

   - Add argument in `main.py`
   - Map to config in `create_config()`

4. **New Gesture Type**:

   - Add to `Gesture` enum in `gesture_detector.py`
   - Update detection logic

5. **New Rendering**:
   - Add method to `fruit_ninja_game.py`
   - Call from `render()` method

## Thread Safety

Current implementation:

- **Single-threaded**: All processing in main loop
- **Synchronous**: Sequential frame processing
- **State**: Owned by FruitNinjaGame instance

Future considerations for multi-threading:

- Separate video capture thread
- Background gesture processing
- Thread-safe trail updates

## Performance Considerations

### Bottlenecks

1. MediaPipe inference (~30-60ms per frame)
2. Trail rendering (O(n) where n = trail points)
3. Collision detection (O(f\*t) where f = fruits, t = trail points)

### Optimizations

- Deque for automatic trail size limiting
- Early return for no-gesture case
- Only check recent trail points for collision
- Spatial partitioning possible for many fruits

## Error Handling

```
main()
    ├─→ try/except KeyboardInterrupt → Clean exit
    ├─→ try/except Exception → Error message
    └─→ if args.debug → Re-raise for traceback

FruitNinjaGame.run()
    ├─→ if not ret → break (camera failure)
    └─→ cv2.waitKey() → 'q' to quit
```

## Testing Strategy

1. **Import Tests**: Verify all modules load
2. **Config Tests**: Validate settings and presets
3. **Instantiation Tests**: Game can be created
4. **Integration Tests**: Components work together
5. **Manual Tests**: Run game and verify behavior
