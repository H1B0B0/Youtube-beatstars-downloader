import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QFileDialog, QProgressBar, QMessageBox, QFrame,
                            QGraphicsDropShadowEffect, QComboBox, QRadioButton,
                            QButtonGroup, QTabWidget)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QColor, QDesktopServices

class EmergencyBeatApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Emergency Beat Downloader")
        self.setMinimumSize(600, 400)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                            stop:0 #16171d, stop:1 #282a36);
            }
            QLabel {
                color: #f8f8f2;
                font-size: 14px;
            }
            QLineEdit {
                padding: 12px;
                border-radius: 6px;
                background-color: rgba(255, 255, 255, 0.07);
                color: #FFFFFF;
                border: 1px solid rgba(255, 255, 255, 0.1);
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #64B5F6;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                            stop:0 #42A5F5, stop:1 #2196F3);
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                padding: 12px 15px;
                font-size: 15px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                            stop:0 #64B5F6, stop:1 #42A5F5);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                            stop:0 #1E88E5, stop:1 #1976D2);
            }
            QProgressBar {
                border: none;
                border-radius: 6px;
                text-align: center;
                background-color: rgba(255, 255, 255, 0.07);
                color: white;
                height: 12px;
                font-size: 12px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                            stop:0 #42A5F5, stop:1 #2196F3);
                border-radius: 6px;
            }
            QComboBox {
                padding: 10px;
                border-radius: 6px;
                background-color: rgba(255, 255, 255, 0.07);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.1);
                font-size: 14px;
                min-width: 100px;
            }
            QComboBox:on {
                border: 1px solid #64B5F6;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox QAbstractItemView {
                background-color: #212121;
                color: white;
                selection-background-color: #2196F3;
                selection-color: white;
                border: 1px solid #424242;
                border-radius: 4px;
            }
            QRadioButton {
                color: white;
                font-size: 14px;
                spacing: 8px;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
            }
            QRadioButton::indicator:checked {
                background-color: #2196F3;
                border: 2px solid #BBDEFB;
                border-radius: 10px;
            }
            QRadioButton::indicator:unchecked {
                background-color: rgba(255, 255, 255, 0.07);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
            }
        """)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Emergency Music Downloader")
        title_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #2196F3; letter-spacing: 1px; margin-bottom: 5px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Download beats from Beatstars and audio from YouTube")
        subtitle_label.setStyleSheet("font-size: 16px; color: #BBDEFB;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: rgba(255, 255, 255, 0.1); height: 1px;")
        main_layout.addWidget(separator)
        
        # Create tab widget
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 6px;
                background-color: rgba(33, 33, 33, 0.85);
                padding: 10px;
            }
            QTabBar::tab {
                background-color: rgba(30, 30, 30, 0.7);
                color: #aaaaaa;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                padding: 8px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: rgba(33, 33, 33, 0.95);
                color: #ffffff;
                border-bottom: 2px solid #2196F3;
            }
            QTabBar::tab:hover:!selected {
                background-color: rgba(40, 40, 40, 0.7);
                color: #ffffff;
            }
        """)
        
        # Create Beatstars Tab
        beats_tab = QWidget()
        beats_layout = QVBoxLayout(beats_tab)
        beats_layout.setContentsMargins(20, 20, 20, 20)
        beats_layout.setSpacing(15)
        
        # Beat ID input
        id_layout = QVBoxLayout()
        id_label = QLabel("Beat ID or URL:")
        id_layout.addWidget(id_label)
        
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter Beatstars ID or any Beatstars URL")
        id_layout.addWidget(self.id_input)
        beats_layout.addLayout(id_layout)
        
        # Name input
        name_layout = QVBoxLayout()
        name_label = QLabel("Filename (optional):")
        name_layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter the output filename (without .mp3)")
        name_layout.addWidget(self.name_input)
        beats_layout.addLayout(name_layout)
        
        # Progress bar
        self.progress_bar_beats = QProgressBar()
        self.progress_bar_beats.setValue(0)
        self.progress_bar_beats.setTextVisible(True)
        self.progress_bar_beats.setFormat("%p%")
        beats_layout.addWidget(self.progress_bar_beats)
        
        # Download button
        self.download_button_beats = QPushButton("Download Beat")
        self.download_button_beats.setMinimumHeight(50)
        self.download_button_beats.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #ff5555, stop:1 #ff8080);
            color: white;
            font-weight: bold;
            font-size: 16px;
            border: none;
            border-radius: 8px;
        """)
        # Add drop shadow effect
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(8)
        shadow_effect.setColor(QColor(0, 0, 0, 100))
        shadow_effect.setOffset(0, 4)
        self.download_button_beats.setGraphicsEffect(shadow_effect)
        
        self.download_button_beats.clicked.connect(self.start_beats_download)
        beats_layout.addWidget(self.download_button_beats)
        
        # Create YouTube Tab
        yt_tab = QWidget()
        yt_layout = QVBoxLayout(yt_tab)
        yt_layout.setContentsMargins(20, 20, 20, 20)
        yt_layout.setSpacing(15)
        
        # YouTube URL input
        yt_url_layout = QVBoxLayout()
        yt_url_label = QLabel("YouTube URL:")
        yt_url_layout.addWidget(yt_url_label)
        
        self.yt_url_input = QLineEdit()
        self.yt_url_input.setPlaceholderText("Enter YouTube video URL")
        yt_url_layout.addWidget(self.yt_url_input)
        yt_layout.addLayout(yt_url_layout)
        
        # Output name input
        yt_name_layout = QVBoxLayout()
        yt_name_label = QLabel("Filename (optional):")
        yt_name_layout.addWidget(yt_name_label)
        
        self.yt_name_input = QLineEdit()
        self.yt_name_input.setPlaceholderText("Enter the output filename (without .mp3)")
        yt_name_layout.addWidget(self.yt_name_input)
        yt_layout.addLayout(yt_name_layout)
        
        # Progress bar for YouTube
        self.progress_bar_yt = QProgressBar()
        self.progress_bar_yt.setValue(0)
        self.progress_bar_yt.setTextVisible(True)
        self.progress_bar_yt.setFormat("%p%")
        yt_layout.addWidget(self.progress_bar_yt)
        
        # YouTube video info display
        self.yt_info_label = QLabel("Video details will appear here")
        self.yt_info_label.setStyleSheet("""
            color: #bbbbbb;
            background-color: rgba(20, 20, 20, 0.5);
            border-radius: 5px;
            padding: 10px;
            min-height: 50px;
        """)
        self.yt_info_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.yt_info_label.setWordWrap(True)
        yt_layout.addWidget(self.yt_info_label)
        
        # Download button for YouTube
        self.download_button_yt = QPushButton("Download Audio from YouTube")
        self.download_button_yt.setMinimumHeight(50)
        self.download_button_yt.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                        stop:0 #F44336, stop:1 #FF5252);
            color: white;
            font-weight: bold;
            font-size: 16px;
            border: none;
            border-radius: 8px;
        """)
        # Add drop shadow effect
        yt_shadow_effect = QGraphicsDropShadowEffect()
        yt_shadow_effect.setBlurRadius(8)
        yt_shadow_effect.setColor(QColor(0, 0, 0, 100))
        yt_shadow_effect.setOffset(0, 4)
        self.download_button_yt.setGraphicsEffect(yt_shadow_effect)
        
        self.download_button_yt.clicked.connect(self.start_youtube_download)
        yt_layout.addWidget(self.download_button_yt)
        
        # Add tabs to tab widget
        tab_widget.addTab(beats_tab, "Beatstars")
        tab_widget.addTab(yt_tab, "YouTube")
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 8)
        tab_widget.setGraphicsEffect(shadow)
        
        main_layout.addWidget(tab_widget)
        
        # Footer
        footer_label = QLabel("Emergency Music Downloader by HIBOBO - 2025")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("color: rgba(255, 255, 255, 0.4); font-size: 12px;")
        main_layout.addWidget(footer_label)
    
    def browse_location(self, for_youtube=False):
        if for_youtube:
            name_input = self.yt_name_input
        else:
            name_input = self.name_input
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Audio As",
            os.path.join(os.getcwd(), name_input.text() or "audio.mp3"),
            "MP3 Files (*.mp3)"
        )
        
        if file_path:
            # Extract just the filename without path and extension
            filename = os.path.basename(file_path)
            if filename.endswith('.mp3'):
                filename = filename[:-4]  # Remove .mp3 extension
            name_input.setText(filename)
    
    def start_beats_download(self):
        from src.downloaders.beatstars import DownloaderThread
        
        song_id = self.id_input.text().strip()
        name = self.name_input.text().strip()
        
        # Validate input
        if not song_id:
            self.show_error("Please enter a Beat ID or Beatstars URL")
            return
        
        # Disable UI during download
        self.download_button_beats.setEnabled(False)
        self.download_button_beats.setText("Downloading...")
        
        # Create and start the downloader thread
        self.downloader = DownloaderThread(song_id, name)
        self.downloader.progress_signal.connect(self.update_beats_progress)
        self.downloader.finished_signal.connect(self.download_finished)
        self.downloader.error_signal.connect(self.show_error)
        self.downloader.start()
    
    def start_youtube_download(self):
        from src.downloaders.youtube import YouTubeDownloaderThread
        
        url = self.yt_url_input.text().strip()
        output_path = os.getcwd()  # Current directory
        
        # Validate input
        if not url:
            self.show_error("Please enter a YouTube URL")
            return
            
        # Verify it's a valid YouTube URL
        import re
        youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        if not re.match(youtube_regex, url):
            self.show_error("Invalid YouTube URL. Please enter a valid YouTube video URL.")
            return
        
        # Disable UI during download
        self.download_button_yt.setEnabled(False)
        self.download_button_yt.setText("Downloading...")
        
        # Create and start the YouTube downloader thread
        self.yt_downloader = YouTubeDownloaderThread(url, output_path)
        self.yt_downloader.progress_signal.connect(self.update_youtube_progress)
        self.yt_downloader.finished_signal.connect(self.youtube_download_finished)
        self.yt_downloader.error_signal.connect(self.show_error)
        self.yt_downloader.info_signal.connect(self.update_youtube_info)
        self.yt_downloader.start()
    
    def update_beats_progress(self, value):
        self.progress_bar_beats.setValue(value)
        
    def update_youtube_progress(self, value):
        self.progress_bar_yt.setValue(value)
    
    def update_youtube_info(self, info):
        # Format video info
        duration_min = info["length"] // 60
        duration_sec = info["length"] % 60
        
        info_text = (
            f"<b>Title:</b> {info['title']}<br>"
            f"<b>Channel:</b> {info['author']}<br>"
            f"<b>Duration:</b> {duration_min}:{duration_sec:02d}<br>"
            f"<b>Views:</b> {info['views']:,}"
        )
        
        self.yt_info_label.setText(info_text)
        
    def youtube_download_finished(self, file_path):
        # Rename file if needed
        custom_name = self.yt_name_input.text().strip()
        if custom_name:
            directory = os.path.dirname(file_path)
            new_file_path = os.path.join(directory, f"{custom_name}.mp3")
            
            try:
                os.rename(file_path, new_file_path)
                file_path = new_file_path
            except Exception as e:
                print(f"[WARNING] Failed to rename file: {str(e)}")
        
        self.progress_bar_yt.setValue(100)
        self.download_button_yt.setEnabled(True)
        self.download_button_yt.setText("Download Audio from YouTube")
        
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Download Complete")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(f"Your audio has been successfully downloaded to:\n{file_path}")
        
        open_folder_button = msg_box.addButton("Open Folder", QMessageBox.ActionRole)
        msg_box.addButton(QMessageBox.Ok)
        
        msg_box.exec_()
        
        if msg_box.clickedButton() == open_folder_button:
            QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(file_path)))
    
    def download_finished(self, file_path):
        self.progress_bar_beats.setValue(100)
        self.download_button_beats.setEnabled(True)
        self.download_button_beats.setText("Download Beat")
        
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Download Complete")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(f"Your beat has been successfully downloaded to:\n{file_path}")
        
        open_folder_button = msg_box.addButton("Open Folder", QMessageBox.ActionRole)
        msg_box.addButton(QMessageBox.Ok)
        
        msg_box.exec_()
        
        if msg_box.clickedButton() == open_folder_button:
            QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(file_path)))
    
    def show_error(self, error_message):
        # Reset both progress bars
        self.progress_bar_beats.setValue(0)
        self.progress_bar_yt.setValue(0)
        
        # Reset both buttons
        self.download_button_beats.setEnabled(True)
        self.download_button_beats.setText("Download Beat")
        
        self.download_button_yt.setEnabled(True)
        self.download_button_yt.setText("Download Audio from YouTube")
        
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(error_message)
        
        if "403" in error_message:
            # Additional info for 403 errors
            msg_box.setInformativeText(
                "Access denied by Beatstars. This could happen because:\n"
                "1. The beat is protected against downloads\n"
                "2. Beatstars has changed their API\n"
                "3. The beat requires purchase before download"
            )
        elif "400" in error_message or "Unknown API" in error_message:
            # Additional info for 400 errors
            msg_box.setInformativeText(
                "Bad request to Beatstars API. This could happen because:\n"
                "1. The beat ID is incorrect\n"
                "2. Beatstars has changed their API\n"
                "3. The beat is no longer available"
            )
            
        # Style the error message box with dark theme and better contrast
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #1e1e2e;
                color: white;
            }
            QLabel {
                color: #ff6b6b;
                font-size: 14px;
                background-color: transparent;
            }
            QLabel#qt_msgbox_informativelabel {
                color: #f8f8f2;
                font-size: 13px;
            }
            QPushButton {
                background-color: #ff5555;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 13px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #ff6e6e;
            }
        """)
        msg_box.exec_()
