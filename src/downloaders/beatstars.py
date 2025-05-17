import os
import requests
import urllib.request
import time
from PyQt5.QtCore import QThread, pyqtSignal

class DownloaderThread(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    
    def __init__(self, song_id, name):
        super().__init__()
        # Extract ID from URL if needed
        self.song_id = self.extract_id(song_id)
        self.name = name
        self.format_type = "mp3"  # MP3 is the only available format
    
    def extract_id(self, input_text):
        # Check if input is a full beatstars URL
        if "beatstars.com/beat/" in input_text:
            try:
                # Extract the ID from the URL (last part of the URL which is a number)
                parts = input_text.split("/")
                # Get the last part and extract numeric ID
                last_part = parts[-1]
                # If it's a number, return it directly
                if last_part.isdigit():
                    return last_part
                
                # Otherwise, try to find the ID in the URL (formats like producer.beatstars.com/beat/name-12345678)
                for part in parts:
                    # Look for parts that contain a dash with numbers after it (beat-name-12345678)
                    if "-" in part:
                        # Try to get the digits after the last dash
                        possible_id = part.split("-")[-1]
                        if possible_id.isdigit():
                            return possible_id
            except:
                return input_text
        return input_text
        
    def resolve(self, url):
        # Create a custom opener with headers that simulate a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.beatstars.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        
        req = urllib.request.Request(url, headers=headers)
        return urllib.request.urlopen(req).geturl()
        
    def run(self):
        try:
            # Validate song_id
            if not self.song_id:
                self.error_signal.emit("Please enter a valid Beat ID")
                return
            
            # Set filename
            if not self.name:
                self.name = f"beat.{self.format_type}"
            elif not self.name.lower().endswith(f'.{self.format_type}'):
                self.name = f"{self.name}.{self.format_type}"
            
            # Debug information    
            print(f"[DEBUG] Extracted beat ID: {self.song_id}")
            print(f"[DEBUG] Output filename: {self.name}")
            print(f"[DEBUG] Format type: {self.format_type}")
            
            # It seems the API has changed, use 'audio' instead of specific format type
            # This will make the server determine the appropriate format
            song_url = f"https://main.v2.beatstars.com/stream?id={self.song_id}&return=audio"
            print(f"[DEBUG] Requesting URL: {song_url}")
            
            # Progress simulation - connection
            self.progress_signal.emit(10)
            time.sleep(0.2)
            
            # Define browser-like headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': 'audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.beatstars.com/',
                'Origin': 'https://www.beatstars.com',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
            }
            
            # Get real URL
            try:
                print(f"[DEBUG] Attempting to resolve URL...")
                real_url = self.resolve(song_url)
                print(f"[DEBUG] Resolved URL: {real_url}")
                self.progress_signal.emit(30)
            except Exception as e:
                print(f"[ERROR] Failed to resolve URL: {str(e)}")
                self.error_signal.emit(f"Error resolving URL: {str(e)}")
                return
                
            # Download the file
            try:
                print(f"[DEBUG] Sending GET request with headers:")
                for key, value in headers.items():
                    print(f"[DEBUG] Header - {key}: {value}")
                    
                print(f"[DEBUG] Downloading from: {real_url}")
                r = requests.get(real_url, stream=True, headers=headers)
                print(f"[DEBUG] Response status code: {r.status_code}")
                
                if r.status_code != 200:
                    print(f"[ERROR] Bad response: HTTP {r.status_code}")
                    print(f"[ERROR] Response headers: {dict(r.headers)}")
                    print(f"[ERROR] Response content: {r.text[:500]}")  # Print first 500 chars of response
                    self.error_signal.emit(f"Error: Received status code {r.status_code}. The beat may be protected or not available for download.")
                    return
                    
                self.progress_signal.emit(50)
                
                # Save the file
                total_size = int(r.headers.get('content-length', 0))
                block_size = 1024
                downloaded = 0
                
                with open(self.name, 'wb') as f:
                    for data in r.iter_content(block_size):
                        f.write(data)
                        downloaded += len(data)
                        if total_size > 0:
                            progress = int(70 + 30 * (downloaded / total_size))
                            self.progress_signal.emit(min(progress, 100))
                
                self.progress_signal.emit(100)
                self.finished_signal.emit(os.path.abspath(self.name))
                
            except Exception as e:
                self.error_signal.emit(f"Error downloading file: {str(e)}")
                return
                
        except Exception as e:
            self.error_signal.emit(f"Unexpected error: {str(e)}")
