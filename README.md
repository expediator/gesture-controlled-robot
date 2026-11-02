<div align="center">

# 🤖 Gesture & Voice Controlled RC Car

**Real-time hand gesture + offline voice control for an ESP32 robot car**

[![GitHub](https://img.shields.io/badge/GitHub-expediator%2Fgesture--controlled--robot-181717?style=flat-square&logo=github)](https://github.com/expediator/gesture-controlled-robot)
[![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white)](https://opencv.org)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0097A7?style=flat-square)](https://mediapipe.dev)
[![Arduino](https://img.shields.io/badge/Arduino%2FESP32-00979D?style=flat-square&logo=arduino&logoColor=white)](https://arduino.cc)

A fully functional RC robot car controlled by a laptop camera using hand gestures (MediaPipe) or offline voice commands (Vosk). Commands sent over UDP to an ESP32 microcontroller. Built solo in 4 weeks.

</div>

---

## Control Modes

### Gesture Control (`gesture_control.py`)

| Gesture | Command |
|---------|---------|
| Index finger up | Forward |
| Pinky up | Backward |
| Thumb left | Turn left |
| Thumb right | Turn right |
| Fist / no hand | Stop |

### Voice Control (`voice_control.py`)

| Spoken word | Command |
|-------------|---------|
| "forward" / "go" | Forward |
| "back" / "reverse" | Backward |
| "left" | Turn left |
| "right" | Turn right |
| "stop" | Stop |

Fully offline — no internet, no cloud API required.

## Architecture

```
Laptop (webcam / mic)
       ↓  MediaPipe Hands / Vosk STT
gesture_control.py  or  voice_control.py
       ↓  UDP packet over WiFi (same LAN)
ESP32 (Arduino C firmware)
       ↓  GPIO PWM signals
L298N Motor Driver
       ↓
4 × DC Motors → Movement
```

## Hardware

| Component | Purpose |
|-----------|---------|
| ESP32 | WiFi microcontroller — receives UDP commands |
| L298N | Dual H-bridge motor driver |
| 4× DC motors | Drive wheels |
| LiPo battery | Powers motors + ESP32 |
| HC-SR04 | Ultrasonic obstacle detection |

## Setup

```bash
pip install mediapipe opencv-python vosk pyaudio
```

Download [vosk-model-small-en-us-0.15](https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip) and extract into the project folder.

```bash
python gesture_control.py   # set ESP32_IP at top of file
python voice_control.py     # set ESP32_IP at top of file
```

## Files

```
gesture-controlled-robot/
├── gesture_control.py    ← Webcam + MediaPipe → UDP
├── voice_control.py      ← Vosk STT → UDP
└── README.md
```

---

<div align="center">
An <strong>Expediator Inc.</strong> project · © 2026 · <a href="https://expediator.github.io/resume/">Portfolio</a>
</div>