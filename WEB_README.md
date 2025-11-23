# 🌐 Web-Based Video Streaming Server

A modern, YouTube-like web interface for streaming videos over HTTP. Simply place your videos in the `assets/videos` folder and access them from any web browser!

## ✨ Features

- 🎬 **YouTube-Style Interface** - Modern, dark-themed web UI
- 📁 **Simple Video Management** - Just drop videos in a folder
- 🌐 **Browser-Based** - Access from anywhere on your network
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- ⚡ **Fast Streaming** - HTTP range requests for seeking support
- 🎯 **Multiple Formats** - Supports MP4, AVI, MOV, MKV, WebM, and more
- 🔍 **Video Library** - Browse all your videos in one place
- ⌨️ **Keyboard Shortcuts** - Full keyboard control for video playback

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install Flask opencv-python Pillow numpy
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

### 2. Add Your Videos

Place video files in the `assets/videos` folder:
```
Video_Streaming_RTSP/
└── assets/
    └── videos/
        ├── your_video1.mp4
        ├── your_video2.avi
        └── your_video3.mov
```

**Supported formats**: MP4, AVI, MOV, MKV, WebM, FLV, WMV, M4V

### 3. Start the Server

```bash
python web_server.py
```

Or double-click: `start_web_server.bat` (Windows)

### 4. Open in Browser

Navigate to: **http://localhost:5000**

You'll see your video library with all available videos!

## 🎮 Using the Web Interface

### Home Page
- Browse all videos in a grid layout
- Click any video to start watching
- See video file size and format

### Video Player
- Click video or press `Space` to play/pause
- Press `F` for fullscreen
- Use `Arrow Left/Right` to seek ±5 seconds
- Use `Arrow Up/Down` to adjust volume
- Press `M` to mute/unmute
- Video automatically plays when page loads

## 🌐 Network Access

### Access from Other Devices

The server runs on `0.0.0.0:5000`, making it accessible from any device on your network.

**To access from another device:**

1. Find your computer's IP address:
   ```bash
   # Windows
   ipconfig
   
   # Linux/Mac
   ifconfig
   ```

2. On another device, open browser and go to:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```

   Example: `http://192.168.1.100:5000`

## 📊 API Endpoints

The server provides a REST API:

### GET `/api/videos`
Get list of all available videos
```json
{
    "success": true,
    "count": 3,
    "videos": [
        {
            "filename": "video.mp4",
            "name": "video",
            "size": 15728640,
            "size_mb": 15.0,
            "extension": "MP4"
        }
    ]
}
```

### GET `/api/video/<filename>`
Stream video with range request support
- Supports HTTP range requests for seeking
- Automatic format detection
- Efficient chunk-based streaming

### GET `/watch/<filename>`
Video player page for a specific video

## 🎨 Features Explained

### Video Library Page
- **Grid Layout** - Videos displayed in responsive grid
- **Video Cards** - Shows title, format, and file size
- **Color Gradients** - Each video gets a unique gradient thumbnail
- **Auto-count** - Shows total number of videos
- **Empty State** - Helpful message when no videos found

### Video Player Page
- **HTML5 Video Player** - Native browser video controls
- **Video Info** - Display format, size, duration, resolution
- **Keyboard Shortcuts** - Full keyboard control
- **Responsive** - Adapts to any screen size
- **Auto-play** - Starts playing automatically

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` or `K` | Play/Pause |
| `F` | Toggle Fullscreen |
| `M` | Mute/Unmute |
| `←` | Rewind 5 seconds |
| `→` | Forward 5 seconds |
| `↑` | Volume up |
| `↓` | Volume down |

## 🔧 Configuration

Edit `web_server.py` to customize:

```python
# Port number
app.run(host='0.0.0.0', port=5000)

# Videos folder location
VIDEOS_FOLDER = 'assets/videos'

