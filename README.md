# 🤖 Hand Gesture & Voice Controlled RC Car

Real-time hand gesture recognition and offline voice control for an **ESP32-based RC robot car**, using a webcam, MediaPipe, and Vosk speech recognition.

**Source:** [github.com/expediator/gesture-controlled-robot](https://github.com/expediator/gesture-controlled-robot) &nbsp;·&nbsp; **Portfolio:** [expediator.github.io/resume](https://expediator.github.io/resume/)

---

## Control Modes

### Gesture Control (`gesture_control.py`)
Uses your webcam to detect hand gestures via MediaPipe Hands, then sends movement commands over UDP to an ESP32 on the robot.

| Gesture | Command |
|---|---|
| Index finger up | Forward |
| Pinky up | Backward |
| Thumb left | Turn left |
| Thumb right | Turn right |
| Fist / no hand | Stop |

### Voice Control (`voice_control.py`)
Offline speech recognition using **Vosk** — no internet required. Recognizes English and Hindi commands sent to the robot over UDP.

| Spoken word | Command |
|---|---|
| "forward" / "go" | Forward |
| "back" / "reverse" | Backward |
| "left" | Turn left |
| "right" | Turn right |
| "stop" | Stop |

## Hardware

- **ESP32** microcontroller (receives UDP commands over WiFi)
- **L298N motor driver** — controls 4 DC motors
- **LiPo battery** — powers motors and ESP32
- **Ultrasonic sensor (HC-SR04)** — obstacle detection
- Custom chassis, wheel assembly

## Architecture

```
Laptop (webcam/mic)
    ↓ MediaPipe / Vosk
gesture_control.py / voice_control.py
    ↓ UDP packet (WiFi, same network)
ESP32 (Arduino C firmware)
    ↓ GPIO signals
L298N Motor Driver
    ↓
4 DC Motors → Movement
```

## Setup

### Python dependencies
```bash
pip install mediapipe opencv-python vosk pyaudio
```

### Vosk model
Download the small English model:
```
https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
```
Extract it as `vosk-model-small-en-us-0.15/` in the same directory as the scripts.

### Run gesture control
```bash
python gesture_control.py
```
Set `ESP32_IP` in the script to your robot's IP address.

### Run voice control
```bash
python voice_control.py
```

## Files

```
gesture-controlled-robot/
├── gesture_control.py    ← Webcam + MediaPipe → UDP commands
├── voice_control.py      ← Vosk speech recognition → UDP commands
└── README.md
```

## Built in 4 weeks as a solo project.
