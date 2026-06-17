import socket
import sounddevice as sd
import vosk
import json
import keyboard
import queue
import sys

# ==== UDP setup ====
ESP32_IP = "192.168.4.1"
ESP32_PORT = 1234
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Test connection
try:
    sock.sendto(b"CONNECTION_TEST", (ESP32_IP, ESP32_PORT))
    print(f"✅ Connected to ESP32 at {ESP32_IP}:{ESP32_PORT}")
except Exception as e:
    print(f"❌ Failed to connect: {e}")

# ==== Load Vosk model ====
# Download a model from https://alphacephei.com/vosk/models and set the path below
MODEL_PATH = "vosk-model-small-en-us-0.15"
model = vosk.Model(MODEL_PATH)

# Queue to communicate between audio callback and main thread
q = queue.Queue()

# Movement commands (Hindi, English, Hinglish variants)
movement_commands = {
    "forward": "FORWARD",
    "aage": "FORWARD",
    "peeche": "BACKWARD",
    "backward": "BACKWARD",
    "left": "LEFT",
    "baaye": "LEFT",
    "right": "RIGHT",
    "daaye": "RIGHT",
    "stop": "STOP",
    "ruk": "STOP",
    "forward left": "FORWARD_LEFT",
    "aage baaye": "FORWARD_LEFT",
    "forward right": "FORWARD_RIGHT",
    "aage daaye": "FORWARD_RIGHT",
    "backward left": "BACKWARD_LEFT",
    "peeche baaye": "BACKWARD_LEFT",
    "backward right": "BACKWARD_RIGHT",
    "peeche daaye": "BACKWARD_RIGHT"
}

# Speed commands
speed_commands = {
    "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
    "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
    "q": "q",
    "slow": "0",
    "tezz": "q"
}

last_movement_command = None
last_speed_command = None

print("🎤 Offline Voice Control Started!")
print("Press SPACE to listen, SHIFT to STOP, ESC to quit")

# ==== Audio callback ====
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# ==== Main loop ====
with sd.RawInputStream(samplerate=16000, blocksize = 8000, dtype='int16',
                       channels=1, callback=callback):
    rec = vosk.KaldiRecognizer(model, 16000)
    while True:
        try:
            if keyboard.is_pressed('esc'):
                print("👋 Exiting...")
                break

            # Instant STOP
            if keyboard.is_pressed('shift'):
                if last_movement_command != "STOP":
                    sock.sendto("STOP".encode(), (ESP32_IP, ESP32_PORT))
                    last_movement_command = "STOP"
                    print("📤 Sent STOP (SHIFT key)")
                continue

            # Listen on SPACE
            if keyboard.is_pressed('space'):
                print("🎙️ Listening...")
                while True:
                    data = q.get()
                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        text = result.get("text", "").lower()
                        print(f"🗣️ Heard: {text}")

                        # Movement commands
                        for key_phrase, cmd in movement_commands.items():
                            if key_phrase in text:
                                if cmd != last_movement_command:
                                    sock.sendto(cmd.encode(), (ESP32_IP, ESP32_PORT))
                                    last_movement_command = cmd
                                    print(f"📤 Sent movement: {cmd}")
                                break

                        # Speed commands
                        for key_phrase, cmd in speed_commands.items():
                            if key_phrase in text:
                                if cmd != last_speed_command:
                                    sock.sendto(cmd.encode(), (ESP32_IP, ESP32_PORT))
                                    last_speed_command = cmd
                                    print(f"🎛️ Sent speed: {cmd}")
                                break
                        break  # stop after one recognition

        except KeyboardInterrupt:
            break

sock.close()
