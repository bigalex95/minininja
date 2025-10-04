minininja/
│
├── README.md # Project overview, build instructions
├── LICENSE # MIT, GPL, Apache, etc.
├── .gitignore # Python + C++ + Qt + IDE ignores
├── CMakeLists.txt # Root CMake (for C++ build)
│
├── proto/ # 🐍 PYTHON PROTOTYPE (frozen after port)
│ ├── hand_tracker.py
│ ├── gesture_detector.py
│ ├── fruit_ninja_game.py
│ └── requirements.txt # mediapipe, opencv-python, etc.
│
├── src/ # 🧱 C++ / QT SOURCE CODE
│ ├── core/ # Core logic (portable, no Qt)
│ │ ├── gesture_detector.h
│ │ ├── gesture_detector.cpp
│ │ └── game_state.h/cpp
│ │
│ ├── cv/ # Computer vision layer
│ │ ├── hand_tracker.h
│ │ ├── hand_tracker.cpp # MediaPipe C++ wrapper
│ │ └── camera_manager.h/cpp
│ │
│ ├── gui/ # Qt UI layer
│ │ ├── mainwindow.h/cpp
│ │ ├── gameview.h/cpp # Custom widget for rendering
│ │ └── main.cpp # Qt entry point
│ │
│ └── CMakeLists.txt # CMake for src/
│
├── assets/ # 🎨 MEDIA & RESOURCES
│ ├── images/
│ │ ├── fruits/ # fruit sprites (or generate procedurally)
│ │ ├── ui/ # buttons, dojo background, etc.
│ │ └── logo_minininja.png
│ │
│ └── sounds/ # [Optional] slice, whoosh, score sounds
│ ├── slice.wav
│ └── level_up.wav
│
├── docs/ # 📚 DESIGN & MIGRATION
│ ├── ARCHITECTURE.md # High-level design
│ ├── PROTO_TO_CPP.md # Critical: how Python maps to C++
│ └── BUILD_INSTRUCTIONS.md # How to build on Win/macOS/Linux
│
├── scripts/ # 🛠️ HELPER SCRIPTS
│ ├── build.sh # Cross-platform build helper
│ └── run_proto.sh # Quick launch for Python prototype
│
├── tests/ # [Optional] Unit tests (GoogleTest, etc.)
│ └── core_tests.cpp
│
└── third_party/ # [Optional] Vendored deps (if not using vcpkg/conan)
└── (avoid if possible — prefer package managers)