# Streaming chunk size
CHUNK_SIZE = 1024 * 1024  # 1MB
```

## 📁 Project Structure

```
Video_Streaming_RTSP/
│
├── web_server.py           # Flask web server
│
├── assets/
│   └── videos/            # Place your videos here
│
├── static/
│   ├── css/
│   │   └── style.css      # Styles (YouTube-like theme)
│   └── js/
│       ├── main.js        # Library page functionality
│       └── player.js      # Video player controls
│
├── templates/
│   ├── index.html         # Home page (video library)
│   ├── player.html        # Video player page
│   └── 404.html           # Error page
│
└── requirements.txt       # Python dependencies
```

## 🎯 Use Cases

### Personal Media Server
- Stream your personal video collection
- Access from any device on your network
- No need to copy files to different devices

### Local Network Streaming
- Share videos with family/friends on same network
- Great for home theater setups
- No internet required

### Development/Testing
- Test video streaming implementations
- Prototype video-based applications
- Learn web development with real streaming

## 🛠️ Technical Details

### Technology Stack
- **Backend**: Flask (Python web framework)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla JS)
- **Video**: HTML5 Video API with range requests
- **Styling**: Modern CSS with dark theme

### Streaming Method
- **Protocol**: HTTP with range request support
- **Chunking**: 1MB chunks for efficient streaming
- **Seeking**: Full support via range headers
- **Format**: Direct video file streaming (no transcoding)

### Browser Compatibility
- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Opera
- ⚠️ Internet Explorer (limited support)

## 🔍 Troubleshooting

### Port Already in Use
```
Error: Address already in use
```
**Solution**: Change port in `web_server.py` or stop other servers on port 5000

### Video Won't Play
**Possible causes**:
1. Browser doesn't support video format - Try MP4 or WebM
2. Video codec not supported - Use H.264 for best compatibility
3. File is corrupted - Try a different video

**Solution**: Convert video to MP4 with H.264 codec:
```bash
ffmpeg -i input.avi -c:v libx264 -c:a aac output.mp4
```

### Can't Access from Other Devices
**Checklist**:
1. Server is running on `0.0.0.0` (not `127.0.0.1`)
2. Firewall allows port 5000
3. Devices are on same network
4. Using correct IP address

### No Videos Showing
**Checklist**:
1. Videos are in `assets/videos/` folder
2. Files have supported extensions
3. Server has read permissions
4. Refresh the page

## 📝 Adding Videos

### Method 1: Copy Files
Simply copy video files to `assets/videos/` folder

### Method 2: Create Sample Video
```bash
python VideoConverter.py --test
```
Then move `movie.Mjpeg` to `assets/videos/` (if compatible)

### Method 3: Download Videos
Download videos from the internet and place in `assets/videos/`

## 🔒 Security Notes

⚠️ **Important**: This is a local/development server

- **No Authentication** - Anyone with network access can view videos
- **No Encryption** - Videos stream over unencrypted HTTP
- **Local Use Only** - Not intended for internet exposure

**For production use**, implement:
- User authentication
- HTTPS/SSL encryption
- Access control lists
- Rate limiting

## 🎓 Learning Resources

This project demonstrates:
- Flask web server development
- REST API design
- HTML5 video streaming
- Range request handling
- Modern web UI design
- Responsive CSS layout
- JavaScript event handling

## 📈 Performance Tips

### For Large Video Files
1. Use MP4 with H.264 codec (best compatibility)
2. Keep resolution reasonable (1080p or lower)
3. Use appropriate bitrate (don't exceed 10 Mbps)

### For Many Videos
1. Organize in subfolders (feature to be added)
2. Use consistent naming convention
3. Delete unused videos to save space

### For Slow Networks
1. Reduce video quality/bitrate
2. Use lower resolutions (720p instead of 1080p)
3. Consider WebM format for smaller file sizes

## 🚀 Future Enhancements

Potential features to add:
- 🔍 Search functionality
- 📁 Folder organization
- 📊 Video thumbnails extraction
- ⭐ Favorites/playlists
- 👤 User accounts
- 📥 Upload interface
- 🎬 Video information editing
- 📱 Mobile app
- 🔐 Access control

## 📞 Support

### Common Commands

**Start server:**
```bash
python web_server.py
```

**Stop server:**
Press `Ctrl+C` in terminal

**Check if port is in use:**
```bash
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000
```

---

**Enjoy your web-based video streaming server!** 🎬🌐

For more information about the original RTSP/RTP implementation, see `TECHNICAL_DOC.md`.
