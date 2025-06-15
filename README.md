# 🤖 Hand Gesture Volume Control

Control your system volume using hand gestures and your webcam!  
Built with **OpenCV**, **MediaPipe**, and **cross-platform system volume APIs**, this application works on **Windows**, **Linux**, and **macOS**.

---

## 📸 Demo

![Hand Volume Control - 85%](Screenshots/Screenshot%20From%202025-06-15%2004-30-38.png)  
![Hand Volume Control - 51%](Screenshots/Screenshot%20From%202025-06-15%2004-30-53.png)

---

## 🧠 How It Works

- Uses **MediaPipe Hands** to detect landmarks of your hand via webcam.
- Measures the distance between **thumb tip** and **index finger tip**.
- Converts that distance into a **volume level**.
- Sets system volume accordingly using:
  - **pycaw** on Windows (via COM)
  - **amixer** on Linux (via PulseAudio)
  - **osascript** on macOS (via AppleScript)

---

## 💻 Features

- 📦 Cross-platform (Windows, Linux, macOS)
- 🔍 Real-time hand tracking
- 📊 Visual volume bar
- 🔊 Smooth audio volume control
- 💡 Auto-detects OS and applies correct volume API

---

## 🛠️ Requirements

Install the dependencies using pip:

```bash
pip install opencv-python mediapipe numpy
```

Additional OS-specific requirements:

### 🔵 Windows
```bash
pip install pycaw comtypes
```

### 🟢 Linux
```bash
sudo apt install alsa-utils
```

### 🍎 macOS
AppleScript is pre-installed, no additional dependencies needed.

---

## 🏁 How to Run

```bash
python Volume_Control.py
```

- Press the **spacebar** to exit.
- Make sure your webcam is working.

---

## 🧩 Project Structure

```
Volume-control-with-hand-detection/
├── Volume_Control.py        # Main app
├── Screenshots/             # Screenshots for demo
│   ├── Screenshot From 2025-06-15 04-30-38.png
│   └── Screenshot From 2025-06-15 04-30-53.png
├── README.md                # You're here
```

---

## 📚 Explanation of Key Libraries

- **OpenCV** – for video capture and GUI display.
- **MediaPipe** – to detect hand landmarks.
- **NumPy** – for linear interpolation and distance calculation.
- **pycaw / amixer / osascript** – platform-specific volume control.

---

## 🔐 Permissions

Make sure your system allows access to:
- **Webcam**
- **System audio** (especially on Linux/macOS where you may need permission to execute volume scripts)

---

## 💡 Credits

Developed by: **Rajesh Kumar Jogi**  
Inspired by real-world gesture-based UI applications and media control systems.

---

## 📜 License

This project is open source and free to use under the MIT License.
