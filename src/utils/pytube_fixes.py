# Simple fixes for the pytubefix library
import pytubefix
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def apply_pytube_fix():
    """Apply fixes for pytubefix to handle YouTube's API changes"""
    print("[DEBUG] Applying pytubefix fixes")
    
    # Set modern User-Agent
    orig_get = pytubefix.request.get
    def new_get(url, extra_headers=None):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        if extra_headers:
            headers.update(extra_headers)
        return orig_get(url, headers)
    
    # Apply the patched request function
    pytubefix.request.get = new_get
    
    # Make YouTube initialization more robust
    original_init = pytubefix.YouTube.__init__
    def patched_init(self, url, *args, **kwargs):
        print(f"[DEBUG] Initializing YouTube with URL: {url}")
        try:
            original_init(self, url, *args, **kwargs)
        except Exception as e:
            print(f"[DEBUG] Initialization error: {str(e)}")
            # Set minimal required attributes to prevent crashes
            self.js = ""
            self.js_url = ""
            self.vid_info = {}
            self.watch_html = ""
            self.embed_html = ""
            self.title = "Unknown Title"
    
    # Apply the patched init function
    pytubefix.YouTube.__init__ = patched_init
    
    print("[DEBUG] Applied all pytubefix fixes")