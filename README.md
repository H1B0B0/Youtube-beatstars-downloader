<!-- filepath: c:\Users\menet\Downloads\Youtube-beatstars-downloader\README.md -->

# 🎵 Youtube/Beatstar Downloader 🎶

A modern and sleek desktop application to download music from Beatstars and YouTube.

![Youtube/Beatstar Downloader](https://i.imgur.com/placeholder.png)

## ✨ Features

- **🎧 Beatstars Downloader**: Download beats from Beatstars using an ID or URL
- **📥 YouTube Audio Extractor**: Download audio from YouTube videos in MP3 format
- **🖥️ Modern Interface**: Clean interface, dark theme with intuitive controls
- **🌍 Cross-Platform**: Works on Windows, macOS, and Linux

## 📂 Project Structure

```
├── main.py                   # Application entry point
├── requirements.txt          # Project dependencies
├── LICENSE                   # Project license
├── README.md                 # This file
└── src/                      # Source code
    ├── downloaders/          # Download managers
    │   ├── beatstars.py      # Beatstars downloader
    │   └── youtube.py        # YouTube downloader
    ├── ui/                   # User interface
    │   └── app.py            # Main PyQt5 application
    └── utils/                # Utilities
        └── pytube_fixes.py   # Fixes for pytubefix
```

## 🛠️ Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Setup

1. Clone the repository or download the zip file:

   ```bash
   git clone https://github.com/H1B0B0/emergency-beat
   cd emergency-beat
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## 🚀 Usage

### 🎧 Beatstars Downloader

1. Click on the "Beatstars" tab
2. Enter a Beatstars ID or URL (supported formats):
   - Direct ID: `21098135`
   - Standard URL: `https://www.beatstars.com/beat/21098135`
   - Producer URL: `https://producer.beatstars.com/beat/name-21841482`
3. (Optional) Enter a custom file name
4. Click "Download Beat"

### 📥 YouTube Audio Extractor

1. Click on the "YouTube" tab
2. Paste a YouTube video URL
3. (Optional) Enter a custom file name
4. Click "Download Audio from YouTube"
5. The audio will be extracted and saved in MP3 format

## 📦 Dependencies

- **PyQt5 (v5.15.10)**: GUI framework
- **pytubefix (v5.1.3)**: Library for YouTube content extraction
- **requests (v2.32.3)**: Library for HTTP requests

## ⚠️ Limitations

- The Beatstars API may change over time, potentially affecting functionality
- Only MP3 format is currently supported for Beatstars downloads
- Some Beatstars beats may be protected from downloading
- YouTube videos with copyright restrictions may not be downloadable

## 🛠️ Troubleshooting Common Issues

- If you encounter errors with YouTube, ensure `pytubefix` is properly installed and up to date
- For initialization issues, the `pytube_fixes.py` module applies fixes to bypass YouTube API changes
- If certain beats cannot be downloaded from Beatstars, they may be protected or require authentication

## ⚖️ Legal Disclaimer

This tool is intended for personal use only. Please respect copyright laws and only download content you have the right to access. The developers are not responsible for any misuse of this application.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

Created by HIBOBO - 2025

## 🙏 Acknowledgments

- Built with PyQt5 for the user interface
- Uses pytubefix for YouTube integration
- Uses requests for API communication

---

**Note**: This application is provided as-is without any warranty. Use it at your own risk.
