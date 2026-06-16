# 🚀 Setup & Installation Guide

Welcome to the **Local AI Pose Processor**! This guide will walk you through setting up the virtual environment, installing dependencies, and running the application safely.

##  Prerequisites

Before starting, ensure you have the following installed on your system:
1. **Python 3.9 or higher** ([Download here](https://www.python.org/downloads/))
2. **Git** (for version control)
3. **LM Studio** ([Download here](https://lmstudio.ai/)) - *Required for local AI.*
4. **FFmpeg** (Crucial for OpenCV video processing)
   - *Windows:* Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) and add to PATH.
   - *Mac:* `brew install ffmpeg`
   - *Ubuntu/Debian:* `sudo apt install ffmpeg`

---

## ️ Step 1: Project Setup
Using a virtual environment isolates the project dependencies and prevents conflicts with other Python projects.

Windows:

bash  

python -m venv venv
venv\Scripts\activate

Mac / Linux:

python3 -m venv venv
source venv/bin/activate

📦 Step 3: Install Dependencies
With the virtual environment activated, install the required Python libraries:

pip install -r requirements.txt

1
️ Precaution / Troubleshooting:
If you encounter conflicts between mediapipe and opencv-python, try installing the headless version of OpenCV instead:

pip uninstall opencv-python
pip install opencv-python-headless 

▶️ Step 4: Running the Application
1. Start LM Studio Server
The AI features require LM Studio to be running in the background.
Open LM Studio.
Download and load your preferred model (e.g., Llama 3, Mistral).
Go to the Local Server tab (the <-> icon on the left).
Click Start Server. Ensure it says "Server is running on port 1234".
2. Launch the App
In your activated terminal, run the main entry point: