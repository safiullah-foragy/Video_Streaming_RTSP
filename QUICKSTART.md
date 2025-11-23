# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

Open a terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

### Step 2: Create a Test Video

Generate a sample video for testing:

```bash
python VideoConverter.py --test
```

This creates a 10-second animated test video called `movie.Mjpeg`.

### Step 3: Run the Application

**Windows:**
- Double-click `start_server.bat` to start the server
- Double-click `start_client.bat` (in a new terminal) to start the client

**Linux/Mac:**
```bash
chmod +x start_server.sh start_client.sh
./start_server.sh    # Terminal 1
./start_client.sh    # Terminal 2
```

**Manual Start:**
```bash
# Terminal 1 - Server
python Server.py

# Terminal 2 - Client
python Client.py
```

## 🎮 Using the Client

1. **Click "⚙ SETUP"** - Connects to the server
2. **Click "▶ PLAY"** - Starts video streaming
3. **Click "⏸ PAUSE"** - Pauses the video
4. **Click "⏹ STOP"** - Stops and disconnects

## 🎥 Using Your Own Video

Convert any video file to the required format:

```bash
python VideoConverter.py myvideo.mp4
```

This will create `movie.Mjpeg` from your video file.

## 🔧 Troubleshooting

### Server won't start
- Check if port 8554 is already in use
- Try closing other instances or change the port in `config.py`

### Client can't connect
- Make sure the server is running first
- Check firewall settings for ports 8554 and 25000

### Video not displaying
- Ensure `movie.Mjpeg` exists in the project directory
- Try creating a test video with `python VideoConverter.py --test`

## 📝 Default Configuration

- **Server Address:** 127.0.0.1 (localhost)
- **RTSP Port:** 8554 (TCP)
- **RTP Port:** 25000 (UDP)
- **Video File:** movie.Mjpeg
- **Frame Rate:** 24 FPS

Change these in `config.py` if needed.

## 🌐 Network Streaming

To stream over a network:

1. **On the server computer**, edit `config.py`:
   ```python
   SERVER_HOST = '0.0.0.0'  # Listen on all interfaces
   ```

2. **Start the server:**
   ```bash
   python Server.py
   ```

3. **On the client computer**, run:
   ```bash
   python Client.py <server_ip> 8554 25000 movie.Mjpeg
   ```
   Replace `<server_ip>` with the server's IP address.

## 📚 More Information

See `README.md` for complete documentation, protocol details, and advanced usage.

---

**Need help?** Check the full README.md for detailed information about the project architecture and protocols.
