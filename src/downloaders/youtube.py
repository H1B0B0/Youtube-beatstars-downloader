import os
import re
import time
from pytubefix import YouTube
from PyQt5.QtCore import QThread, pyqtSignal

class YouTubeDownloaderThread(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    info_signal = pyqtSignal(dict)
    
    def __init__(self, url, output_path=None):
        super().__init__()
        self.url = url
        self.output_path = output_path
        
    def extract_video_id(self, url):
        """Extract the YouTube video ID from various URL formats"""
        # Common URL patterns
        patterns = [
            r'(?:v=|v\/|vi=|vi\/|youtu\.be\/|\/v\/|u\/\w\/|embed\/|shorts\/|watch\?v=|\&v=)([^#\&\?\n<>\'\"]+)',
            r'(?:youtu.be\/|youtube.com\/(?:embed\/|v\/|shorts\/|watch\?v=|\&v=))([^#\&\?\n<>\'\"]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
                
        return None
    
    def run(self):
        try:
            # Validate URL
            if not self.url:
                self.error_signal.emit("Please enter a valid YouTube URL")
                return
                
            self.progress_signal.emit(10)
            
            try:
                # Clean up the URL - extract video ID and create clean URL
                print(f"[DEBUG] Original URL: {self.url}")
                video_id = self.extract_video_id(self.url)
                
                if not video_id:
                    raise ValueError("Could not extract video ID from URL")
                    
                clean_url = f"https://www.youtube.com/watch?v={video_id}"
                print(f"[DEBUG] Clean URL with video ID: {clean_url}")
                
                # Initialize YouTube object with pytubefix - use multiple attempts
                try:
                    print("[DEBUG] Initializing pytubefix YouTube object")
                    # First attempt - standard initialization
                    try:
                        yt = YouTube(clean_url)
                        print(f"[DEBUG] Successfully initialized YouTube for video: {yt.title}")
                    except Exception as e1:
                        print(f"[DEBUG] First initialization attempt failed: {str(e1)}")
                        # Second attempt - with use_oauth set to False
                        try:
                            yt = YouTube(clean_url, use_oauth=False, allow_oauth_cache=False)
                            print(f"[DEBUG] Second attempt initialized YouTube for video: {yt.title}")
                        except Exception as e2:
                            print(f"[DEBUG] Second initialization attempt failed: {str(e2)}")
                            # Try an embed URL as last resort
                            embed_url = f"https://www.youtube.com/embed/{video_id}"
                            yt = YouTube(embed_url)
                            print(f"[DEBUG] Embed URL initialization worked for video: {yt.title}")
                except Exception as e:
                    print(f"[ERROR] All initialization attempts failed: {str(e)}")
                    raise
                
                # Setup progress callback
                def progress_callback(stream, chunk, bytes_remaining):
                    try:
                        size = stream.filesize
                        if size > 0:
                            downloaded = size - bytes_remaining
                            percent = int((downloaded / size) * 90) + 10  # 10-100%
                            self.progress_signal.emit(percent)
                    except Exception as e:
                        print(f"[WARNING] Progress callback error: {str(e)}")
                
                # Register callback
                yt.register_on_progress_callback(progress_callback)
                
                # Get video info
                video_info = {
                    "title": yt.title,
                    "author": yt.author,
                    "length": yt.length,
                    "views": yt.views,
                    "thumbnail_url": yt.thumbnail_url,
                    "streams": []
                }
                
                # Get available audio streams - try/catch each stream operation
                try:
                    print("[DEBUG] Getting available streams...")
                    audio_streams = yt.streams.filter(only_audio=True).order_by("abr").desc()
                    
                    # Fallback in case the main stream listing fails
                    if not audio_streams:
                        print("[DEBUG] No audio streams found, trying alternative approach")
                        # Force stream refresh 
                        yt.streams._streams = []
                        yt.streams._fmt_streams = []
                        audio_streams = yt.streams.filter(only_audio=True)
                    
                    for stream in audio_streams:
                        if stream.mime_type.startswith("audio"):
                            video_info["streams"].append({
                                "itag": stream.itag,
                                "abr": stream.abr,
                                "mime_type": stream.mime_type,
                                "type": "audio"
                            })
                except Exception as e:
                    print(f"[DEBUG] Error getting audio streams: {str(e)}")
                    # Continue anyway - we'll try to get a stream for download later
                
                self.progress_signal.emit(20)
                self.info_signal.emit(video_info)
                
                # Get highest quality audio stream
                try:
                    print("[DEBUG] Getting available audio streams for download...")
                    # Main approach
                    audio = None
                    
                    # Try specific itags known to be audio-only (sorted by quality)
                    audio_itags = [251, 140, 250, 249, 139, 171, 18]
                    for itag in audio_itags:
                        try:
                            print(f"[DEBUG] Trying to get stream with itag {itag}")
                            stream = yt.streams.get_by_itag(itag)
                            if stream:
                                audio = stream
                                print(f"[DEBUG] Found stream with itag {itag}")
                                break
                        except Exception as e:
                            print(f"[DEBUG] Couldn't get stream with itag {itag}: {str(e)}")
                    
                    # Fallback approach 1
                    if not audio:
                        try:
                            print("[DEBUG] Trying to get audio through filter(only_audio=True)")
                            audio = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
                            print(f"[DEBUG] Found audio stream through filter: {audio}")
                        except Exception as e:
                            print(f"[DEBUG] Couldn't get stream through filter(only_audio=True): {str(e)}")
                    
                    # Fallback approach 2
                    if not audio:
                        try:
                            print("[DEBUG] Trying to get any progressive stream")
                            audio = yt.streams.filter(progressive=True).order_by('resolution').desc().first()
                            print(f"[DEBUG] Found progressive stream: {audio}")
                        except Exception as e:
                            print(f"[DEBUG] Couldn't get progressive stream: {str(e)}")
                    
                    if not audio:
                        raise Exception("No suitable streams found for this video after multiple attempts")
                        
                    print(f"[DEBUG] Selected audio stream: {audio}")
                    
                    # Download
                    print(f"[DEBUG] Downloading audio stream: {audio}")
                    output_file = audio.download(output_path=self.output_path)
                    
                    # Convert to mp3
                    base, _ = os.path.splitext(output_file)
                    mp3_file = base + ".mp3"
                    os.rename(output_file, mp3_file)
                    
                    self.progress_signal.emit(100)
                    self.finished_signal.emit(mp3_file)
                except Exception as e:
                    print(f"[ERROR] Error during stream download: {str(e)}")
                    self.error_signal.emit(f"Error downloading stream: {str(e)}")
                    return
                
            except Exception as e:
                print(f"[ERROR] YouTube download error: {str(e)}")
                self.error_signal.emit(f"YouTube download error: {str(e)}")
                return
                
        except Exception as e:
            print(f"[ERROR] Unexpected error: {str(e)}")
            self.error_signal.emit(f"Unexpected error: {str(e)}")
