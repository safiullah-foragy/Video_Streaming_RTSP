# Video Streaming with RTSP and RTP

A comprehensive **Python-based video streaming system** implementing RTSP (Real-Time Streaming Protocol) for session control and RTP (Real-Time Transport Protocol) for real-time video transmission. Features a modern **YouTube-like GUI** built with Tkinter.

## 🎯 Features

- **RTSP Protocol Implementation**: Full support for SETUP, PLAY, PAUSE, and TEARDOWN commands
- **RTP Video Streaming**: Real-time video frame transmission over UDP
- **Modern YouTube-like Interface**: Intuitive GUI with playback controls
- **Real-time Statistics**: Display of FPS, bitrate, and frame count
- **Multi-threaded Architecture**: Separate threads for video streaming and GUI
- **Frame-by-frame Streaming**: Server provides video frames one at a time via RTP packets

## 📋 Requirements

- Python 3.7 or higher
- OpenCV (cv2)
- Pillow (PIL)
- NumPy
- Tkinter (usually included with Python)

## 🚀 Installation

1. **Clone or download this repository**

2. **Install required packages:**
```bash
pip install -r requirements.txt
```

3. **Prepare a video file:**

You have two options:

**Option A: Create a test video**
```bash
python VideoConverter.py --test
```
This creates a 10-second test video called `movie.Mjpeg` with animated content.

**Option B: Convert your own video**
```bash
python VideoConverter.py your_video.mp4
```
This converts your video to the MJPEG format required for streaming.

## 🎬 Usage

### Step 1: Start the RTSP Server

Open a terminal/command prompt and run:
```bash
python Server.py
```

You should see:
```
[SERVER] Starting RTSP server on 127.0.0.1:8554
[SERVER] RTSP server ready. Waiting for connections...
```

### Step 2: Start the Client

Open another terminal/command prompt and run:
```bash
python Client.py
```

This will launch the YouTube-like GUI client.

### Step 3: Stream Video

In the client GUI:
1. Click **"⚙ SETUP"** to establish connection with the server
2. Click **"▶ PLAY"** to start streaming video
3. Click **"⏸ PAUSE"** to pause the stream
4. Click **"⏹ STOP"** to disconnect and close

## 🎨 GUI Features

The client features a modern, dark-themed interface similar to YouTube:

- **Video Display Area**: Shows the streaming video (640x480)
- **Progress Bar**: Visual indicator of playback
- **Control Buttons**:
  - ⚙ SETUP: Initialize connection
  - ▶ PLAY: Start streaming
  - ⏸ PAUSE: Pause streaming
  - ⏹ STOP: Stop and disconnect
- **Status Bar**: Shows connection status, frame count, bitrate, and FPS

## 📁 Project Structure

```
Video_Streaming_RTSP/
│
├── Server.py              # RTSP server main entry point
├── ServerWorker.py        # Handles individual client connections
├── Client.py              # RTSP client with YouTube-like GUI
├── RtpPacket.py          # RTP packet encoding/decoding
├── VideoStream.py        # Video file handling
├── VideoConverter.py     # Utility to convert videos to MJPEG
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── movie.Mjpeg          # Sample video file (MJPEG format)
└── README.md            # This file
```

## ⚙️ Configuration

Edit `config.py` to customize settings:

```python
SERVER_HOST = '127.0.0.1'    # Server IP address
RTSP_PORT = 8554             # RTSP control port
RTP_PORT = 25000             # RTP data port
VIDEO_FILE = 'movie.Mjpeg'   # Video file name
FRAME_RATE = 24              # Streaming frame rate
```

## 🔧 Advanced Usage

### Custom Server/Port

Run client with custom parameters:
```bash
python Client.py <server_ip> <rtsp_port> <rtp_port> <video_file>
```

Example:
```bash
python Client.py 192.168.1.100 8554 25000 movie.Mjpeg
```

### Multiple Clients

The server supports multiple simultaneous clients. Simply run additional client instances:
```bash
python Client.py
```

**Note**: Each client should use a different RTP port. Modify in code or pass as argument.

## 🛠️ How It Works

### RTSP Session Control

1. **SETUP**: Client requests to setup a session, server allocates resources
2. **PLAY**: Client requests to start streaming, server begins sending RTP packets
3. **PAUSE**: Client requests to pause, server stops sending packets
4. **TEARDOWN**: Client disconnects, server releases resources

### RTP Video Streaming

1. Server reads video frames from MJPEG file
2. Each frame is encapsulated in an RTP packet
3. RTP packets are sent via UDP to the client
4. Client receives packets, extracts frames, and displays them
5. Frame rate controlled to maintain smooth playback

### Protocol Flow

```
Client                          Server
  |                               |
  |-- SETUP request ----------->  |
  |<--------- 200 OK -------------|
  |                               |
  |-- PLAY request ------------->  |
  |<--------- 200 OK -------------|
  |                               |
  |<======= RTP packets =========|
  |<======= RTP packets =========|
  |                               |
  |-- PAUSE request ------------>  |
  |<--------- 200 OK -------------|
  |                               |
  |-- TEARDOWN request --------->  |
  |<--------- 200 OK -------------|
```

## 📊 Statistics

The client displays real-time statistics:

- **Frame Count**: Total frames received
- **Bitrate**: Data rate in kbps
- **FPS**: Actual frames per second
- **Status**: Current connection state

## 🐛 Troubleshooting

### Port Already in Use
```
Error: [Errno 10048] Address already in use
```
**Solution**: Close other instances or change ports in `config.py`

### Video File Not Found
```
Error: Could not open video file
```
**Solution**: Ensure `movie.Mjpeg` exists or run `VideoConverter.py --test`

### Connection Refused
```
Connection Error: Failed to connect to server
```
**Solution**: Ensure the server is running before starting the client

### Firewall Issues
If clients can't connect, check firewall settings for ports 8554 and 25000.

## 🎓 Learning Outcomes

This project demonstrates:

- **Network Protocols**: RTSP and RTP implementation
- **Socket Programming**: TCP for control, UDP for data
- **Multi-threading**: Concurrent client handling
- **Multimedia Streaming**: Real-time video transmission
- **GUI Development**: Modern interface with Tkinter
- **Client-Server Architecture**: Scalable streaming system

## 📝 Protocol Details

### RTSP Methods Implemented

- **SETUP**: Initialize session and allocate resources
- **PLAY**: Start media transmission
- **PAUSE**: Temporarily halt transmission
- **TEARDOWN**: End session and free resources

### RTP Packet Structure

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|V=2|P|X|  CC   |M|     PT      |       Sequence Number         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                           Timestamp                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             SSRC                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                         Payload (JPEG)                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

## 🚀 Future Enhancements

Potential improvements:

- **Adaptive Streaming**: Adjust quality based on network conditions
- **Video Seeking**: Allow jumping to specific timestamps
- **Multiple Video Sources**: Support for different video files
- **Authentication**: Secure access control
- **Recording**: Save received streams to disk
- **Full-screen Mode**: Enhanced viewing experience
- **Playlist Support**: Queue multiple videos

## 📄 License

This project is created for educational purposes as part of a Computer Networks lab assignment.

## 👨‍💻 Author

Created as a comprehensive implementation of RTSP/RTP video streaming protocols with a modern user interface.

## 🙏 Acknowledgments

- RTSP/RTP Protocol specifications (RFC 2326, RFC 3550)
- OpenCV for video processing
- Python community for excellent libraries

---

**Enjoy streaming!** 🎬📺
