# Color Object Tracker 🎨

A simple real-time color-based object tracking system using OpenCV and Python.

---

## 🎯 Summary

This project tracks the largest object of a specified color (e.g., red) in a video or webcam feed, highlights it with a bounding box and center point, and lets you pause/resume tracking.

---

## ✨ Features

- Real-time object tracking
- HSV color range filtering
- Pause/resume with keyboard
- Simple and customizable

---

## ⚙️ Installation

```bash
pip install opencv-python numpy
```
🚀 Usage
Run the tracker:
```bash
python color_tracker.py
```
To use webcam instead of video file:
```bash
python tracker = ColorTracker(0)
```
## Controls
Press P to pause/resume

Press Q to quit
## 📸 Example Outputs

Tracking a red object in video 1  
![](Screenshot129.png)

Tracking a red object in video 2  
![](Screenshot133.png)

