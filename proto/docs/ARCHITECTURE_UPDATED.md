# System Architecture - Updated with Leaderboard

## Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Fruit Ninja CV                              │
│                     Computer Vision Game System                      │
└─────────────────────────────────────────────────────────────────────┘

                              main.py
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
              ┌─────────┐  ┌─────────┐  ┌──────────┐
              │  Core   │  │   CV    │  │   UI     │
              │ Module  │  │ Module  │  │  Module  │
              └─────────┘  └─────────┘  └──────────┘
                    │            │            │
                    └────────────┼────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   Leaderboard   │
                        │     Module      │
                        └─────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │    Supabase     │
                        │  Cloud Database │
                        └─────────────────┘
```

## Module Details

### 1. Core Module (`src/core/`)

```
src/core/
├── config.py          → GameConfig, DifficultyLevel
├── entities.py        → Fruit, Trail, TrailPoint
└── game.py           → FruitNinjaGame (Main Controller)
```

**Responsibilities:**

- Game state management
- Entity physics and collision
- Game loop orchestration
- Configuration management

**Dependencies:**

- cv module (HandTracker, GestureDetector)
- entities module (Fruit, Trail)
- Standard library (time, random)
- opencv-python

### 2. CV Module (`src/cv/`)

```
src/cv/
├── hand_tracker.py      → HandTracker (MediaPipe)
└── gesture_detector.py  → GestureDetector, Gesture
```

**Responsibilities:**

- Hand detection and tracking
- Landmark extraction
- Gesture recognition
- Motion analysis

**Dependencies:**

- MediaPipe
- OpenCV
- Standard library (collections)

### 3. Leaderboard Module (`src/leaderboard/`)

```
src/leaderboard/
└── leaderboard.py    → Leaderboard (Supabase Client)
```

**Responsibilities:**

- Score submission
- Leaderboard retrieval
- Player statistics
- Database communication

**Dependencies:**

- Supabase Python SDK
- python-dotenv
- Standard library (os, datetime)

### 4. UI Module (`src/ui/`)

```
src/ui/
└── leaderboard_ui.py  → LeaderboardUI (Rendering)
```

**Responsibilities:**

- Leaderboard visualization
- Score display
- UI overlays
- Visual feedback

**Dependencies:**

- OpenCV
- NumPy (via OpenCV)

## Data Flow

### Game Loop

```
┌──────────────────────────────────────────────────────────────┐
│                        Game Loop                              │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │  Capture Frame   │ (OpenCV)
                    └──────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │  Track Hands     │ (MediaPipe)
                    └──────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │ Detect Gestures  │ (GestureDetector)
                    └──────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │  Update Entities │ (Physics)
                    └──────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │ Check Collisions │
                    └──────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │  Render Frame    │ (OpenCV)
                    └──────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │   Display        │
                    └──────────────────┘
```

### Leaderboard Flow

```
┌──────────────────────────────────────────────────────────────┐
│                     Leaderboard Flow                          │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │   Game Ends      │
                    │  (Final Score)   │
                    └──────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │  Submit Score    │ (Leaderboard)
                    └──────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │  Supabase API    │ (HTTP POST)
                    └──────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │   PostgreSQL     │ (Database)
                    └──────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │ Fetch Top Scores │ (HTTP GET)
                    └──────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │  Display to User │ (Console/UI)
                    └──────────────────┘
```

## Component Interactions

### Initialization

```python
main.py
  ├─> load_dotenv()                    # Load .env
  ├─> parse_args()                     # CLI arguments
  ├─> create_config()                  # GameConfig
  │
  ├─> FruitNinjaGame(config)
  │     ├─> HandTracker()              # Initialize MediaPipe
  │     ├─> GestureDetector()          # Initialize gesture tracking
  │     └─> Trail()                    # Initialize visual trail
  │
  └─> game.run()                       # Start game loop
        │
        └─> (on exit) Leaderboard()    # Submit score
              └─> Supabase.insert()    # Save to database
```

### Runtime

```python
# Game Loop (60 FPS)
while running:
    frame = capture_frame()                  # OpenCV
    hands = hand_tracker.process(frame)      # MediaPipe

    if hands:
        fingertip = hands[0].landmark[8]     # Index finger
        gesture = gesture_detector.update(fingertip)

        if gesture == Gesture.SLASH:
            for fruit in fruits:
                if fruit.check_collision(fingertip):
                    score += 1
                    fruits.remove(fruit)

    update_physics()                         # Gravity, motion
    render_frame()                           # Draw everything
    display()                                # Show window
