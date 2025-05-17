"""
Emergency Beat Downloader
Main application entry point
"""
import sys
import os
import ssl
from PyQt5.QtWidgets import QApplication

# Add the parent directory to path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from src.utils.pytube_fixes import apply_pytube_fix
from src.ui.app import EmergencyBeatApp

# Configure SSL
ssl._create_default_https_context = ssl._create_unverified_context

if __name__ == "__main__":
    # Apply the Pytube fixes before using the library
    apply_pytube_fix()
    
    app = QApplication(sys.argv)
    window = EmergencyBeatApp()
    window.show()
    sys.exit(app.exec_())
