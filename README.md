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

- **Input**: Real-time RGB video (640×480 @ 30 FPS typical)
- **Annotations**: Hand landmarks generated on-the-fly by MediaPipe Hands
- **Gesture labels**: Dynamically inferred from fingertip motion (4 classes: `SWIPE_LEFT`, `SWIPE_RIGHT`, `SWIPE_UP`, `SWIPE_DOWN`)

> 💡 _No pre-collected dataset is needed—interaction is continuous and user-driven._

## Method / Approach

### Architecture

- **Input**: Webcam feed → RGB frame
- **Hand Detection**: MediaPipe Hands (BlazePalm + Hand Landmark CNN)
- **Gesture Engine**: Temporal velocity analysis of index fingertip (landmark #8)
- **Game Logic**: Fruit physics, collision, scoring
- **Output**: Annotated frame with fruits, score, and visual feedback

### Key Libraries

| Layer        | Technology                             |
| ------------ | -------------------------------------- |
| Prototype    | Python, OpenCV, MediaPipe              |
| Production   | C++, OpenCV, MediaPipe (C++ API), Qt 6 |
| Build System | CMake                                  |
| Rendering    | Qt Widgets / QImage                    |

## Results

### Performance (on mid-range laptop: i5, 8GB RAM)

- **End-to-end latency**: ~60–80 ms (camera → slice response)
- **Hand tracking**: 25–30 FPS (stable under good lighting)
- **Gesture accuracy**: >90% swipe direction accuracy with tuned thresholds

### Example Output

![MiniNinja gameplay](assets/demo.gif)  
_Player slicing fruits with hand swipes. Juice splashes on hit!_

> 📌 _Demo video/GIF recommended in `assets/`_

## Usage

### Run Python Prototype

```bash
# 1. Clone repo
git clone https://github.com/bigalex95/minininja.git
cd minininja

# 2. Install dependencies
cd proto
pip install -r requirements.txt  # opencv-python, mediapipe

# 3. Run!
python fruit_ninja_game.py
```
