<div align="center">

# 😴 SleepGuard — Real-Time Drowsiness Detection System

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-0F9D58?style=for-the-badge&logo=google&logoColor=white)](https://mediapipe.dev)
[![Flask](https://img.shields.io/badge/Flask-Web_UI-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**AI-powered real-time drowsiness detection using Eye Aspect Ratio (EAR) algorithm.**  
Detects multiple faces simultaneously, tracks individuals, and triggers alerts when sleeping is detected.

![Demo Banner](https://raw.githubusercontent.com/YOUR_USERNAME/sleepguard/main/assets/banner.png)

</div>

---

## 📸 Screenshots

<div align="center">

| Live Detection | Alert Triggered | Multi-Face Tracking |
|:-:|:-:|:-:|
| ![Live](https://raw.githubusercontent.com/YOUR_USERNAME/sleepguard/main/assets/live.png) | ![Alert](https://raw.githubusercontent.com/YOUR_USERNAME/sleepguard/main/assets/alert.png) | ![Multi](https://raw.githubusercontent.com/YOUR_USERNAME/sleepguard/main/assets/multi.png) |
| Real-time EAR monitoring | Red alert when sleeping | Tracks up to 5 faces |

</div>

---

## ✨ Features

- 🎯 **Real-Time Detection** — Processes webcam feed live using MediaPipe Face Mesh (468 landmarks)
- 👥 **Multi-Face Tracking** — Detects and tracks up to 5 individuals simultaneously with unique IDs
- 📊 **EAR Algorithm** — Eye Aspect Ratio calculation for accurate blink/sleep detection
- 🌐 **Web Dashboard** — Beautiful dark-themed UI accessible from any browser
- 🔔 **Instant Alerts** — Visual alarm + browser audio beep when drowsiness is detected
- 📝 **Event Log** — Timestamped log of all sleeping events in real-time
- ⚡ **1-Click Launch** — Double-click `START.bat` and everything runs automatically

---

## 🧠 How It Works

```
Webcam Feed
    │
    ▼
MediaPipe Face Mesh (468 landmarks per face)
    │
    ▼
EAR Calculation ──── Left Eye + Right Eye
    │                (A + B) / (2 × C)
    ▼
EAR < 0.22 for 1+ seconds?
    │
    ├── YES ──► SLEEPING ALERT 🚨
    │           • Red banner on video
    │           • Audio beep alarm
    │           • Screen flash effect
    │           • Event logged
    │
    └── NO  ──► Normal monitoring ✅
```

### EAR Formula

```
     |p2-p6| + |p3-p5|
EAR = ─────────────────
          2 × |p1-p4|
```

| Condition | EAR Value |
|-----------|-----------|
| Eyes Open | ~0.30+ |
| Drowsy | ~0.20–0.25 |
| Eyes Closed / Sleeping | < 0.22 |

---

## 🚀 Quick Start

### Method 1 — 1-Click Launch (Recommended)

```
1. Download all files
2. Put them in one folder
3. Double-click START.bat
4. Browser opens automatically at http://localhost:5000
```

> ✅ Automatically installs dependencies on first run!

### Method 2 — Manual

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/sleepguard.git
cd sleepguard

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Then open **http://localhost:5000** in your browser.

---

## 📁 Project Structure

```
sleepguard/
│
├── 🖱️  START.bat              ← Double-click to launch (Windows)
├── 🐍  app.py                 ← Flask web server
├── 🔍  face_detection.py      ← Core detection engine
├── 📋  requirements.txt       ← Python dependencies
│
└── 📂  templates/
    └── 🌐  index.html         ← Web dashboard UI
```

---

## ⚙️ Configuration

Edit these values in `face_detection.py` to tune detection:

```python
EAR_THRESHOLD  = 0.22   # Lower = more sensitive (try 0.20–0.25)
SLEEPING_TIME  = 1.0    # Seconds before alarm triggers
MAX_TRACK_DIST = 50     # Max pixel distance to match same face
FRAME_WIDTH    = 640    # Camera resolution width
FRAME_HEIGHT   = 480    # Camera resolution height
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `opencv-python` | 4.x | Video capture & drawing |
| `mediapipe` | Latest | Face mesh landmarks |
| `numpy` | Latest | Math & distance calculations |
| `flask` | Latest | Web server & UI |

---

## 🖥️ Web Dashboard

<div align="center">

![Dashboard](https://raw.githubusercontent.com/YOUR_USERNAME/sleepguard/main/assets/dashboard.png)

</div>

The web dashboard includes:
- **Live MJPEG feed** — Annotated video stream with bounding boxes, IDs, and EAR values
- **People counter** — Number of faces currently detected
- **Sleeping counter** — Number of people currently sleeping
- **System status panel** — EAR threshold, timer, alarm state
- **Real-time event log** — Timestamped alerts and clear events
- **Audio alarm** — Browser Web Audio API beep (no extra software needed)

---

## 🔧 Tech Stack

```
Frontend  →  HTML5 + CSS3 + Vanilla JS (Web Audio API)
Backend   →  Python + Flask (MJPEG streaming)
AI/CV     →  MediaPipe Face Mesh + OpenCV
Algorithm →  Eye Aspect Ratio (EAR) — Soukupová & Čech (2016)
```

---

## ⚠️ Known Limitations

- Requires good lighting for accurate detection
- EAR threshold is global (not per-person calibrated)
- Windows only for `START.bat` (use `python app.py` on Mac/Linux)
- Webcam must be available and not in use by another app

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|---------|
| Black screen / no feed | Check webcam is connected and not used by another app |
| `mediapipe` install error | Try `pip install mediapipe --upgrade` |
| Browser doesn't open | Manually go to `http://localhost:5000` |
| Too many false positives | Increase `EAR_THRESHOLD` to `0.25` |
| Missing detections | Improve lighting or decrease `EAR_THRESHOLD` to `0.20` |

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use and modify!

---

## 🙋 Author

Made with ❤️ by **[Your Name](https://github.com/YOUR_USERNAME)**

If you found this useful, please ⭐ the repo!

---

<div align="center">

**[⬆ Back to Top](#-sleepguard--real-time-drowsiness-detection-system)**

</div>