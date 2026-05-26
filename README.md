# Face Recognition Attendance System

A real-time automated attendance system that uses facial recognition to detect, identify, and log attendance — eliminating the need for manual roll calls.

---

## Demo

> *(Add a screen recording GIF or screenshot here)*

---

## Features

- Real-time face detection and recognition via webcam
- Automatically marks and logs attendance with timestamp to a CSV file
- Skips duplicate entries — each person is marked only once per session
- Voice announcement when attendance is marked
- Displays name label and bounding box on live video feed
- Handles unknown faces gracefully without crashing

---

## Tech Stack

| Area | Tools |
|---|---|
| Face Recognition | `face_recognition`, `dlib` |
| Computer Vision | `OpenCV` |
| Numerical Computing | `NumPy` |
| Text-to-Speech | `pyttsx3` |
| Concurrency | `threading` |
| Data Logging | `csv`, `datetime` |

---

## How It Works

1. **Encoding known faces** — On startup, the system reads all images from the `Images/` folder, detects faces, and computes 128-dimensional face encodings for each person.
2. **Real-time detection** — Each webcam frame is scanned for faces. Detected faces are encoded on the fly.
3. **Matching** — The system compares live encodings against known encodings using Euclidean face distance. The closest match below a confidence threshold is selected.
4. **Logging** — On a successful match, the person's name and current timestamp are written to `attendance.csv`. Each person is logged only once per session using a set to track already-marked names.
5. **Voice feedback** — A separate thread triggers a voice announcement so audio doesn't block the video feed.

---

## Project Structure

```
face-recognition-attendance/
│
├── Images/                  # Folder containing known face images
│   ├── John.jpg
│   ├── Jane.jpg
│   └── ...
│
├── attendance.csv           # Auto-generated attendance log
├── main.py                  # Main application script
├── requirements.txt         # Python dependencies
└── README.md
```

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/Squash2453/face-recognition-attendance.git
cd face-recognition-attendance
```

### 2. Install dependencies

> It is recommended to use a virtual environment.

```bash
pip install -r requirements.txt
```

> **Note:** `face_recognition` requires `dlib` which requires CMake. If installation fails, install CMake first:
> ```bash
> pip install cmake
> pip install dlib
> pip install face_recognition
> ```

### 3. Add known faces

Place `.jpg` or `.png` images of known individuals inside the `Images/` folder. Each file should be named after the person:

```
Images/
├── Shibli.jpg
├── John.jpg
```

### 4. Run the system

```bash
python main.py
```

Press **`q`** to quit the webcam window.

---

## Output

The system generates an `attendance.csv` file that logs each recognized person with their timestamp:

```
Name, Time
Shibli, 09:15:32
John, 09:16:04
```

---

## Known Limitations

- Works best with clear, front-facing images in the `Images/` folder
- Recognition accuracy may drop in low-light conditions
- Currently marks attendance once per session (resets on restart)

---

## Requirements

```
opencv-python
face_recognition
numpy
pyttsx3
```

> See `requirements.txt` for exact versions.
