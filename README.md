# Gesture Controlled Robot

Real-time hand gesture and offline voice control for an ESP32-based RC robot, using a webcam and MediaPipe.

## Modes

### Gesture Control (`gesture_control.py`)
- Detects hand landmarks via **MediaPipe Hands**
- Maps finger combinations to robot commands sent over **UDP** to an ESP32 in AP mode
- Includes a **pinch-distance speed controller** (thumb + index = SPEED mode, distance → 0–100%)

| Gesture | Command |
|---|---|
| Index finger only | FORWARD |
| Index + Middle | LEFT |
| Index + Middle + Ring | RIGHT |
| All four fingers | BACKWARD |
| Fist | STOP |
| Thumb + Index (pinch) | SPEED CONTROL |

### Voice Control (`voice_control.py`)
- Fully **offline** speech recognition using **Vosk** (no API key needed)
- Bilingual: understands English and Hindi/Hinglish commands
- Press SPACE to listen, SHIFT for instant STOP, ESC to quit

| Voice Command | Action |
|---|---|
| "forward" / "aage" | FORWARD |
| "backward" / "peeche" | BACKWARD |
| "left" / "baaye" | LEFT |
| "right" / "daaye" | RIGHT |
| "stop" / "ruk" | STOP |
| "slow" / "tezz" | Speed 0% / 100% |

## Setup

```bash
pip install opencv-python mediapipe
python gesture_control.py
```

For voice control:
```bash
pip install sounddevice vosk keyboard
# Download a Vosk model from https://alphacephei.com/vosk/models
# Update MODEL_PATH in voice_control.py
python voice_control.py
```

## Hardware

- **ESP32** in AP mode (IP: `192.168.4.1`, UDP port `1234`) — update `ESP32_IP` in the script if different
- Any standard webcam

## Stack

`Python` · `OpenCV` · `MediaPipe` · `Vosk` · `socket (UDP)` · `Arduino (ESP32)`
