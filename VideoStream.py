"""
Video Stream Class
Handles video file operations and frame extraction for streaming
"""

import sys


class VideoStream:
    """Class to handle video file operations"""
    
    def __init__(self, filename):
        """Initialize video stream with a filename"""
        self.filename = filename
        try:
            self.file = open(filename, 'rb')
        except:
            raise IOError(f"Could not open video file: {filename}")
        
        self.frameNum = 0
    
    def nextFrame(self):
        """Get the next frame from the video file"""
        try:
            data = self.file.read(5)  # Get the frame length from the first 5 bytes
            if data:
                framelength = int(data)
                
                # Read the current frame
                frame_data = self.file.read(framelength)
                self.frameNum += 1
                return frame_data
            else:
                return None
        except:
            return None
    
    def frameNbr(self):
        """Return current frame number"""
        return self.frameNum
    
    def reset(self):
        """Reset to beginning of file"""
        self.file.seek(0)
        self.frameNum = 0
    
    def close(self):
        """Close the video file"""
        self.file.close()