```

## External Services

### Supabase Integration

```
Application                    Supabase Cloud
    │                                │
    │  1. Submit Score                │
    ├──────────────────────────────>  │
    │     POST /rest/v1/leaderboard   │
    │     {                           │
    │       "player_name": "...",     │
    │       "score": 123,             │
    │       "difficulty": "medium"    │
    │     }                           │
    │                                │
    │  2. Fetch Top Scores           │
    ├──────────────────────────────> │
    │     GET /rest/v1/leaderboard   │
    │     ?order=score.desc           │
    │     &limit=10                  │
    │                                │
    │  3. Response                   │
    │ <────────────────────────────── │
    │     [                          │
    │       {                        │
    │         "player_name": "...",  │
    │         "score": 456,          │
    │         "created_at": "..."    │
    │       },                       │
    │       ...                      │
    │     ]                          │
    │                                │
```

## Configuration Flow

```
Environment Variables (.env)
         │
         ├─> SUPABASE_URL  ──┐
         └─> SUPABASE_KEY  ──┼──> python-dotenv
                             │
                             ▼
                    os.getenv('...')
                             │
                             ▼
                    Leaderboard.__init__()
                             │
                             ▼
                    supabase.create_client()
```

## Error Handling

```
Try Submit Score
    │
    ├─> Success? ──> ✅ Show confirmation
    │
    └─> Failed?
          │
          ├─> Network error? ──> ⚠️  Show offline message
          ├─> Auth error? ──────> ❌ Check credentials
          └─> Unknown error? ───> 🐛 Debug mode info
```

## Performance Considerations

### Optimizations

- **Frame Rate**: 60 FPS target
- **Hand Tracking**: 30 FPS sufficient for MediaPipe
- **Database**: Async operations (non-blocking)
- **Indexing**: Supabase indices for fast queries

### Resource Usage

- **Memory**: ~100-200 MB (MediaPipe models)
- **CPU**: ~20-30% (single core)
- **Network**: Minimal (only score submission)
- **Database**: <1 KB per score entry

## Security Model

```
Application (Client)
    │
    ├─> Uses anon/public key (safe to expose)
    │
    ▼
Supabase (Server)
    │
    ├─> Row Level Security (RLS)
    │   ├─> READ: Anyone (public leaderboard)
    │   ├─> INSERT: Anyone (submit scores)
    │   ├─> UPDATE: None (prevent cheating)
    │   └─> DELETE: None (preserve history)
    │
    └─> PostgreSQL Database
        └─> Secure server-side validation
```

## Deployment Architecture

```
Development
    │
    ├─> Local Python environment
    ├─> Local webcam
    ├─> .env file (local credentials)
    └─> Direct Supabase access
         │
         ▼
Production/Distribution
    │
    ├─> Package with PyInstaller/py2exe
    ├─> Include .env.example
    ├─> User provides own Supabase credentials
    └─> OR use shared public Supabase instance
```

## Module Import Graph

```
main.py
  │
  ├─> src.core.game (FruitNinjaGame)
  │     ├─> src.core.config (GameConfig, DifficultyLevel)
  │     ├─> src.core.entities (Fruit, Trail)
  │     ├─> src.cv.hand_tracker (HandTracker)
  │     └─> src.cv.gesture_detector (GestureDetector, Gesture)
  │
  ├─> src.leaderboard.leaderboard (Leaderboard)
  │     └─> supabase (external)
  │
  └─> src.ui.leaderboard_ui (LeaderboardUI)
        └─> opencv-python (external)
```

## Technology Stack

```
┌─────────────────────────────────────────┐
│           Application Layer              │
│  (Python 3.11+ / Game Logic)            │
└─────────────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
┌─────────────┐    ┌─────────────────┐
│  Computer   │    │   Leaderboard   │
│   Vision    │    │    System       │
└─────────────┘    └─────────────────┘
        │                   │
        ▼                   ▼
┌─────────────┐    ┌─────────────────┐
│  MediaPipe  │    │    Supabase     │
│   OpenCV    │    │   PostgreSQL    │
└─────────────┘    └─────────────────┘
```

---

This architecture provides:

- ✅ Clear separation of concerns
- ✅ Modular design
- ✅ Easy to test and extend
- ✅ Cloud-connected features
- ✅ Secure credential management
