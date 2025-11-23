"""
Configuration file for Video Streaming System
"""

# Server Configuration
SERVER_HOST = '127.0.0.1'
RTSP_PORT = 8554
RTP_PORT = 25000

# Video Configuration
VIDEO_FILE = 'movie.Mjpeg'
FRAME_RATE = 24  # frames per second
MAX_PACKET_SIZE = 20480  # Maximum RTP packet size

# RTSP Methods
RTSP_VER = 'RTSP/1.0'
SETUP = 'SETUP'
PLAY = 'PLAY'
PAUSE = 'PAUSE'
TEARDOWN = 'TEARDOWN'

# RTSP Response Codes
OK = 200
NOT_FOUND = 404
INTERNAL_ERROR = 500

# Session States
INIT = 0
READY = 1
PLAYING = 2
