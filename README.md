# 🎥 Local AI Pose Processor

A lightweight, privacy-focused desktop application that analyzes human posture in videos using CPU-optimized pose estimation and local Large Language Models (LLMs). 

Built with a highly modular **10-file architecture**, this system ensures fault isolation, easy customization, and seamless Git collaboration.

## ✨ Key Features

-  **100% Local & Private:** Runs entirely on your machine. Connects to LM Studio for AI analysis—no external API keys or cloud costs.
- ⚡ **CPU-Optimized:** Uses MediaPipe for lightweight pose detection, making it perfect for low-end devices and laptops without dedicated GPUs.
- 🧩 **Modular 10-File Architecture:** Separation of Concerns (SoC). If one module crashes, the rest of the app keeps running.
- 📊 **Comprehensive JSON Output:** Generates unique, timestamped JSON files containing frame-by-frame pose data, video metadata, and the exact LM configuration used.
- 🎨 **Modern UI:** Built with `customtkinter` for a sleek, dark/light mode interface that never freezes (thanks to background threading).
- ⚙️ **Highly Configurable:** Adjust AI parameters (Temperature, Top-K, Top-P, System Prompts) directly in the UI and save them to a local JSON config.

## ️ Tech Stack

- **Language:** Python 3.9+
- **UI Framework:** CustomTkinter, Tkinter
- **Vision:** MediaPipe, OpenCV
- **AI Integration:** LM Studio (Local Server), Requests
- **Data:** JSON, SQLite (optional)

##  Quick Start

1. **Install LM Studio** and start the local server on port `1234`.
2. **Clone this repository:**
   ```bash
   git clone https://github.com/hjk-inc/pose-ai-processor.git